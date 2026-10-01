"""FastAPI router exposing a minimal verified anomaly endpoint."""
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from typing import Any

from ..security import require_internal_token
from .anomaly_detection_service import get_anomaly_detection_service

router = APIRouter(
    prefix="/api/v1",
    tags=["anomaly-detection"],
    dependencies=[Depends(require_internal_token)],
)


class AnomalyRecord(BaseModel):
    transaction_id: str
    user_id: str
    anomaly_type: str
    amount: float
    category: str
    date: str
    expected_amount: float | None = None
    severity: str
    reason: str


class AnomalyResponse(BaseModel):
    user_id: str
    analysis_days: int
    anomalies: list[AnomalyRecord]
    verified: bool = True
    source: str = "verified_hisabdo_transaction_ledger"


@router.get(
    "/anomalies/{user_id}",
    response_model=AnomalyResponse,
    summary="Return verified anomaly results for one authenticated user",
)
def anomalies(user_id: str, analysis_days: int = Query(default=30, ge=1)):
    service = get_anomaly_detection_service()
    try:
        return service.get_anomalies(user_id, analysis_days)
    except ValueError as exc:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=str(exc)) from exc
