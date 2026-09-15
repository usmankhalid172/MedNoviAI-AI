from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class Symptom(BaseModel):
    name: str
    duration: Optional[str] = None
    severity: Optional[str] = None


class SafetyCheck(BaseModel):
    is_emergency: bool
    reason: Optional[str] = None


class PatientIntake(BaseModel):
    patient_input: str
    symptoms: List[Symptom] = Field(default_factory=list)
    duration: Optional[str] = None
    severity: Optional[str] = None
    missing_information: List[str] = Field(default_factory=list)
    safety_check: SafetyCheck


class IntakeResponse(BaseModel):
    status: str
    conversation_id: Optional[str] = None
    intake: PatientIntake
    next_action: str
    response: str
