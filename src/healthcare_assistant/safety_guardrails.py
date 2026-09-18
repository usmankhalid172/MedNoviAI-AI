from __future__ import annotations

import re
from typing import Dict, Optional


# Safety priority:
# emergency override > prescription refusal > diagnosis refusal > normal

EMERGENCY_PATTERNS = (
    # Chest pain / cardiac-style emergencies
    r"\b(?:severe|crushing|intense|very bad)\s+(?:chest\s+)?pain\b",
    r"\bmy\s+chest\s+(?:hurts|is\s+hurting|really\s+hurts)\b",
    r"\bchest\s+pain\b",

    # Breathing emergencies
    r"\b(?:can't|cannot|can not|unable to)\s+(?:breathe|breathing)\b",
    r"\b(?:having trouble|struggling|difficulty|hard|hard time)\s+(?:breathing|to breathe)\b",
    r"\bshortness\s+of\s+breath\b",
    r"\bcan't\s+catch\s+my\s+breath\b",
    r"\bcan['’]t\s+catch\s+my\s+breath\b",

    # Bleeding
    r"\b(?:heavy|severe|uncontrolled|a lot of)\s+(?:bleeding|blood)\b",

    # Consciousness
    r"\b(?:i\s+)?(?:passed|passing)\s+out\b",
    r"\bloss\s+of\s+consciousness\b",
    r"\bunconscious\b",

    # Stroke
    r"\bsigns?\s+of\s+(?:a\s+)?stroke\b",
    r"\bstroke\s+symptoms?\b",

    # Allergic reaction
    r"\bsevere\s+allergic\s+reaction\b",
    r"\b(?:my\s+)?throat\s+(?:is\s+)?swelling\b",
    r"\bswelling\s+(?:of|in)\s+(?:my\s+)?throat\b",

    # Seizure
    r"\bhaving\s+a\s+seizure\b",
    r"\bseizure\b",
)


# Personalized prescription / medication-change requests.
PRESCRIPTION_PATTERNS = (
    r"\bwhat\s+(?:medicine|medication|drug)\s+should\s+i\s+(?:take|use)\b",
    r"\bwhich\s+(?:medicine|medication|drug)\s+(?:should|can|could)\s+i\s+(?:take|use)\b",
    r"\bwhat\s+antibiotic\s+(?:should|can|could)\s+i\s+take\b",
    r"\bwhich\s+antibiotic\s+(?:should|can|could)\s+i\s+take\b",

    # Natural-language personalized medication requests
    r"\bwhich\s+(?:medicine|medication|drug|antibiotic)\s+would\s+be\s+(?:appropriate|best|suitable)\s+for\s+me\b",
    r"\bwhat\s+(?:medicine|medication|drug|antibiotic)\s+would\s+be\s+(?:appropriate|best|suitable)\s+for\s+me\b",
    r"\bwhich\s+(?:medicine|medication|drug|antibiotic)\s+is\s+(?:best|appropriate|suitable)\s+for\s+me\b",
    r"\bwhat\s+(?:medicine|medication|drug|antibiotic)\s+is\s+(?:best|appropriate|suitable)\s+for\s+me\b",

    # "What/which should I take for..."
    r"\bwhat\s+should\s+i\s+take\s+for\b",
    r"\bwhat\s+can\s+i\s+take\s+for\b",
    r"\bwhat\s+medicine\s+can\s+i\s+take\s+for\b",

    # Dosage questions
    r"\bwhat\s+(?:dose|dosage)\s+should\s+i\s+(?:take|use)\b",
    r"\bhow\s+much\s+(?:medicine|medication|of\s+this)\s+should\s+i\s+take\b",
    r"\bhow\s+many\s+(?:mg|milligrams|tablets|pills)\s+should\s+i\s+take\b",

    # Medication changes
    r"\bshould\s+i\s+(?:increase|decrease|double)\s+my\s+(?:dose|dosage)\b",
    r"\bcan\s+i\s+(?:increase|decrease|double)\s+my\s+(?:dose|dosage)\b",
    r"\bshould\s+i\s+stop\s+(?:taking\s+)?my\s+(?:medicine|medication)\b",
    r"\bcan\s+i\s+stop\s+(?:taking\s+)?my\s+(?:medicine|medication)\b",
    r"\bshould\s+i\s+(?:change|switch)\s+my\s+(?:medicine|medication)\b",
    r"\bcan\s+i\s+(?:change|switch)\s+my\s+(?:medicine|medication)\b",

    # Direct prescription requests
    r"\bprescribe\s+(?:me|a|some)\b",
    r"\bprescribe\s+(?:medicine|medication|a\s+drug)\b",
)


