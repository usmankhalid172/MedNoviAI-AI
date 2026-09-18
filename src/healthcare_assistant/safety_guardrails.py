from __future__ import annotations

import re
from typing import Dict, Optional


# Input priority:
# emergency > serious > prescription > treatment > diagnosis > unclear > normal

EMERGENCY_PATTERNS = (
    r"\b(?:severe|crushing|intense|very bad)\s+(?:chest\s+)?pain\b",
    r"\bmy\s+chest\s+(?:hurts|is\s+hurting|really\s+hurts)\b",
    r"\bchest\s+pain\b",
    r"\b(?:can't|cannot|can not|unable to)\s+(?:breathe|breathing)\b",
    r"\b(?:having trouble|struggling|difficulty|hard|hard time)\s+(?:breathing|to breathe)\b",
    r"\bshortness\s+of\s+breath\b",
    r"\bcan['’]?t\s+catch\s+my\s+breath\b",
    r"\bgasping\s+for\s+air\b",
    r"\b(?:heavy|severe|uncontrolled|a lot of|won['’]t\s+stop)\s+(?:bleeding|blood)\b",
    r"\b(?:passed\s+out|passing\s+out|fainted|fainting)\b",
    r"\bloss\s+of\s+consciousness\b",
    r"\bunconscious\b",
    r"\bunresponsive\b",
    r"\bsigns?\s+of\s+(?:a\s+)?stroke\b",
    r"\bstroke\s+symptoms?\b",
    r"\bsudden\s+(?:weakness|numbness)\s+(?:on|in)\s+(?:one|the)\s+(?:side|arm|leg)\b",
    r"\b(?:face\s+drooping|slurred\s+speech|speech\s+is\s+(?:suddenly\s+)?slurred|sudden\s+trouble\s+speaking|sudden\s+speech\s+difficulty)\b",
    r"\bsevere\s+allergic\s+reaction\b",
    r"\banaphylaxis\b",
    r"\b(?:my\s+)?throat\s+(?:is\s+)?swelling\b",
    r"\bswelling\s+(?:of|in)\s+(?:my\s+)?throat\b",
    r"\b(?:lips?|tongue)\s+(?:are|is)\s+swelling\b",
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
    r"\bhow\s+often\s+should\s+i\s+take\s+(?:this|my|the)\s+(?:medicine|medication|drug|antibiotic)\b",
    r"\bshould\s+i\s+(?:increase|decrease|double)\s+my\s+(?:dose|dosage)\b",
    r"\bcan\s+i\s+(?:increase|decrease|double)\s+my\s+(?:dose|dosage)\b",
    r"\bshould\s+i\s+start\s+taking\s+(?:this|my|a|an)\s+(?:medicine|medication|drug|antibiotic)\b",
    r"\bcan\s+i\s+start\s+taking\s+(?:this|my|a|an)\s+(?:medicine|medication|drug|antibiotic)\b",
    r"\bshould\s+i\s+stop\s+(?:taking\s+)?my\s+(?:medicine|medication|drug)\b",
    r"\bcan\s+i\s+stop\s+(?:taking\s+)?my\s+(?:medicine|medication|drug)\b",
    r"\bshould\s+i\s+(?:change|switch)\s+my\s+(?:medicine|medication|drug)\b",
    r"\bcan\s+i\s+(?:change|switch)\s+my\s+(?:medicine|medication|drug)\b",
    r"\bshould\s+i\s+take\s+(?:antibiotics|an\s+antibiotic)\b",
    r"\bprescribe\s+(?:me|a|some)\b",
    r"\bprescribe\s+(?:medicine|medication|a\s+drug)\b",
)

PERSONALIZED_TREATMENT_PATTERNS = (
    r"\bwhat\s+treatment\s+should\s+i\s+(?:personally\s+)?follow\b",
    r"\bwhat\s+treatment\s+should\s+i\s+use\b",
    r"\bwhat\s+treatment\s+is\s+(?:best|appropriate|suitable)\s+for\s+me\b",
    r"\bwhat\s+treatment\s+do\s+i\s+need\b",
    r"\bwhat\s+treatment\s+do\s+i\s+need\s+for\b",
    r"\bhow\s+should\s+i\s+treat\s+(?:this|it|my\s+symptoms?|my\s+condition)\b",
    r"\bhow\s+can\s+i\s+treat\s+(?:this|it|my\s+symptoms?|my\s+condition)\b",
    r"\bwhat\s+should\s+i\s+do\s+to\s+treat\s+(?:this|it|my\s+symptoms?|my\s+condition)\b",
    r"\bwhat\s+should\s+i\s+do\s+to\s+cure\s+(?:this|it|my\s+symptoms?|my\s+condition)\b",
    r"\btell\s+me\s+how\s+to\s+treat\s+(?:this|it|my\s+symptoms?|my\s+condition)\b",
)

