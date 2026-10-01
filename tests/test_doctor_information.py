from src.doctor_information.context import DoctorConversationContext
from src.doctor_information.intents import (
    DoctorInformationIntent,
    detect_intent,
)
from src.doctor_information.schemas import (
    DoctorInformationResponse,
    DoctorProfile,
    DoctorSchedule,
)
from src.doctor_information.service import DoctorInformationService


def test_profile_intent():
    assert (
        detect_intent("What are this doctor's qualifications?")
        == DoctorInformationIntent.PROFILE
    )


def test_schedule_intent():
    assert (
        detect_intent("What are the doctor's working hours?")
        == DoctorInformationIntent.SCHEDULE
    )


def test_unknown_intent():
    assert detect_intent("Tell me something else") == DoctorInformationIntent.UNKNOWN


def test_profile_lookup_uses_backend_data_only():
    doctor = DoctorProfile(
        doctor_id="DOC-001",
        doctor_name="Dr. Ahmed",
        specialty="Cardiology",
        qualifications=["MBBS", "FCPS"],
    )

    result = DoctorInformationService().process(
        "What are Dr. Ahmed's qualifications?",
        doctor=doctor,
    )

    assert result.information_available is True
    assert result.doctor == doctor
    assert result.doctor.specialty == "Cardiology"


def test_profile_lookup_does_not_invent_missing_data():
    result = DoctorInformationService().process(
        "What are the doctor's qualifications?"
    )

    assert result.information_available is False
    assert result.doctor is None


def test_schedule_lookup_uses_backend_data_only():
    schedule = DoctorSchedule(
        doctor_id="DOC-001",
        doctor_name="Dr. Ahmed",
        schedule={
            "Monday": ["10:00 AM", "2:00 PM"],
            "Wednesday": ["11:00 AM"],
        },
    )

    result = DoctorInformationService().process(
        "When is Dr. Ahmed available?",
        schedule=schedule,
    )

    assert result.information_available is True
    assert result.schedule == schedule
    assert result.schedule.schedule["Monday"] == ["10:00 AM", "2:00 PM"]


def test_schedule_lookup_does_not_invent_availability():
    result = DoctorInformationService().process(
        "When is Dr. Ahmed available?"
    )

    assert result.information_available is False
    assert result.schedule is None


def test_unknown_request_asks_for_clarification():
    result = DoctorInformationService().process("Tell me about the doctor")

    assert result.information_available is False
    assert result.requested_information == "unknown"
    assert "profile or schedule" in result.message


def test_response_rejects_unexpected_fields():
    try:
        DoctorInformationResponse(
            requested_information="profile",
            information_available=True,
            message="ok",
            unexpected_field="should fail",
        )
        assert False
    except Exception:
        assert True


def test_context_stores_active_doctor_after_profile_lookup():
    doctor = DoctorProfile(
        doctor_id="DOC-001",
        doctor_name="Dr. Ahmed",
        specialty="Cardiology",
    )
    context = DoctorConversationContext()

    DoctorInformationService().process(
        "Tell me about Dr. Ahmed's profile",
        doctor=doctor,
        context=context,
    )

    assert context.active_doctor == "Dr. Ahmed"
    assert context.active_doctor_id == "DOC-001"
    assert context.last_intent == "profile"


def test_context_stores_active_doctor_after_schedule_lookup():
    schedule = DoctorSchedule(
        doctor_id="DOC-001",
        doctor_name="Dr. Ahmed",
        schedule={"Monday": ["10:00 AM"]},
    )
    context = DoctorConversationContext()

    DoctorInformationService().process(
        "When is Dr. Ahmed available?",
        schedule=schedule,
        context=context,
    )

    assert context.active_doctor == "Dr. Ahmed"
    assert context.active_doctor_id == "DOC-001"
    assert context.last_intent == "schedule"


def test_unknown_follow_up_uses_active_context():
    context = DoctorConversationContext(
        active_doctor="Dr. Ahmed",
        active_doctor_id="DOC-001",
        last_intent="profile",
    )

    result = DoctorInformationService().process(
        "What else can you tell me?",
        context=context,
    )

    assert result.information_available is False
    assert result.requested_information == "unknown"
    assert "Dr. Ahmed" in result.message


