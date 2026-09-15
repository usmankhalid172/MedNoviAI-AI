from __future__ import annotations

from typing import Optional

from .safety_guardrails import check_safety, emergency_response
from .schemas import (
    IntakeResponse,
    PatientIntake,
    SafetyCheck,
    Symptom,
)
from .symptom_extractor import extract_symptom_data


def determine_missing_information(symptoms: list[Symptom], duration: Optional[str]) -> list[str]:
    missing: list[str] = []

    if not symptoms:
        missing.append("symptoms")

    if duration is None:
        missing.append("duration")

    return missing


def process_patient_message(
    message: str,
    conversation_id: Optional[str] = None,
) -> IntakeResponse:
    if not message or not message.strip():
        raise ValueError("Patient message must not be empty.")

    extraction = extract_symptom_data(message)
    safety = check_safety(message)

    symptoms = [
        Symptom(name=name, duration=extraction["duration"])
        for name in extraction["symptoms"]
    ]

    safety_check = SafetyCheck(**safety)

    if safety_check.is_emergency:
        intake = PatientIntake(
            patient_input=message,
            symptoms=symptoms,
            duration=extraction["duration"],
            missing_information=[],
            safety_check=safety_check,
        )

        return IntakeResponse(
            status="success",
            conversation_id=conversation_id,
            intake=intake,
            next_action="emergency_guidance",
            response=emergency_response(),
        )

    missing = determine_missing_information(symptoms, extraction["duration"])

    if missing:
        if "symptoms" in missing:
            response = "Please tell me your main symptoms so I can understand your concern."
        else:
            response = "How long have you had these symptoms?"

        next_action = "ask_clarification"
    else:
        response = (
            "Thank you. I have captured the symptoms and duration you provided."
        )
        next_action = "continue_intake"

    intake = PatientIntake(
        patient_input=message,
        symptoms=symptoms,
        duration=extraction["duration"],
        missing_information=missing,
        safety_check=safety_check,
    )

    return IntakeResponse(
        status="success",
        conversation_id=conversation_id,
        intake=intake,
        next_action=next_action,
        response=response,
    )
