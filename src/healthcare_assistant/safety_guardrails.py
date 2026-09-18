from __future__ import annotations

import re
from typing import Dict, Optional


# Input safety priority:
# emergency > serious > prescription > diagnosis > unclear > normal

EMERGENCY_PATTERNS = (
    r"\b(?:severe|crushing|intense|very bad)\s+(?:chest\s+)?pain\b",
    r"\bmy\s+chest\s+(?:hurts|is\s+hurting|really\s+hurts)\b",
    r"\bchest\s+pain\b",
    r"\b(?:can't|cannot|can not|unable to)\s+(?:breathe|breathing)\b",
    r"\b(?:having trouble|struggling|difficulty|hard|hard time)\s+(?:breathing|to breathe)\b",
    r"\bshortness\s+of\s+breath\b",
    r"\bcan['’]?t\s+catch\s+my\s+breath\b",
    r"\b(?:heavy|severe|uncontrolled|a lot of)\s+(?:bleeding|blood)\b",
    r"\b(?:i\s+)?(?:passed|passing)\s+out\b",
    r"\bloss\s+of\s+consciousness\b",
    r"\bunconscious\b",
    r"\bsigns?\s+of\s+(?:a\s+)?stroke\b",
    r"\bstroke\s+symptoms?\b",
    r"\bsevere\s+allergic\s+reaction\b",
    r"\b(?:my\s+)?throat\s+(?:is\s+)?swelling\b",
    r"\bswelling\s+(?:of|in)\s+(?:my\s+)?throat\b",
    r"\bhaving\s+a\s+seizure\b",
    r"\bseizure\b",
)


SERIOUS_SYMPTOM_PATTERNS = (
    r"\bmy\s+symptoms?\s+(?:are\s+)?getting\s+worse\b",
    r"\bsymptoms?\s+(?:are\s+)?getting\s+worse\b",
    r"\bsymptoms?\s+(?:are\s+)?worsening\b",
    r"\bgetting\s+worse\s+(?:quickly|rapidly)\b",
    r"\brapidly\s+worsening\s+symptoms?\b",
    r"\bpersistent\s+(?:and\s+)?(?:concerning\s+)?symptoms?\b",
    r"\bpersistent\s+severe\s+fever\b",
    r"\bsevere\s+fever\s+(?:for|lasting)\b",
    r"\bpersistent\s+(?:or\s+)?repeated\s+vomiting\b",
    r"\bsevere\s+weakness\b",
    r"\bsevere\s+pain\s+(?:that\s+)?(?:isn't|is\s+not)\s+improving\b",
    r"\bpain\s+(?:that\s+)?(?:isn't|is\s+not)\s+improving\b",
)


