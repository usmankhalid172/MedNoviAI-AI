"""
Financial Health Score API — HisabDo AI, Day 10
---------------------------------------------------
Implements the API contract defined in Section 17 of the spec:

    Endpoint: GET /api/ai/financial-health/{userId}

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

Initial development/testing uses a dummy data provider in this repository.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

from financial_health_scoring import FinancialData, calculate_financial_health_score

router = APIRouter(prefix="/api/ai", tags=["Financial Health Score"])


# ---------------------------------------------------------------------
# Response model — mirrors the requested API contract
# ---------------------------------------------------------------------

class FinancialHealthResponse(BaseModel):
    score: float
    status: str
    income: float
    expenses: float
    savingRate: float
    expenseRatio: float
    budgetUtilization: Optional[float]
    cashFlow: float
    budgetStatus: str
    expenseGrowth: Optional[float]
    factorScores: Dict[str, Any]
    insights: List[str]


# ---------------------------------------------------------------------
# Integration point — dummy data provider for local development/testing
# (Section 16, steps 1-3: authenticate, retrieve, aggregate)
# ---------------------------------------------------------------------

def get_user_financial_data(user_id: str) -> FinancialData:
    """
    Local test implementation. This returns a deterministic dummy dataset for
    the requested user_id, giving the project an end-to-end path without the
    HisabDo DB integration being available.

    In a real deployment, this function should validate authentication and
    ownership, then retrieve only records tied to this user_id.
    """
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")

    # Dummy dataset intentionally kept stable for regression testing.
    # This mirrors the worked example and the requested response contract.
    return FinancialData(
        total_income=150000,
        total_expense=108500,
        budget=103000,
        previous_expense=92000,
        debt_amount=12000,
        has_transactions=True,
    )


# ---------------------------------------------------------------------
# Endpoint
# ---------------------------------------------------------------------

@router.get("/financial-health/{user_id}", response_model=FinancialHealthResponse)
def get_financial_health(user_id: str):
    try:
        data = get_user_financial_data(user_id)
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))

    result = calculate_financial_health_score(data)
    return result