def test_unknown_query_without_context_asks_for_clarification():
    context = DoctorConversationContext()

    result = DoctorInformationService().process(
        "What else can you tell me?",
        context=context,
    )

    assert result.information_available is False
    assert "profile or schedule" in result.message


def test_context_switches_to_new_doctor():
    first_doctor = DoctorProfile(
        doctor_id="DOC-001",
        doctor_name="Dr. Ahmed",
        specialty="Cardiology",
    )
    second_doctor = DoctorProfile(
        doctor_id="DOC-002",
        doctor_name="Dr. Sara",
        specialty="ENT",
    )
    context = DoctorConversationContext()

    service = DoctorInformationService()

    service.process(
        "Tell me about Dr. Ahmed's profile",
        doctor=first_doctor,
        context=context,
    )

    service.process(
        "Tell me about Dr. Sara's profile",
        doctor=second_doctor,
        context=context,
    )

    assert context.active_doctor == "Dr. Sara"
    assert context.active_doctor_id == "DOC-002"

from src.doctor_information.prompts import (
    APPOINTMENT_GUIDANCE_PROMPT,
    DOCTOR_SEARCH_GUIDANCE_PROMPT,
)


def test_doctor_search_prompt_has_frontend_response_contract():
    assert "response_type" in DOCTOR_SEARCH_GUIDANCE_PROMPT
    assert "message" in DOCTOR_SEARCH_GUIDANCE_PROMPT
    assert "next_step" in DOCTOR_SEARCH_GUIDANCE_PROMPT
    assert "requires_backend_data" in DOCTOR_SEARCH_GUIDANCE_PROMPT
    assert "valid JSON only" in DOCTOR_SEARCH_GUIDANCE_PROMPT
    assert "Do not add extra fields" in DOCTOR_SEARCH_GUIDANCE_PROMPT


def test_doctor_search_prompt_enforces_grounded_data():
    assert "Never invent doctors" in DOCTOR_SEARCH_GUIDANCE_PROMPT
    assert "requires_backend_data to true" in DOCTOR_SEARCH_GUIDANCE_PROMPT
    assert "Do not diagnose the patient" in DOCTOR_SEARCH_GUIDANCE_PROMPT


def test_appointment_prompt_has_frontend_response_contract():
    assert "response_type" in APPOINTMENT_GUIDANCE_PROMPT
    assert "message" in APPOINTMENT_GUIDANCE_PROMPT
    assert "next_step" in APPOINTMENT_GUIDANCE_PROMPT
    assert "requires_backend_data" in APPOINTMENT_GUIDANCE_PROMPT
    assert "valid JSON only" in APPOINTMENT_GUIDANCE_PROMPT
    assert "Do not add extra fields" in APPOINTMENT_GUIDANCE_PROMPT


def test_appointment_prompt_enforces_booking_safety():
    assert "Never invent appointment slots" in APPOINTMENT_GUIDANCE_PROMPT
    assert "requested dates and times as patient preferences" in APPOINTMENT_GUIDANCE_PROMPT
    assert "Never claim that an appointment is booked" in APPOINTMENT_GUIDANCE_PROMPT
    assert "requires_backend_data to true" in APPOINTMENT_GUIDANCE_PROMPT

def test_context_preserves_previous_patient_queries():
    context = DoctorConversationContext()
    service = DoctorInformationService()

    service.process(
        "Tell me about Dr. Ahmed",
        context=context,
    )
    service.process(
        "What are his working hours?",
        context=context,
    )

    assert context.previous_queries == [
        "Tell me about Dr. Ahmed",
        "What are his working hours?",
    ]


def test_context_preserves_queries_across_multiple_turns():
    context = DoctorConversationContext()
    service = DoctorInformationService()

    queries = [
        "Tell me about Dr. Ahmed",
        "What is his specialty?",
        "What are his qualifications?",
        "When is he available?",
    ]

    for query in queries:
        service.process(query, context=context)

    assert context.previous_queries == queries


def test_context_preserves_active_doctor_and_query_history():
    doctor = DoctorProfile(
        doctor_id="DOC-001",
        doctor_name="Dr. Ahmed",
        specialty="Cardiology",
    )
    context = DoctorConversationContext()
    service = DoctorInformationService()

    service.process(
        "Tell me about Dr. Ahmed's profile",
        doctor=doctor,
        context=context,
    )
    service.process(
        "What else can you tell me?",
        context=context,
    )

    assert context.active_doctor == "Dr. Ahmed"
    assert context.active_doctor_id == "DOC-001"
    assert context.previous_queries == [
        "Tell me about Dr. Ahmed's profile",
        "What else can you tell me?",
    ]

