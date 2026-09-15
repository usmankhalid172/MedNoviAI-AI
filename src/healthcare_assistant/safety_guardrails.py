from __future__ import annotations

import re
from typing import Dict, Optional


# Safety priority:
# emergency > prescription > diagnosis > normal
EMERGENCY_PATTERNS = (
    "severe chest pain",
    "crushing chest pain",
    "chest pain and difficulty breathing",
    "chest pain and shortness of breath",
    "difficulty breathing",
    "shortness of breath",
    "cannot breathe",
    "can't breathe",
    "unable to breathe",
    "heavy bleeding",
    "severe bleeding",
    "uncontrolled bleeding",
    "unconscious",
    "loss of consciousness",
    "passed out",
    "signs of stroke",
    "stroke symptoms",
    "severe allergic reaction",
    "throat swelling",
    "swelling of throat",
    "seizure",
)


# These patterns target personalized medication or prescription requests.
PRESCRIPTION_PATTERNS = (
    "what medicine should i take",
    "what medication should i take",
    "what drug should i take",
    "what antibiotic should i take",
    "which antibiotic should i take",
    "what prescription should i take",
    "what dosage should i take",
    "what dose should i take",
    "what dose should i use",
    "can i increase my dosage",
    "can i increase my dose",
    "should i increase my dosage",
    "should i increase my dose",
    "should i decrease my dosage",
    "should i decrease my dose",
    "should i stop my medication",
    "should i stop taking my medicine",
    "should i change my medication",
    "should i switch my medication",
    "should i start this medication",
    "prescribe me",
    "prescribe a medicine",
    "prescribe medication",
)


# These patterns target requests for diagnosis or confirmation of a condition.
DIAGNOSIS_PATTERNS = (
    "diagnose me",
    "what disease do i have",
    "what condition do i have",
    "what illness do i have",
    "what disorder do i have",
    "what's wrong with me",
    "what is wrong with me",
    "do i have covid",
    "do i have diabetes",
    "do i have cancer",
    "do i definitely have",
    "what is my diagnosis",
    "tell me my diagnosis",
    "is this definitely",
)


def _normalize(text: str) -> str:
    """Normalize user input for deterministic safety matching."""
    return re.sub(r"\s+", " ", (text or "").lower().strip())


def _contains_any(text: str, patterns: tuple[str, ...]) -> bool:
    """Return True if at least one configured pattern is present."""
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
            "requires_immediate_redirect": False,
            "reason": None,
        }

    # Emergency must always be evaluated first.
    if _contains_any(normalized, EMERGENCY_PATTERNS):
        return {
            "category": "emergency",
            "is_emergency": True,
            "is_prescription": False,
            "is_diagnosis": False,
            "requires_immediate_redirect": True,
            "reason": "Potential emergency symptoms detected.",
        }

    if _contains_any(normalized, PRESCRIPTION_PATTERNS):
        return {
            "category": "prescription",
            "is_emergency": False,
            "is_prescription": True,
            "is_diagnosis": False,
            "requires_immediate_redirect": False,
            "reason": "Personalized prescription or medication request detected.",
        }

    if _contains_any(normalized, DIAGNOSIS_PATTERNS):
        return {
            "category": "diagnosis",
            "is_emergency": False,
            "is_prescription": False,
            "is_diagnosis": True,
            "requires_immediate_redirect": False,
            "reason": "Diagnosis request detected.",
        }

    return {
        "category": "normal",
        "is_emergency": False,
        "is_prescription": False,
        "is_diagnosis": False,
        "requires_immediate_redirect": False,
        "reason": None,
    }


def check_safety(text: str) -> Dict[str, Optional[object]]:
    """
    Backward-compatible safety check plus Sept 9 safety metadata.
    """
    result = classify_request(text)

    return {
        "is_emergency": result["is_emergency"],
        "is_prescription": result["is_prescription"],
        "is_diagnosis": result["is_diagnosis"],
        "category": result["category"],
        "requires_immediate_redirect": result["requires_immediate_redirect"],
        "reason": result["reason"],
    }


def should_redirect_immediately(text: str) -> bool:
    """
    Return True when the request requires immediate emergency redirection.

    This function is intentionally limited to emergency handling. Diagnosis
    and prescription requests use refusal logic but do not trigger emergency
    redirection.
    """
    result = classify_request(text)

    return bool(
        result["is_emergency"]
        and result["requires_immediate_redirect"]
    )


def emergency_response() -> str:
    """
    Return an immediate emergency redirect without diagnosis or treatment advice.
    """
    return (
        "This may require immediate medical attention. "
        "Please contact local emergency services or seek emergency medical care "
        "immediately. This assistant cannot diagnose or treat an emergency and "
        "is not a substitute for professional medical care."
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

    Priority:
        emergency -> prescription -> diagnosis -> normal

    Emergency cases are intended to be redirected before normal AI processing.
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