# Requests asking the assistant to diagnose or confirm a condition.
DIAGNOSIS_PATTERNS = (
    r"\bdiagnose\s+me\b",
    r"\bwhat\s+(?:disease|condition|illness|disorder)\s+do\s+i\s+have\b",
    r"\bwhat\s+is\s+my\s+diagnosis\b",
    r"\btell\s+me\s+my\s+diagnosis\b",

    r"\bdo\s+i\s+have\s+(?:covid|diabetes|cancer|pneumonia|flu|asthma)\b",
    r"\bdo\s+i\s+definitely\s+have\b",

    # Natural-language diagnosis variants
    r"\bcould\s+this\s+be\s+(?:a\s+)?(?:disease|condition|illness|infection)\b",
    r"\bcould\s+this\s+be\s+(?:covid|diabetes|cancer|pneumonia|flu|asthma|a\s+heart\s+attack|a\s+stroke)\b",

    r"\bcould\s+(?:these|those)\s+symptoms\s+(?:mean|indicate|suggest)\s+(?:that\s+)?i\s+have\b",
    r"\bmight\s+(?:these|those)\s+symptoms\s+(?:mean|indicate|suggest)\s+(?:that\s+)?i\s+have\b",
    r"\bmay\s+(?:these|those)\s+symptoms\s+(?:mean|indicate|suggest)\s+(?:that\s+)?i\s+have\b",

    r"\bis\s+this\s+(?:covid|diabetes|cancer|pneumonia|flu|asthma)\b",
    r"\bis\s+this\s+(?:a\s+)?(?:heart\s+attack|stroke|serious\s+condition)\b",

    r"\bwhat\s+condition\s+is\s+this\b",
    r"\bwhat\s+illness\s+is\s+this\b",
    r"\bwhat\s+disease\s+is\s+this\b",
)


def _normalize(text: str) -> str:
    """Normalize whitespace and case for deterministic matching."""
    return re.sub(r"\s+", " ", (text or "").lower().strip())


def _matches_any(text: str, patterns: tuple[str, ...]) -> bool:
    """Return True if any regular-expression safety pattern matches."""
    return any(re.search(pattern, text) for pattern in patterns)


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

    # Emergency MUST be checked first.
    if _matches_any(normalized, EMERGENCY_PATTERNS):
        return {
            "category": "emergency",
            "is_emergency": True,
            "is_prescription": False,
            "is_diagnosis": False,
            "requires_immediate_redirect": True,
            "reason": "Potential emergency symptoms detected.",
        }

    if _matches_any(normalized, PRESCRIPTION_PATTERNS):
        return {
            "category": "prescription",
            "is_emergency": False,
            "is_prescription": True,
            "is_diagnosis": False,
            "requires_immediate_redirect": False,
            "reason": "Personalized prescription or medication request detected.",
        }

    if _matches_any(normalized, DIAGNOSIS_PATTERNS):
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
    """Return safety classification and boundary metadata."""
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
    """Return True when an emergency safety override is required."""
    result = classify_request(text)

    return bool(
        result["is_emergency"]
        and result["requires_immediate_redirect"]
    )


def emergency_response() -> str:
    """Return deterministic emergency-care guidance."""
    return (
        "This may be a medical emergency and requires immediate attention. "
        "Please seek immediate professional medical care or contact local "
        "emergency services now. This assistant cannot diagnose or treat "
        "medical emergencies."
    )


def apply_safety_override(text: str) -> Optional[str]:
    """
    Return an immediate emergency response when required.

    Returning None means normal safety classification can continue.
    """
    if should_redirect_immediately(text):
        return emergency_response()

    return None


def prescription_refusal_response() -> str:
    """Return deterministic refusal for personalized medication requests."""
    return (
        "I can't prescribe medicines or provide personalized dosage instructions. "
        "Please consult a qualified healthcare professional or pharmacist for "
        "advice about the appropriate medication or dose."
    )


def diagnosis_refusal_response() -> str:
    """Return deterministic refusal for diagnosis requests."""
    return (
        "I can't provide a definitive medical diagnosis. "
        "I can provide general health information, but a qualified healthcare "
        "professional should evaluate your symptoms and provide a diagnosis."
    )


def get_safety_response(text: str) -> Optional[str]:
    """
    Return the deterministic response required by the safety layer.

    Priority:
        emergency > prescription > diagnosis > normal
    """
    override_response = apply_safety_override(text)

    if override_response is not None:
        return override_response

    category = classify_request(text)["category"]

    if category == "prescription":
        return prescription_refusal_response()

    if category == "diagnosis":
        return diagnosis_refusal_response()

    return None