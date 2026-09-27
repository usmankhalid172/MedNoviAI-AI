"""
Structured request/response contracts for the AI <-> .NET backend integration.
Keep this file as the single source of truth for the API contract.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


# ---------- Shared ----------

class SafetyFlag(BaseModel):
    is_emergency: bool = False
    is_diagnosis_request: bool = False
    is_prescription_request: bool = False
    disclaimer: Optional[str] = None


# ---------- /api/ai/chat ----------

class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Stable ID for the patient's conversation")
    message: str = Field(..., min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    safety: SafetyFlag
    turn_count: int


# ---------- /api/ai/intake ----------

class SymptomEntry(BaseModel):
    name: str
    duration: Optional[str] = None
    severity: Optional[Literal["mild", "moderate", "severe", "unknown"]] = "unknown"
    notes: Optional[str] = None


class PatientIntakeData(BaseModel):
    symptoms: list[SymptomEntry] = Field(default_factory=list)
    duration_overall: Optional[str] = None
    context: Optional[str] = None
    missing_fields: list[str] = Field(default_factory=list)
    is_complete: bool = False


class IntakeRequest(BaseModel):
    session_id: str
    message: str = Field(..., min_length=1, max_length=4000)


class IntakeResponse(BaseModel):
    session_id: str
    intake_data: PatientIntakeData
    follow_up_question: Optional[str] = None
    safety: SafetyFlag
    summary: Optional[str] = None


# ---------- /api/ai/recommend-specialty ----------

class SpecialtyRequest(BaseModel):
    session_id: Optional[str] = None
    intake_data: PatientIntakeData


class SpecialtyMatch(BaseModel):
    specialty: str
    confidence: Literal["low", "medium", "high"]
    doc_id: Optional[str] = None
    matched_terms: list[str] = Field(default_factory=list)


class SpecialtyResponse(BaseModel):
    recommendations: list[SpecialtyMatch]
    disclaimer: str
    knowledge_base_notes: list[str] = Field(default_factory=list)
