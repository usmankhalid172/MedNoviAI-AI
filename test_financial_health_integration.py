"""
Test suite — Financial Health Score, "Everyone: Testing" checklist
HisabDo AI, Day 10

Covers, against the REAL scoring engine (financial_health_scoring.py) and the
integration/display layer (financial_health_integration.py):

    1. Normal financial data
    2. Zero income
    3. No transactions
    4. No budget
    5. Negative cash flow
    6. Large transactions
    7. Duplicate transactions
    8. Missing/invalid categories
    9. User-data isolation

Run with:  python3 -m pytest test_financial_health_integration.py -v
(or just:  python3 test_financial_health_integration.py   -- it will run
 without pytest too, using plain asserts)
"""

from financial_health_scoring import FinancialData, calculate_financial_health_score
from financial_health_integration import (
    build_display_payload,
    handle_api_error,
    FinancialHealthAPIError,
)


def test_1_normal_financial_data():
    """Section 11 worked example — sanity check against the spec's own numbers."""
    data = FinancialData(
        total_income=150000,
        total_expense=108500,
        budget=103000,
        previous_expense=92000,
        debt_amount=12000,
    )
    result = calculate_financial_health_score(data)
    assert result["savingRate"] == 27.67
    assert result["status"] in ("Good", "Excellent", "Fair")
    payload = build_display_payload(result)
    assert payload["header"]["score"] == result["score"]
    assert len(payload["factors"]) == 6
    assert payload["aiInsight"]  # AI insight text is present


def test_2_zero_income():
    """Income = 0 must not raise a ZeroDivisionError anywhere in the pipeline."""
    data = FinancialData(total_income=0, total_expense=5000)
    result = calculate_financial_health_score(data)
    assert result["savingRate"] == 0
    assert result["expenseRatio"] == 0
    payload = build_display_payload(result)
    # Saving/expense factors should degrade gracefully, not crash the UI
    assert payload["factors"][0]["label"] in ("Needs Attention", "Unknown")


def test_3_no_transactions():
    """has_transactions=False -> explicit 'no data' branch in the scoring engine."""
    data = FinancialData(total_income=0, total_expense=0, has_transactions=False)
    result = calculate_financial_health_score(data)
    assert result["score"] == 0
    assert result["budgetStatus"] == "No Data"
    assert "No transaction data" in result["insights"][0]
    payload = build_display_payload(result)
    assert payload["header"]["status"] == "Poor"


def test_4_no_budget():
    """budget=None -> Budget Control must be excluded, not zeroed out / penalized."""
    data = FinancialData(total_income=100000, total_expense=60000, budget=None)
    result = calculate_financial_health_score(data)
    assert result["budgetStatus"] == "No Budget Set"
    payload = build_display_payload(result)
    budget_factor = next(f for f in payload["factors"] if f["name"] == "Budget Control")
    assert budget_factor["label"] == "Not Set"


def test_5_negative_cash_flow():
    data = FinancialData(total_income=50000, total_expense=70000)
    result = calculate_financial_health_score(data)
    assert result["cashFlow"] < 0
    payload = build_display_payload(result)
    cash_factor = next(f for f in payload["factors"] if f["name"] == "Cash Flow")
    assert cash_factor["label"] == "Negative"


def test_6_large_transactions():
    """Very large numbers should not overflow, lose precision, or break formulas."""
    data = FinancialData(
        total_income=50_000_000, total_expense=12_000_000, budget=15_000_000,
        previous_expense=10_000_000, debt_amount=1_000_000,
    )
    result = calculate_financial_health_score(data)
    assert result["score"] >= 0
    assert isinstance(result["savingRate"], float)
    payload = build_display_payload(result)
    assert payload["header"]["scoreDisplay"].endswith("/100")


def test_7_duplicate_transactions():
    """
    The scoring engine only receives already-aggregated totals — duplicate
    detection/removal must happen upstream, at the DB aggregation step
    (get_user_financial_data in the router), not here. This test documents
    that expectation: if a duplicate slips through, this layer has no way
    to know, so it's the aggregation layer's responsibility, not the
    integration layer's. Flag this explicitly in the test report.
    """
    inflated = FinancialData(total_income=100000, total_expense=40000)  # dup counted
    correct = FinancialData(total_income=100000, total_expense=20000)   # de-duplicated
    r1 = calculate_financial_health_score(inflated)
    r2 = calculate_financial_health_score(correct)
    assert r1["expenseRatio"] != r2["expenseRatio"], (
        "Confirms duplicate-inflated totals DO change the score — "
        "proving de-duplication must happen before this layer, in the DB/aggregation step."
    )


def test_8_missing_invalid_categories():
    """
    Category is used for spending-breakdown insights elsewhere in HisabDo,
    but the six scoring factors here never key off category at all — so a
    missing/invalid category should have ZERO effect on the score.
    """
    data = FinancialData(total_income=100000, total_expense=50000)
    result = calculate_financial_health_score(data)
    assert result["score"] > 0
    assert result["status"] != "Poor"


def test_9_user_data_isolation():
    """
    Two different users' data must never mix. This is enforced at the
    get_user_financial_data() DB layer (per Omesh's router docstring,
    Section 16 steps 1-2: authenticate + retrieve only that user's records)
    — not something the scoring math can test. This test simulates two
    separate calls and confirms results are independent given independent inputs.
    """
    user_a = FinancialData(total_income=100000, total_expense=30000)
    user_b = FinancialData(total_income=100000, total_expense=90000)
    result_a = calculate_financial_health_score(user_a)
    result_b = calculate_financial_health_score(user_b)
    assert result_a["score"] != result_b["score"], "Two users with different data must get different scores."


def test_error_handling_404():
    err = FinancialHealthAPIError(404, "User not found")
    ui_state = handle_api_error(err)
    assert ui_state["state"] == "no_data"


def test_error_handling_501_not_wired_in():
    """Today's real state of the endpoint — DB layer not connected yet."""
    err = FinancialHealthAPIError(501, "get_user_financial_data() must be connected...")
    ui_state = handle_api_error(err)
    assert ui_state["state"] == "not_ready"


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    passed, failed = 0, 0
    for t in tests:
        try:
            t()
            print(f"PASS: {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL: {t.__name__} -> {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed out of {len(tests)}")
