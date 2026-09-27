"""
Medical safety guardrails.

Rules of engagement for the assistant:
  - Never provide a diagnosis. Only suggest a specialty to consult.
  - Never provide or suggest a prescription, dosage, or medication.
  - Always attach a non-diagnostic disclaimer to health-related replies.
  - Detect emergency language and short-circuit straight to an escalation
    message instead of routing through the normal chat/intake flow.
"""
from __future__ import annotations

import re

from ai_core.schemas import SafetyFlag

SYSTEM_PROMPT = """You are the MedNoviAI Healthcare Assistant, a non-diagnostic \
intake and navigation assistant for a doctor-booking platform.

Hard rules you must always follow:
1. You NEVER provide a medical diagnosis. You may only describe symptoms back \
   to the patient and suggest which type of specialist to see.
2. You NEVER recommend, name, or suggest a dosage for any medication or \
   prescription drug, even if asked directly. Redirect to "please discuss \
   medication with a licensed doctor."
3. If the patient describes a medical emergency (e.g. chest pain, difficulty \
   breathing, severe bleeding, stroke symptoms, suicidal ideation, loss of \
   consciousness), you immediately tell them to contact local emergency \
   services or go to the nearest emergency room. Do not continue the normal \
   intake flow.
4. You only reference doctors, specialties, or platform information that is \
   given to you in context. Never invent a doctor's name, qualification, or \
   availability.
5. Every substantive health-related reply ends with a short disclaimer that \
   you are not a substitute for professional medical advice.
6. Keep replies concise, empathetic, and focused on collecting the \
   information needed to route the patient to the right specialist.
"""

NON_DIAGNOSTIC_DISCLAIMER = (
    "This is not a medical diagnosis. Please consult a licensed doctor for "
    "an accurate assessment."
)

EMERGENCY_MESSAGE = (
    "This sounds like it could be a medical emergency. Please contact your "
    "local emergency services immediately or go to the nearest emergency "
    "room. I'm not able to help further with this here."
)

_EMERGENCY_PATTERNS = [
    r"\bchest pain\b",
    r"\bcan'?t breathe\b",
    r"\bdifficulty breathing\b",
    r"\bshortness of breath\b",
    r"\bsevere bleeding\b",
    r"\bunconscious\b",
    r"\bstroke\b",
    r"\bnumb(ness)? (on |in )?(one side|face|arm)\b",
    r"\bsuicid(e|al)\b",
    r"\bkill myself\b",
    r"\bwant to die\b",
    r"\boverdose\b",
    r"\bheart attack\b",
    r"\bseizure\b",
    r"\bnot breathing\b",
    r"\bsevere allergic reaction\b",
    r"\banaphylaxis\b",
]
_EMERGENCY_RE = re.compile("|".join(_EMERGENCY_PATTERNS), re.IGNORECASE)

_PRESCRIPTION_PATTERNS = [
    r"\bwhat (medicine|medication|drug|pill)s? should i take\b",
    r"\bprescribe\b",
    r"\bdosage\b",
    r"\bhow many (mg|milligrams)\b",
]
_PRESCRIPTION_RE = re.compile("|".join(_PRESCRIPTION_PATTERNS), re.IGNORECASE)

_DIAGNOSIS_PATTERNS = [
    r"\bdo i have\b",
    r"\bwhat disease\b",
    r"\bam i (sick|dying)\b",
    r"\bdiagnose me\b",
]
_DIAGNOSIS_RE = re.compile("|".join(_DIAGNOSIS_PATTERNS), re.IGNORECASE)


def evaluate_safety(text: str) -> SafetyFlag:
    """Run all guardrail checks against a single user message."""
    is_emergency = bool(_EMERGENCY_RE.search(text))
    is_prescription_request = bool(_PRESCRIPTION_RE.search(text))
    is_diagnosis_request = bool(_DIAGNOSIS_RE.search(text))

    disclaimer = None
    if is_emergency:
        disclaimer = EMERGENCY_MESSAGE
    elif is_diagnosis_request or is_prescription_request:
        disclaimer = NON_DIAGNOSTIC_DISCLAIMER

    return SafetyFlag(
        is_emergency=is_emergency,
        is_diagnosis_request=is_diagnosis_request,
        is_prescription_request=is_prescription_request,
        disclaimer=disclaimer,
    )