DIAGNOSIS_PATTERNS = (
    r"\bdiagnose\s+me\b",
    r"\bcan\s+you\s+diagnose\s+me\b",
    r"\bwhat\s+(?:disease|condition|illness|disorder)\s+do\s+i\s+have\b",
    r"\bwhat(?:'s|\s+is)\s+exactly\s+wrong\s+with\s+me\b",
    r"\bcan\s+you\s+tell\s+me\s+(?:exactly\s+)?what(?:'s|\s+is)\s+wrong\s+with\s+me\b",
    r"\bwhat\s+(?:exactly\s+)?is\s+my\s+diagnosis\b",
    r"\bwhat's\s+my\s+diagnosis\b",
    r"\btell\s+me\s+my\s+diagnosis\b",
    r"\bcan\s+you\s+confirm\s+(?:that\s+)?(?:i\s+have|this\s+is)\b",
    r"\bcan\s+you\s+tell\s+me\s+if\s+i\s+have\b",
    r"\bdo\s+i\s+have\s+(?:covid|diabetes|cancer|pneumonia|flu|asthma)\b",
    r"\bdo\s+i\s+definitely\s+have\b",
    r"\bcould\s+this\s+be\s+(?:a\s+)?(?:disease|condition|illness|infection)\b",
    r"\bcould\s+this\s+be\s+(?:covid|diabetes|cancer|pneumonia|flu|asthma|a\s+heart\s+attack|a\s+stroke)\b",
    r"\bcould\s+(?:these|those)\s+symptoms\s+(?:mean|indicate|suggest)\s+(?:that\s+)?i\s+have\b",
    r"\bmight\s+(?:these|those)\s+symptoms\s+(?:mean|indicate|suggest)\s+(?:that\s+)?i\s+have\b",
    r"\bmay\s+(?:these|those)\s+symptoms\s+(?:mean|indicate|suggest)\s+(?:that\s+)?i\s+have\b",
    r"\bdo\s+these\s+symptoms\s+mean\s+i\s+have\b",
    r"\bis\s+this\s+(?:definitely|really)\s+(?:covid|diabetes|cancer|pneumonia|flu|asthma)\b",
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

UNSAFE_DIAGNOSIS_OUTPUT_PATTERNS = (
    r"\bbased\s+on\s+(?:your|the)\s+symptoms?.{0,80}\byou\s+(?:(?:definitely|probably|likely)\s+)?have\b",
    r"\bfrom\s+what\s+you\s+described.{0,80}\byou\s+(?:(?:definitely|probably|likely)\s+)?have\b",
    r"\byou\s+(?:definitely|probably|likely)\s+have\s+(?:a\s+|an\s+)?[a-z][a-z-]+\b",
    r"\byou\s+are\s+diagnosed\s+with\s+(?:a\s+|an\s+)?[a-z][a-z-]+\b",
    r"\bi\s+diagnose\s+you\s+with\s+(?:a\s+|an\s+)?[a-z][a-z-]+\b",
    r"\byour\s+diagnosis\s+is\s+(?:a\s+|an\s+)?[a-z][a-z-]+\b",
    r"\byou\s+have\s+(?:pneumonia|diabetes|cancer|covid|flu|asthma|a\s+heart\s+attack|a\s+stroke|an?\s+infection)\b",
    r"\bthis\s+(?:is|looks\s+like|appears\s+to\s+be)\s+(?:definitely|probably|likely)?\s*(?:pneumonia|diabetes|cancer|covid|flu|asthma|a\s+heart\s+attack|a\s+stroke)\b",
    r"\byour\s+symptoms?\s+(?:prove|confirm|show)\s+(?:that\s+)?you\s+have\b",
)

UNSAFE_PRESCRIPTION_OUTPUT_PATTERNS = (
    r"\byou\s+should\s+take\s+(?:amoxicillin|azithromycin|ibuprofen|paracetamol|acetaminophen|aspirin|metformin|insulin|prednisone)\b",
    r"\byou\s+need\s+to\s+take\s+(?:amoxicillin|azithromycin|ibuprofen|paracetamol|acetaminophen|aspirin|metformin|insulin|prednisone)\b",
    r"\bi\s+recommend\s+taking\s+(?:amoxicillin|azithromycin|ibuprofen|paracetamol|acetaminophen|aspirin|metformin|insulin|prednisone)\b",
    r"\bstart\s+taking\s+(?:amoxicillin|azithromycin|ibuprofen|paracetamol|acetaminophen|aspirin|metformin|insulin|prednisone)\b",
    r"\byou\s+should\s+take\s+(?:this|the)\s+(?:medicine|medication|drug)\b",
    r"\byou\s+need\s+to\s+take\s+(?:this|the)\s+(?:medicine|medication|drug)\b",
    r"\bstart\s+taking\s+(?:this|the)\s+(?:medicine|medication|drug)\b",
    r"\btake\s+\d+(?:\.\d+)?\s*(?:mg|mcg|g|ml|mL)\s+(?:once|twice|three times|daily|per day)\b",
    r"\b\d+(?:\.\d+)?\s*(?:mg|mcg|g|ml|mL)\s+(?:once|twice|three times|daily|per day)\b",
    r"\bincrease\s+your\s+(?:dose|dosage)\b",
    r"\bdecrease\s+your\s+(?:dose|dosage)\b",
    r"\bstop\s+taking\s+your\s+(?:medicine|medication)\b",
    r"\bstart\s+taking\s+your\s+(?:medicine|medication)\b",
    r"\bswitch\s+your\s+(?:medicine|medication)\b",
)

UNSAFE_TREATMENT_OUTPUT_PATTERNS = (
    r"\byou\s+should\s+follow\s+(?:this|the)\s+treatment\b",
    r"\byou\s+should\s+treat\s+(?:this|it)\s+with\b",
    r"\byou\s+need\s+to\s+treat\s+(?:this|it)\s+with\b",
    r"\bfor\s+your\s+symptoms,?\s+you\s+should\s+(?:use|take|apply|follow|start)\b",
    r"\bfor\s+your\s+condition,?\s+you\s+should\s+(?:use|take|apply|follow|start)\b",
    r"\bi\s+recommend\s+(?:this|the\s+following)\s+treatment\s+for\s+you\b",
)


def _normalize(text: str) -> str:
    """Normalize whitespace and case for deterministic matching."""
    return re.sub(r"\s+", " ", (text or "").lower().strip())


def _matches_any(text: str, patterns: tuple[str, ...]) -> bool:
    """Return True if any configured regex matches."""
    return any(re.search(pattern, text) for pattern in patterns)


def classify_request(text: str) -> Dict[str, Optional[object]]:
    """
    Classify a healthcare input request.

    Priority:
        emergency > serious > prescription > treatment > diagnosis > unclear > normal
    """
    normalized = _normalize(text)

    if not normalized:
        return {
            "category": "normal",
            "is_emergency": False,
            "is_serious": False,
            "is_prescription": False,
            "is_treatment": False,
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
            "is_treatment": False,
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
            "is_treatment": False,
            "is_diagnosis": False,
            "is_unclear": False,
            "requires_immediate_redirect": False,
            "reason": "Potentially serious or urgent symptoms detected.",
        }

    if _matches_any(normalized, PRESCRIPTION_PATTERNS):
        return {
            "category": "prescription",
            "is_emergency": False,
            "is_serious": False,
            "is_prescription": True,
            "is_treatment": False,
            "is_diagnosis": False,
            "is_unclear": False,
            "requires_immediate_redirect": False,
            "reason": "Personalized prescription or medication request detected.",
        }

    if _matches_any(normalized, PERSONALIZED_TREATMENT_PATTERNS):
        return {
            "category": "treatment",
            "is_emergency": False,
            "is_serious": False,
            "is_prescription": False,
            "is_treatment": True,
            "is_diagnosis": False,
            "is_unclear": False,
            "requires_immediate_redirect": False,
            "reason": "Personalized treatment request detected.",
        }

    if _matches_any(normalized, DIAGNOSIS_PATTERNS):
        return {
            "category": "diagnosis",
            "is_emergency": False,
            "is_serious": False,
            "is_prescription": False,
            "is_treatment": False,
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
            "is_treatment": False,
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
        "is_treatment": False,
        "is_diagnosis": False,
        "is_unclear": False,
        "requires_immediate_redirect": False,
        "reason": None,
    }


def check_safety(text: str) -> Dict[str, Optional[object]]:
    """Return safety classification and metadata."""
    result = classify_request(text)

    return {
        "is_emergency": result["is_emergency"],
        "is_serious": result["is_serious"],
        "is_prescription": result["is_prescription"],
        "is_treatment": result["is_treatment"],
        "is_diagnosis": result["is_diagnosis"],
        "is_unclear": result["is_unclear"],
        "category": result["category"],
        "requires_immediate_redirect": result["requires_immediate_redirect"],
        "reason": result["reason"],
    }


def should_redirect_immediately(text: str) -> bool:
    """Return True when emergency escalation is required."""
    result = classify_request(text)

    return bool(
        result["is_emergency"]
        and result["requires_immediate_redirect"]
    )


def emergency_response() -> str:
    """Return immediate emergency-care guidance."""
    return (
        "This may be a medical emergency and requires immediate attention. "
        "Please contact local emergency services or seek immediate professional "
        "medical care from a qualified healthcare professional now. Do not delay "
        "care by relying on this assistant. This assistant cannot diagnose "
        "or treat medical emergencies."
    )


def serious_symptom_response() -> str:
    """Return professional referral guidance for serious symptoms."""
    return (
        "These symptoms may require prompt medical evaluation. "
        "Please contact a qualified healthcare professional for assessment, "
        "especially if the symptoms are worsening, persistent, or concerning."
    )


def prescription_refusal_response() -> str:
    """Return refusal for personalized medication requests."""
    return (
        "I can't prescribe medicines or provide personalized dosage instructions. "
        "Please consult a qualified healthcare professional or pharmacist for "
        "advice about the appropriate medication or dose."
    )


def treatment_refusal_response() -> str:
    """Return refusal for personalized treatment requests."""
    return (
        "I can't choose or provide a personalized treatment plan for you. "
        "I can provide general educational information about treatment options, "
        "but a qualified healthcare professional should assess your situation "
        "and determine appropriate treatment."
    )


def diagnosis_refusal_response() -> str:
    """Return refusal for definitive diagnosis requests."""
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
    """Return emergency response when immediate escalation is required."""
    if should_redirect_immediately(text):
        return emergency_response()

    return None


def contains_unsafe_diagnosis(text: str) -> bool:
    """Detect unsafe personalized diagnostic statements in AI output."""
    normalized = _normalize(text)
    return _matches_any(
        normalized,
        UNSAFE_DIAGNOSIS_OUTPUT_PATTERNS,
    )


def contains_unsafe_prescription(text: str) -> bool:
    """Detect unsafe prescription or dosage advice in AI output."""
    normalized = _normalize(text)
    return _matches_any(
        normalized,
        UNSAFE_PRESCRIPTION_OUTPUT_PATTERNS,
    )


def contains_unsafe_treatment(text: str) -> bool:
    """Detect unsafe personalized treatment instructions in AI output."""
    normalized = _normalize(text)
    return _matches_any(
        normalized,
        UNSAFE_TREATMENT_OUTPUT_PATTERNS,
    )


def classify_ai_output(text: str) -> str:
    """
    Classify an AI-generated response.

    Returns:
        diagnosis
        prescription
        treatment
        safe
    """
    if contains_unsafe_diagnosis(text):
        return "diagnosis"

    if contains_unsafe_prescription(text):
        return "prescription"

    if contains_unsafe_treatment(text):
        return "treatment"

    return "safe"


def validate_ai_response(text: str) -> Dict[str, object]:
    """Validate an AI-generated response against output safety rules."""
    category = classify_ai_output(text)

    return {
        "is_safe": category == "safe",
        "category": category,
        "contains_unsafe_diagnosis": category == "diagnosis",
        "contains_unsafe_prescription": category == "prescription",
        "contains_unsafe_treatment": category == "treatment",
    }


def sanitize_ai_response(text: str) -> str:
    """Replace unsafe AI output with a deterministic safe response."""
    category = classify_ai_output(text)

    if category == "diagnosis":
        return diagnosis_refusal_response()

    if category == "prescription":
        return prescription_refusal_response()

    if category == "treatment":
        return treatment_refusal_response()

    return text


def get_safety_response(text: str) -> Optional[str]:
    """
    Return deterministic input-safety response.

    Priority:
        emergency > serious > prescription > treatment > diagnosis > unclear > normal
    """
    override_response = apply_safety_override(text)

    if override_response is not None:
        return override_response

    category = classify_request(text)["category"]

    if category == "serious":
        return serious_symptom_response()

    if category == "prescription":
        return prescription_refusal_response()

    if category == "treatment":
        return treatment_refusal_response()

    if category == "diagnosis":
        return diagnosis_refusal_response()

    if category == "unclear":
        return unclear_medical_response()

    return None
