from fastapi import APIRouter

from ai_core.llm_client import structured_extraction
from ai_core.safety import EMERGENCY_MESSAGE, NON_DIAGNOSTIC_DISCLAIMER, evaluate_safety
from ai_core.schemas import IntakeRequest, IntakeResponse, PatientIntakeData, SymptomEntry
from ai_core.session_store import get_or_create_session

router = APIRouter(prefix="/api/ai", tags=["intake"])

_EXTRACTION_INSTRUCTIONS = """You extract structured patient intake data from \
free-text messages for a healthcare booking platform. You do NOT diagnose \
anything. Given the patient's latest message and their intake data so far, \
return ONLY a JSON object with this exact shape (merge with, don't discard, \
existing data unless the patient corrects it):

{
  "symptoms": [{"name": str, "duration": str|null, "severity": "mild"|"moderate"|"severe"|"unknown", "notes": str|null}],
  "duration_overall": str|null,
  "context": str|null
}

Only include symptoms and details the patient actually mentioned. Do not \
invent information."""


def _compute_missing_fields(data: PatientIntakeData) -> list[str]:
    missing = []
    if not data.symptoms:
        missing.append("symptoms")
    if not data.duration_overall:
        missing.append("duration_overall")
    return missing


def _follow_up_question(missing: list[str]) -> str | None:
    if "symptoms" in missing:
        return "Could you describe what symptoms you're experiencing?"
    if "duration_overall" in missing:
        return "How long have you been experiencing this?"
    return None


def _build_summary(data: PatientIntakeData) -> str:
    symptom_lines = ", ".join(
        f"{s.name} ({s.severity}, {s.duration or 'duration unknown'})"
        for s in data.symptoms
    )
    return (
        f"Symptoms: {symptom_lines}. "
        f"Overall duration: {data.duration_overall}. "
        f"Context: {data.context or 'none provided'}."
    )


@router.post("/intake", response_model=IntakeResponse)
def intake(request: IntakeRequest) -> IntakeResponse:
    session = get_or_create_session(request.session_id)
    safety = evaluate_safety(request.message)

    if safety.is_emergency:
        return IntakeResponse(
            session_id=request.session_id,
            intake_data=session.intake_data,
            follow_up_question=None,
            safety=safety,
            summary=EMERGENCY_MESSAGE,
        )

    session.add_message("user", request.message)

    messages = [
        {"role": "system", "content": _EXTRACTION_INSTRUCTIONS},
        {
            "role": "user",
            "content": (
                f"Existing intake data so far: "
                f"{session.intake_data.model_dump_json()}\n\n"
                f"Patient's latest message: {request.message}"
            ),
        },
    ]
    extracted = structured_extraction(messages)

    if extracted:
        symptoms = [SymptomEntry(**s) for s in extracted.get("symptoms", [])]
        session.intake_data = PatientIntakeData(
            symptoms=symptoms or session.intake_data.symptoms,
            duration_overall=extracted.get("duration_overall")
            or session.intake_data.duration_overall,
            context=extracted.get("context") or session.intake_data.context,
        )

    missing = _compute_missing_fields(session.intake_data)
    session.intake_data.missing_fields = missing
    session.intake_data.is_complete = not missing

    summary = _build_summary(session.intake_data) if not missing else None
    if summary and safety.disclaimer:
        summary = f"{summary}\n\n{NON_DIAGNOSTIC_DISCLAIMER}"

    return IntakeResponse(
        session_id=request.session_id,
        intake_data=session.intake_data,
        follow_up_question=_follow_up_question(missing),
        safety=safety,
        summary=summary,
    )
