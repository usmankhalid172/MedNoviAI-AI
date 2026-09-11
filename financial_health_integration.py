"""
Financial Health Score — Mobile/Web Integration Layer
HisabDo AI, Day 10 — Task owner: Laiba (API + Mobile/Web Integration)

This module sits on top of Omesh's backend:
    financial_health_scoring.py  -> deterministic scoring engine
    financial_health_router.py   -> GET /api/ai/financial-health/{userId}

Responsibilities (per assignment):
    1. Call GET /api/ai/financial-health/{userId}
    2. Handle the raw HTTP response (success + every error case)
    3. Build the "score + status" display block
    4. Build factor-level strengths/weaknesses (Section 18 of the spec)
    5. Surface the AI Insight text
    6. Produce one clean, reusable output structure for mobile/web (Flutter/React/etc.)

IMPORTANT — GAP FOUND DURING VERIFICATION (flag to team lead / Omesh):
    The API contract (Section 17) and the current calculate_financial_health_score()
    return only: score, status, savingRate, expenseRatio, budgetStatus, cashFlow,
    expenseGrowth, insights.

    Two of the six factors needed for the Section 18 UI ("Debt/Udhaar — Healthy")
    are NOT exposed at all:
        - debt/udhaar label (score_debt_udhaar() computes it internally but the
          final response dict never includes it)
        - a cash-flow *status* label ("Strong Positive" / "Positive" / "Negative")
          is computed internally too, but only the raw `cashFlow` amount is
          returned — and total income isn't returned either, so the client
          cannot re-derive the correct band on its own.

    Until the backend adds `debtStatus` and `cashFlowStatus` fields, this layer
    falls back to deriving best-effort labels from what IS available (see
    _cash_flow_label and _debt_fallback below), and marks them as
    "estimated" in the output so mobile/web knows not to treat them as
    verified/authoritative the way the spec's Golden Rule intends.
"""

from dataclasses import dataclass
from typing import Optional
import requests


# ---------------------------------------------------------------------
# 1. Config
# ---------------------------------------------------------------------

API_BASE_URL = "http://localhost:8000"  # replace with real HisabDo backend host


class FinancialHealthAPIError(Exception):
    """Raised for any non-200 response, with the HTTP status attached."""

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"[{status_code}] {detail}")


# ---------------------------------------------------------------------
# 2. Step 1 — Call the API
# ---------------------------------------------------------------------

def fetch_financial_health(user_id: str, base_url: str = API_BASE_URL, timeout: float = 5.0) -> dict:
    """
    Calls GET /api/ai/financial-health/{userId} and returns the parsed JSON body
    on success. Raises FinancialHealthAPIError on any error response so the
    caller (UI layer) can branch on status_code.

    Known status codes from the current backend:
        200 -> normal response (see FinancialHealthResponse model)
        404 -> user not found / no records at all
        501 -> DB layer not wired in yet (NotImplementedError in
               get_user_financial_data) — this is expected right now,
               since Omesh's router is calculation-ready but not DB-connected.
        5xx -> unexpected server error
    """
    url = f"{base_url}/api/ai/financial-health/{user_id}"
    try:
        response = requests.get(url, timeout=timeout)
    except requests.exceptions.RequestException as exc:
        raise FinancialHealthAPIError(0, f"Network/connection error: {exc}") from exc

    if response.status_code == 200:
        return response.json()

    # FastAPI's HTTPException wraps the message in {"detail": "..."}
    try:
        detail = response.json().get("detail", response.text)
    except ValueError:
        detail = response.text
    raise FinancialHealthAPIError(response.status_code, detail)


# ---------------------------------------------------------------------
# 3. Step 2 — Response handling / error mapping for the UI
# ---------------------------------------------------------------------

def handle_api_error(error: FinancialHealthAPIError) -> dict:
    """
    Maps backend error codes to a user-facing UI state, so mobile/web never
    has to show a raw stack trace or HTTP code to the end user.
    """
    if error.status_code == 404:
        return {
            "state": "no_data",
            "title": "No financial data yet",
            "message": "We couldn't find any records for this account yet. "
                       "Add a few transactions to see your Financial Health Score.",
        }
    if error.status_code == 501:
        return {
            "state": "not_ready",
            "title": "Financial Health is not available yet",
            "message": "This feature is still being connected on our end. Please check back soon.",
        }
    if error.status_code == 0:
        return {
            "state": "offline",
            "title": "You're offline",
            "message": "Couldn't reach the server. Check your connection and try again.",
        }
    return {
        "state": "error",
        "title": "Something went wrong",
        "message": "We couldn't load your Financial Health Score right now. Please try again.",
    }


# ---------------------------------------------------------------------
# 4. Step 3 — Factor-level strengths/weaknesses (Section 18)
# ---------------------------------------------------------------------
# These thresholds mirror the spec's own scoring tables (Sections 5, 6, 10)
# so the *label* a user sees always lines up with the *score* they got.

