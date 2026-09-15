from __future__ import annotations

import re
from typing import Dict, Optional


# Safety priority:
# emergency > prescription > diagnosis > normal
EMERGENCY_PATTERNS = (
    "severe chest pain",
    "chest pain and difficulty breathing",
    "difficulty breathing",
    "shortness of breath",
    "cannot breathe",
    "can't breathe",
    "heavy bleeding",
    "severe bleeding",
    "unconscious",
    "loss of consciousness",
    "signs of stroke",
    "stroke symptoms",
)


# These patterns target personalized prescribing or medication-change requests.
PRESCRIPTION_PATTERNS = (
    "what medicine should i take",
    "what medication should i take",
    "what drug should i take",
    "what antibiotic should i take",
    "which antibiotic should i take",
    "what prescription should i take",
    "what dosage should i take",
    "what dose should i take",
    "can i increase my dosage",
    "can i increase my dose",
    "should i increase my dosage",
    "should i stop my medication",
    "should i stop taking my medicine",
    "should i change my medication",
    "should i switch my medication",
    "prescribe me",
    "prescribe a medicine",
)


DIAGNOSIS_PATTERNS = (
    "diagnose me",
    "what disease do i have",
    "what condition do i have",
    "what illness do i have",
    "what's wrong with me",
    "what is wrong with me",
    "do i have covid",
    "do i have diabetes",
    "do i definitely have",
    "what is my diagnosis",
)


def _normalize(text: str) -> str:
    """Normalize user text for deterministic pattern matching."""
    return re.sub(r"\s+", " ", (text or "").lower().strip())


def _contains_any(text: str, patterns: tuple[str, ...]) -> bool:
    """Return True when any configured pattern is present."""
    return any(pattern in text for pattern in patterns)


def classify_request(text: str) -> Dict[str, Optional[object]]:
    """
    Classify a healthcare request using deterministic safety priorities.

    Priority:
        1. emergency
        2. prescription
        3. diagnosis
        4. normal
    """
    normalized = _normalize(text)

    if not normalized:
        return {
            "category": "normal",
            "is_emergency": False,
            "is_prescription": False,
            "is_diagnosis": False,
            "reason": None,
        }

    # Emergency always has the highest priority.
    if _contains_any(normalized, EMERGENCY_PATTERNS):
        return {
            "category": "emergency",
            "is_emergency": True,
            "is_prescription": False,
            "is_diagnosis": False,
            "reason": "Potential emergency symptoms detected.",
        }

    if _contains_any(normalized, PRESCRIPTION_PATTERNS):
        return {
            "category": "prescription",
            "is_emergency": False,
            "is_prescription": True,
            "is_diagnosis": False,
            "reason": "Personalized prescription or medication-change request detected.",
        }

    if _contains_any(normalized, DIAGNOSIS_PATTERNS):
        return {
            "category": "diagnosis",
            "is_emergency": False,
            "is_prescription": False,
            "is_diagnosis": True,
            "reason": "Diagnosis request detected.",
        }

    return {
        "category": "normal",
        "is_emergency": False,
        "is_prescription": False,
        "is_diagnosis": False,
        "reason": None,
    }


def check_safety(text: str) -> Dict[str, Optional[object]]:
    """
    Backward-compatible safety check used by the existing Sprint 1 tests.
    """
    result = classify_request(text)

    return {
        "is_emergency": result["is_emergency"],
        "reason": result["reason"],
        "category": result["category"],
        "is_prescription": result["is_prescription"],
        "is_diagnosis": result["is_diagnosis"],
    }


def emergency_response() -> str:
    """Return safety-first guidance without diagnosing the user."""
    return (
        "This may require urgent medical attention. "
        "Please seek professional medical or emergency care immediately. "
        "This assistant cannot provide a diagnosis and is not a substitute "
        "for professional medical care."
    )


def prescription_refusal_response() -> str:
    """Refuse personalized prescription or dosage instructions."""
    return (
        "I can't prescribe medicines or provide personalized dosage instructions. "
        "Please consult a qualified healthcare professional or pharmacist for "
        "advice about the appropriate medication or dose."
    )


def diagnosis_refusal_response() -> str:
    """Refuse to provide a definitive diagnosis."""
    return (
        "I can't provide a definitive medical diagnosis. "
        "I can provide general health information, but a qualified healthcare "
        "professional should evaluate your symptoms and provide a diagnosis."
    )


def get_safety_response(text: str) -> Optional[str]:
    """
    Return the required safety/refusal response.

    Emergency has the highest priority, followed by prescription,
    then diagnosis.

    Returns None for normal informational requests.
    """
    category = classify_request(text)["category"]

    if category == "emergency":
        return emergency_response()

    if category == "prescription":
        return prescription_refusal_response()

    if category == "diagnosis":
        return diagnosis_refusal_response()

    return None