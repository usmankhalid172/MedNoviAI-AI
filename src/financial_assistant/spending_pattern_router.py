"""FastAPI route for verified spending pattern intelligence."""
from fastapi import APIRouter, Depends, Query

from ..security import require_internal_token
from .spending_pattern_intelligence import get_spending_pattern_intelligence_service

router = APIRouter(
    prefix="/api/v1",
    tags=["spending-pattern-intelligence"],
    dependencies=[Depends(require_internal_token)],
)


@router.get(
    "/spending-pattern-intelligence/{user_id}",
    summary="Return verified spending-pattern intelligence for a single user",
)
def spending_pattern_intelligence(
    user_id: str,
    start_date: str | None = Query(default=None),
    end_date: str | None = Query(default=None),
):
    service = get_spending_pattern_intelligence_service()
    try:
        return service.get_spending_pattern_intelligence(user_id, start_date, end_date)
    except ValueError as exc:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=str(exc)) from exc