def _saving_label(saving_rate: Optional[float]) -> str:
    if saving_rate is None:
        return "Unknown"
    if saving_rate >= 25:
        return "Strong"
    if saving_rate >= 15:
        return "Good"
    if saving_rate >= 5:
        return "Weak"
    return "Needs Attention"


def _expense_control_label(expense_ratio: Optional[float]) -> str:
    if expense_ratio is None:
        return "Unknown"
    if expense_ratio <= 60:
        return "Good"
    if expense_ratio <= 80:
        return "Fair"
    return "Needs Attention"


def _budget_label(budget_status: Optional[str]) -> str:
    mapping = {
        "Within Budget": "Good",
        "No Budget Set": "Not Set",
        "Slightly Over Budget": "Fair",
        "Over Budget": "Needs Attention",
        "Significantly Over Budget": "Needs Attention",
        "Far Over Budget": "Needs Attention",
        "No Data": "Unknown",
    }
    return mapping.get(budget_status, "Unknown")


def _cash_flow_label(cash_flow: Optional[float]) -> str:
    """
    Best-effort ESTIMATE only — see the GAP note at the top of this file.
    Real band ("Strong Positive" vs "Positive") needs income context that
    the API does not currently return; sign-only is all that's reliable here.
    """
    if cash_flow is None:
        return "Unknown"
    if cash_flow > 0:
        return "Positive (estimated)"
    if cash_flow == 0:
        return "Near Zero"
    return "Negative"


def _expense_growth_label(expense_growth: Optional[float]) -> str:
    if expense_growth is None:
        return "No Prior Period Data"
    if expense_growth < 0:
        return "Decreasing"
    if expense_growth <= 10:
        return "Stable"
    if expense_growth <= 20:
        return "Rising"
    return "Needs Attention"


def _debt_fallback() -> str:
    """
    Cannot be computed at all from the current API contract — debt data is
    dropped before the response is built on the backend. Flagged as a gap.
    """
    return "Not Available (backend does not return debt data yet)"


# ---------------------------------------------------------------------
# 5. Step 4 — Build the full mobile/web display structure
# ---------------------------------------------------------------------

def build_display_payload(api_response: dict) -> dict:
    """
    Converts the raw API JSON into the exact shape Section 18 describes:
      - Financial Health score/status header
      - Factor-level strengths/weaknesses
      - AI Insight text(s)
    This is the single object mobile and web both consume — neither platform
    talks to the raw API response directly.
    """
    score = api_response.get("score")
    status = api_response.get("status")
    saving_rate = api_response.get("savingRate")
    expense_ratio = api_response.get("expenseRatio")
    budget_status = api_response.get("budgetStatus")
    cash_flow = api_response.get("cashFlow")
    expense_growth = api_response.get("expenseGrowth")
    insights = api_response.get("insights", [])

    return {
        "header": {
            "title": "Financial Health",
            "score": score,
            "scoreDisplay": f"{score}/100" if score is not None else "N/A",
            "status": status,
        },
        "factors": [
            {"name": "Saving Behavior", "value": saving_rate, "label": _saving_label(saving_rate)},
            {"name": "Expense Control", "value": expense_ratio, "label": _expense_control_label(expense_ratio)},
            {"name": "Budget Control", "value": budget_status, "label": _budget_label(budget_status)},
            {"name": "Cash Flow", "value": cash_flow, "label": _cash_flow_label(cash_flow)},
            {"name": "Debt / Udhaar", "value": None, "label": _debt_fallback()},
            {"name": "Expense Growth", "value": expense_growth, "label": _expense_growth_label(expense_growth)},
        ],
        "aiInsight": " ".join(insights) if insights else "No insights available.",
        "insightsList": insights,
    }


# ---------------------------------------------------------------------
# 6. Single entry point the mobile/web layer calls
# ---------------------------------------------------------------------

def get_financial_health_for_ui(user_id: str, base_url: str = API_BASE_URL) -> dict:
    """
    One function for the client to call. Always returns a dict with a
    top-level "ok" flag so the UI layer never has to catch exceptions itself.
    """
    try:
        api_response = fetch_financial_health(user_id, base_url)
    except FinancialHealthAPIError as error:
        return {"ok": False, "errorState": handle_api_error(error)}

    return {"ok": True, "data": build_display_payload(api_response)}


if __name__ == "__main__":
    # Quick manual check using the worked example from Section 11 of the spec
    from financial_health_scoring import FinancialData, calculate_financial_health_score

    example = FinancialData(
        total_income=150000,
        total_expense=108500,
        budget=103000,
        previous_expense=92000,
        debt_amount=12000,
    )
    raw = calculate_financial_health_score(example)
    print("Raw API-shaped response:", raw)
    print("\nMobile/Web display payload:")
    import json
    print(json.dumps(build_display_payload(raw), indent=2))