PRESCRIPTION_PATTERNS = (
    r"\bwhat\s+(?:medicine|medication|drug)\s+should\s+i\s+(?:take|use)\b",
    r"\bwhich\s+(?:medicine|medication|drug)\s+(?:should|can|could)\s+i\s+(?:take|use)\b",
    r"\bwhat\s+antibiotic\s+(?:should|can|could)\s+i\s+take\b",
    r"\bwhich\s+antibiotic\s+(?:should|can|could)\s+i\s+take\b",
    r"\bwhich\s+(?:medicine|medication|drug|antibiotic)\s+would\s+be\s+(?:appropriate|best|suitable)\s+for\s+me\b",
    r"\bwhat\s+(?:medicine|medication|drug|antibiotic)\s+would\s+be\s+(?:appropriate|best|suitable)\s+for\s+me\b",
    r"\bwhich\s+(?:medicine|medication|drug|antibiotic)\s+is\s+(?:best|appropriate|suitable)\s+for\s+me\b",
    r"\bwhat\s+(?:medicine|medication|drug|antibiotic)\s+is\s+(?:best|appropriate|suitable)\s+for\s+me\b",
    r"\bwhat\s+should\s+i\s+take\s+for\b",
    r"\bwhat\s+can\s+i\s+take\s+for\b",
    r"\bwhat\s+medicine\s+can\s+i\s+take\s+for\b",
    r"\bwhat\s+(?:dose|dosage)\s+should\s+i\s+(?:take|use)\b",
    r"\bhow\s+much\s+(?:medicine|medication|of\s+this)\s+should\s+i\s+take\b",
    r"\bhow\s+many\s+(?:mg|milligrams|tablets|pills)\s+should\s+i\s+take\b",
    r"\bshould\s+i\s+(?:increase|decrease|double)\s+my\s+(?:dose|dosage)\b",
    r"\bcan\s+i\s+(?:increase|decrease|double)\s+my\s+(?:dose|dosage)\b",
    r"\bshould\s+i\s+stop\s+(?:taking\s+)?my\s+(?:medicine|medication)\b",
    r"\bcan\s+i\s+stop\s+(?:taking\s+)?my\s+(?:medicine|medication)\b",
    r"\bshould\s+i\s+(?:change|switch)\s+my\s+(?:medicine|medication)\b",
    r"\bcan\s+i\s+(?:change|switch)\s+my\s+(?:medicine|medication)\b",
    r"\bprescribe\s+(?:me|a|some)\b",
    r"\bprescribe\s+(?:medicine|medication|a\s+drug)\b",
)