def test_context_preserves_active_specialty_after_profile_lookup():
    doctor = DoctorProfile(
        doctor_id="DOC-001",
        doctor_name="Dr. Ahmed",
        specialty="Cardiology",
    )
    context = DoctorConversationContext()
    service = DoctorInformationService()

    service.process(
        "Tell me about Dr. Ahmed's profile",
        doctor=doctor,
        context=context,
    )

    assert context.active_doctor == "Dr. Ahmed"
    assert context.active_doctor_id == "DOC-001"
    assert context.active_specialty == "Cardiology"

def test_doctor_display_card_preserves_supported_fields():
    doctor = DoctorProfile(
        doctor_id="DOC-001",
        doctor_name="Dr. Ahmed",
        specialty="Cardiology",
        qualifications=["MBBS", "FCPS"],
        experience="10 years",
        clinic="City Hospital",
        address="Main Road",
        consultation_fee="3000 PKR",
    )

    result = DoctorInformationService().process(
        "Tell me about Dr. Ahmed's profile",
        doctor=doctor,
    )

    assert result.doctor == doctor
    assert result.doctor.doctor_id == "DOC-001"
    assert result.doctor.doctor_name == "Dr. Ahmed"
    assert result.doctor.specialty == "Cardiology"
    assert result.doctor.qualifications == ["MBBS", "FCPS"]
    assert result.doctor.experience == "10 years"
    assert result.doctor.clinic == "City Hospital"
    assert result.doctor.address == "Main Road"
    assert result.doctor.consultation_fee == "3000 PKR"


def test_doctor_display_card_rejects_unsupported_fields():
    try:
        DoctorProfile(
            doctor_id="DOC-001",
            doctor_name="Dr. Ahmed",
            specialty="Cardiology",
            rating=4.8,
        )
        assert False
    except Exception:
        assert True

def test_doctor_search_prompt_locks_display_card_contract():
    locked_fields = [
        "doctor_id",
        "doctor_name",
        "specialty",
        "qualifications",
        "experience",
        "clinic",
        "address",
        "consultation_fee",
    ]

    assert "The doctor display-card contract is locked" in DOCTOR_SEARCH_GUIDANCE_PROMPT
    assert "Preserve these field names exactly as defined by the backend schema" in DOCTOR_SEARCH_GUIDANCE_PROMPT
    assert "must not introduce frontend-only fields" in DOCTOR_SEARCH_GUIDANCE_PROMPT

    for field in locked_fields:
        assert field in DOCTOR_SEARCH_GUIDANCE_PROMPT

def test_doctor_search_prompt_separates_profile_and_schedule_data():
    assert "Keep doctor profile fields separate from schedule, availability" in DOCTOR_SEARCH_GUIDANCE_PROMPT
    assert "Only display schedule or appointment availability when explicitly supplied" in DOCTOR_SEARCH_GUIDANCE_PROMPT
    assert "Never present a patient's preferred date or time as a confirmed slot" in DOCTOR_SEARCH_GUIDANCE_PROMPT

def test_appointment_prompt_keeps_slots_associated_with_backend_doctor():
    assert "doctor identity" in APPOINTMENT_GUIDANCE_PROMPT
    assert "Do not reassign appointment slots between doctors" in APPOINTMENT_GUIDANCE_PROMPT
    assert "Do not combine appointment slots from different doctors" in APPOINTMENT_GUIDANCE_PROMPT

def test_doctor_guidance_prompts_do_not_expose_internal_information():
    protected_phrases = (
        "system instructions",
        "internal prompts",
        "API keys",
        "credentials",
        "private system information",
    )

    for phrase in protected_phrases:
        assert phrase in DOCTOR_SEARCH_GUIDANCE_PROMPT
        assert phrase in APPOINTMENT_GUIDANCE_PROMPT

def test_doctor_search_prompt_prevents_unsupported_card_fields():
    assert "Do not rename, invent, infer, calculate, derive, or add doctor profile" in DOCTOR_SEARCH_GUIDANCE_PROMPT
    assert "must not introduce frontend-only fields" in DOCTOR_SEARCH_GUIDANCE_PROMPT