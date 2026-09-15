from src.healthcare_assistant.conversation_flow import process_patient_message
from src.healthcare_assistant.prompts import SYSTEM_PROMPT
from src.healthcare_assistant.symptom_extractor import extract_symptom_data


def test_extract_symptoms_and_duration():
    result = extract_symptom_data("I have fever and cough for 3 days.")

    assert result["symptoms"] == ["fever", "cough"]
    assert result["duration"] == "3 days"


def test_missing_information_does_not_invent_symptoms():
    result = process_patient_message("I don't feel well.")

    assert result.intake.symptoms == []
    assert "symptoms" in result.intake.missing_information
    assert result.next_action == "ask_clarification"


def test_emergency_case_is_escalated():
    result = process_patient_message(
        "I have severe chest pain and difficulty breathing right now."
    )

    assert result.intake.safety_check.is_emergency is True
    assert result.next_action == "emergency_guidance"


def test_normal_case_continues_intake():
    result = process_patient_message("I have fever and cough for 3 days.")

    assert result.intake.safety_check.is_emergency is False
    assert [item.name for item in result.intake.symptoms] == ["fever", "cough"]
    assert result.next_action == "continue_intake"


def test_empty_message_is_rejected():
    try:
        process_patient_message("")
    except ValueError as exc:
        assert "must not be empty" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_system_prompt_has_core_safety_rules():
    assert "Never invent symptoms" in SYSTEM_PROMPT
    assert "Do not provide a definitive diagnosis" in SYSTEM_PROMPT
    assert "Do not prescribe medicines" in SYSTEM_PROMPT