DIAGNOSIS_PATTERNS = (
    r"\bdiagnose\s+me\b",
    r"\bwhat\s+(?:disease|condition|illness|disorder)\s+do\s+i\s+have\b",
    r"\bwhat\s+is\s+my\s+diagnosis\b",
    r"\btell\s+me\s+my\s+diagnosis\b",
    r"\bdo\s+i\s+have\s+(?:covid|diabetes|cancer|pneumonia|flu|asthma)\b",
    r"\bdo\s+i\s+definitely\s+have\b",
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


UNCLEAR_MEDICAL_PATTERNS = (
    r"\bi\s+(?:don't|do\s+not)\s+know\s+what(?:'s| is)\s+wrong\b",
    r"\bi['’]?m\s+not\s+sure\s+what(?:'s| is)\s+wrong\b",
    r"\bi\s+(?:don't|do\s+not)\s+know\s+what\s+these\s+symptoms\s+mean\b",
    r"\bi\s+can['’]?t\s+tell\s+what(?:'s| is)\s+causing\s+this\b",
    r"\bsomething\s+feels\s+wrong\b",
    r"\bi\s+feel\s+very\s+unwell\b",
    r"\bi\s+feel\s+strange\s+and\s+don't\s+know\s+(?:what|why)\b",
    r"\bi\s+feel\s+strange\s+and\s+do\s+not\s+know\s+(?:what|why)\b",
)


# Output validation:
# These patterns look for personalized, unsafe conclusions in AI-generated text.

UNSAFE_DIAGNOSIS_OUTPUT_PATTERNS = (
    r"\bbased\s+on\s+(?:your|the)\s+symptoms?.{0,80}\byou\s+(?:definitely\s+)?have\b",
    r"\bfrom\s+what\s+you\s+described.{0,80}\byou\s+(?:definitely\s+)?have\b",
    r"\byou\s+definitely\s+have\s+(?:a\s+|an\s+)?[a-z][a-z-]+\b",
    r"\byou\s+are\s+diagnosed\s+with\s+(?:a\s+|an\s+)?[a-z][a-z-]+\b",
    r"\bi\s+diagnose\s+you\s+with\s+(?:a\s+|an\s+)?[a-z][a-z-]+\b",
    r"\byour\s+diagnosis\s+is\s+(?:a\s+|an\s+)?[a-z][a-z-]+\b",
    r"\byou\s+have\s+(?:pneumonia|diabetes|cancer|covid|flu|asthma|a\s+heart\s+attack|a\s+stroke|an?\s+infection)\b",
    r"\bthis\s+(?:is|looks\s+like|appears\s+to\s+be)\s+(?:definitely\s+)?(?:pneumonia|diabetes|cancer|covid|flu|asthma|a\s+heart\s+attack|a\s+stroke)\b",
)


UNSAFE_PRESCRIPTION_OUTPUT_PATTERNS = (
    r"\byou\s+should\s+take\s+(?:the\s+)?[a-z][a-z-]+\b",
    r"\byou\s+need\s+to\s+take\s+(?:the\s+)?[a-z][a-z-]+\b",
    r"\bi\s+recommend\s+taking\s+(?:the\s+)?[a-z][a-z-]+\b",
    r"\bstart\s+taking\s+(?:the\s+)?[a-z][a-z-]+\b",
    r"\btake\s+(?:the\s+)?(?:amoxicillin|azithromycin|ibuprofen|paracetamol|acetaminophen|aspirin|metformin|insulin|prednisone)\b",
    r"\b\d+(?:\.\d+)?\s*(?:mg|mcg|g|ml|mL)\s+(?:once|twice|three times|daily|per day)\b",
    r"\btake\b.{0,60}\b\d+(?:\.\d+)?\s*(?:mg|mcg|g|ml|mL)\b",
    r"\bincrease\s+your\s+(?:dose|dosage)\b",
    r"\bdecrease\s+your\s+(?:dose|dosage)\b",
    r"\bstop\s+taking\s+your\s+(?:medicine|medication)\b",
    r"\bstart\s+taking\s+your\s+(?:medicine|medication)\b",
)


def _normalize(text: str) -> str:
    """Normalize whitespace and case for deterministic matching."""
    return re.sub(r"\s+", " ", (text or "").lower().strip())


def _matches_any(text: str, patterns: tuple[str, ...]) -> bool:
    """Return True when at least one regex pattern matches."""
    return any(re.search(pattern, text) for pattern in patterns)


def classify_request(text: str) -> Dict[str, Optional[object]]:
    """
    Classify a healthcare input request.

    Priority:
        emergency > serious > prescription > diagnosis > unclear > normal
    """
    normalized = _normalize(text)

    if not normalized:
        return {
            "category": "normal",
            "is_emergency": False,
            "is_serious": False,
            "is_prescription": False,
            "is_diagnosis": False,
            "is_unclear": False,
            "requires_immediate_redirect": False,
            "reason": None,
        }

    if _matches_any(normalized, EMERGENCY_PATTERNS):
        return {
            "category": "emergency",
            "is_emergency": True,
            "is_serious": False,
            "is_prescription": False,
            "is_diagnosis": False,
            "is_unclear": False,
            "requires_immediate_redirect": True,
            "reason": "Potential emergency symptoms detected.",
        }

    if _matches_any(normalized, SERIOUS_SYMPTOM_PATTERNS):
        return {
            "category": "serious",
            "is_emergency": False,
            "is_serious": True,
            "is_prescription": False,
            "is_diagnosis": False,
            "is_unclear": False,
            "requires_immediate_redirect": False,
            "reason": "Potentially serious or worsening symptoms detected.",
        }

    if _matches_any(normalized, PRESCRIPTION_PATTERNS):
        return {
            "category": "prescription",
            "is_emergency": False,
            "is_serious": False,
            "is_prescription": True,
            "is_diagnosis": False,
            "is_unclear": False,
            "requires_immediate_redirect": False,
            "reason": "Personalized prescription or medication request detected.",
        }

    if _matches_any(normalized, DIAGNOSIS_PATTERNS):
        return {
            "category": "diagnosis",
            "is_emergency": False,
            "is_serious": False,
            "is_prescription": False,
            "is_diagnosis": True,
            "is_unclear": False,
            "requires_immediate_redirect": False,
            "reason": "Diagnosis request detected.",
        }

    if _matches_any(normalized, UNCLEAR_MEDICAL_PATTERNS):
        return {
            "category": "unclear",
            "is_emergency": False,
            "is_serious": False,
            "is_prescription": False,
            "is_diagnosis": False,
            "is_unclear": True,
            "requires_immediate_redirect": False,
            "reason": "Unclear medical query detected.",
        }

    return {
        "category": "normal",
        "is_emergency": False,
        "is_serious": False,
        "is_prescription": False,
        "is_diagnosis": False,
        "is_unclear": False,
        "requires_immediate_redirect": False,
        "reason": None,
    }


def check_safety(text: str) -> Dict[str, Optional[object]]:
    """Return safety classification and boundary metadata."""
    result = classify_request(text)

    return {
        "is_emergency": result["is_emergency"],
        "is_serious": result["is_serious"],
        "is_prescription": result["is_prescription"],
        "is_diagnosis": result["is_diagnosis"],
        "is_unclear": result["is_unclear"],
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
    """Return immediate professional/emergency care guidance."""
    return (
        "This may be a medical emergency and requires immediate attention. "
        "Please seek immediate professional medical care or contact local "
        "emergency services now. This assistant cannot diagnose or treat "
        "medical emergencies."
    )


def serious_symptom_response() -> str:
    """Return referral guidance for potentially serious symptoms."""
    return (
        "These symptoms may require prompt medical evaluation. "
        "Please contact a qualified healthcare professional for assessment, "
        "especially if the symptoms are worsening, persistent, or concerning."
    )


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


def unclear_medical_response() -> str:
    """Return safe fallback for unclear medical questions."""
    return (
        "I can't determine the cause of your symptoms from the available "
        "information alone. I can provide general health information, but a "
        "qualified healthcare professional should evaluate symptoms that are "
        "concerning, persistent, or worsening."
    )


def apply_safety_override(text: str) -> Optional[str]:
    """Return the immediate emergency response when an emergency is detected."""
    if should_redirect_immediately(text):
        return emergency_response()

    return None


def contains_unsafe_diagnosis(text: str) -> bool:
    """Detect personalized diagnostic statements in generated AI output."""
    normalized = _normalize(text)
    return _matches_any(normalized, UNSAFE_DIAGNOSIS_OUTPUT_PATTERNS)


def contains_unsafe_prescription(text: str) -> bool:
    """Detect personalized prescription or dosage advice in generated output."""
    normalized = _normalize(text)
    return _matches_any(normalized, UNSAFE_PRESCRIPTION_OUTPUT_PATTERNS)


def classify_ai_output(text: str) -> str:
    """
    Classify generated output for response-level safety validation.

    Returns:
        "diagnosis"    unsafe personalized diagnosis
        "prescription" unsafe personalized medication advice
        "safe"         no detected output violation
    """
    if contains_unsafe_diagnosis(text):
        return "diagnosis"

    if contains_unsafe_prescription(text):
        return "prescription"

    return "safe"


def validate_ai_response(text: str) -> Dict[str, object]:
    """Return deterministic validation metadata for an AI-generated response."""
    category = classify_ai_output(text)

    return {
        "is_safe": category == "safe",
        "category": category,
        "contains_unsafe_diagnosis": category == "diagnosis",
        "contains_unsafe_prescription": category == "prescription",
    }


def sanitize_ai_response(text: str) -> str:
    """
    Replace unsafe generated responses with the appropriate safety response.

    Safe responses are returned unchanged.
    """
    category = classify_ai_output(text)

    if category == "diagnosis":
        return diagnosis_refusal_response()

    if category == "prescription":
        return prescription_refusal_response()

    return text


def get_safety_response(text: str) -> Optional[str]:
    """
    Return the deterministic response required by the input safety layer.

    Priority:
        emergency > serious > prescription > diagnosis > unclear > normal
    """
    override_response = apply_safety_override(text)

    if override_response is not None:
        return override_response

    category = classify_request(text)["category"]

    if category == "serious":
        return serious_symptom_response()

    if category == "prescription":
        return prescription_refusal_response()

    if category == "diagnosis":
        return diagnosis_refusal_response()

    if category == "unclear":
        return unclear_medical_response()

    return None