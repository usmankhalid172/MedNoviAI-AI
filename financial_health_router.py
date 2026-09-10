"""
Financial Health Score API — HisabDo AI, Day 10
---------------------------------------------------
Implements the API contract defined in Section 17 of the spec:

    Endpoint: GET /api/ai/financial-health/{userId}

    Example response:
    {
        "score": 80,
        "status": "Good",
        "savingRate": 27.67,
        "expenseRatio": 72.33,
        "budgetStatus": "Within Budget",
        "cashFlow": 41500,
        "expenseGrowth": 18,
        "insights": [
            "Saving behavior is healthy",
            "Expenses increased compared with the previous period"
        ]
    }

Backend Processing Flow (Section 16):
    1. Authenticate user
    2. Retrieve only that user's permitted records
    3. Aggregate income and expenses
    4. Calculate each factor
    5. Add weighted scores
    6. Assign status
    7. Generate structured insights
    8. (Optionally) send verified values to LLM for natural-language explanation
    9. Return API response

NOTE: Steps 1-3 (auth + DB aggregation) depend on HisabDo's actual database
layer, which is not available in this module. `get_user_financial_data()`
below is the integration point — replace its body with the real DB query
once the HisabDo schema/repository is wired in. Everything downstream
(steps 4-9) is fully implemented and spec-compliant.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from financial_health_scoring import FinancialData, calculate_financial_health_score

router = APIRouter(prefix="/api/ai", tags=["Financial Health Score"])


# ---------------------------------------------------------------------
# Response model — mirrors the exact API contract (Section 17)
# ---------------------------------------------------------------------

class FinancialHealthResponse(BaseModel):
    score: float
    status: str
    savingRate: float
    expenseRatio: float
    budgetStatus: str
    cashFlow: float
    expenseGrowth: Optional[float]
    insights: List[str]


# ---------------------------------------------------------------------
# Integration point — swap this for the real HisabDo DB query
# (Section 16, steps 1-3: authenticate, retrieve, aggregate)
# ---------------------------------------------------------------------

def get_user_financial_data(user_id: str) -> FinancialData:
    """
    Placeholder for HisabDo's real data-access layer.
    Replace this with actual DB aggregation logic:
      - authenticate + verify the requester owns this userId
      - sum transactions by type (income/expense) for the period
      - fetch the user's active budget, if any
      - fetch previous-period expense total
      - fetch outstanding debt/udhaar total

    Raising HTTPException(404) here if the user has no records at all
    covers the 'Test users with no transactions' requirement (Section 19).
    """
    raise NotImplementedError(
        "get_user_financial_data() must be connected to the HisabDo "
        "database layer (User ID, Transaction, Budget, Debt/Udhaar tables)."
    )


# ---------------------------------------------------------------------
# Endpoint
# ---------------------------------------------------------------------

@router.get("/financial-health/{user_id}", response_model=FinancialHealthResponse)
def get_financial_health(user_id: str):
    try:
        data = get_user_financial_data(user_id)
    except NotImplementedError as e:
        # Left explicit (rather than hidden) so the team knows this route
        # is calculation-ready but still needs the DB layer wired in.
        raise HTTPException(status_code=501, detail=str(e))

    result = calculate_financial_health_score(data)
    return result
