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