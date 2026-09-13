import pytest

from src.appointment_assistance.dialogue_policy import (
    PatientDialoguePolicy,
)


def test_dialogue_policy_starts_with_all_fields_missing():
    policy = PatientDialoguePolicy()

    assert policy.get_missing_fields() == [
        "symptoms",
        "symptom_onset",
        "age_group",
    ]

    assert policy.is_ready() is False


def test_first_message_asks_for_symptom_information():
    policy = PatientDialoguePolicy()

    result = policy.process_message("Hello, I need help.")

    assert result.response == "What symptoms are you experiencing?"
    assert result.missing_fields == [
        "symptoms",
        "symptom_onset",
        "age_group",
    ]
    assert result.ready is False
    assert result.handoff is False
    assert result.context is None


def test_existing_symptom_skips_symptom_question():
    policy = PatientDialoguePolicy()

    result = policy.process_message("I have a headache.")

    assert result.response == "When did your symptoms start?"
    assert result.missing_fields == [
        "symptom_onset",
        "age_group",
    ]
    assert result.ready is False
    assert result.handoff is False


def test_multi_turn_dialogue_asks_only_for_missing_information():
    policy = PatientDialoguePolicy()

    result = policy.process_message("I have a headache.")

    assert result.response == "When did your symptoms start?"

    result = policy.process_message("Since yesterday.")

    assert result.response == "What is your age group?"
    assert result.missing_fields == ["age_group"]
    assert result.ready is False
    assert result.handoff is False


def test_multi_turn_dialogue_becomes_ready_after_all_information():
    policy = PatientDialoguePolicy()

    policy.process_message("I have a headache.")
    policy.process_message("Since yesterday.")

    result = policy.process_message("I am an adult.")

    assert result.response == (
        "Thank you. I have collected the required patient "
        "information. The information can now be passed to "
        "the recommendation module."
    )

    assert result.missing_fields == []
    assert result.ready is True
    assert result.handoff is True

    assert result.context == {
        "symptoms": "a headache",
        "symptom_onset": "Since yesterday",
        "age_group": "adult",
    }


def test_all_information_can_be_provided_in_one_message():
    policy = PatientDialoguePolicy()

    result = policy.process_message(
        "I have a headache. Since yesterday. I am an adult."
    )

    assert result.missing_fields == []
    assert result.ready is True
    assert result.handoff is True

    assert result.context == {
        "symptoms": "a headache",
        "symptom_onset": "Since yesterday",
        "age_group": "adult",
    }


def test_policy_preserves_information_between_turns():
    policy = PatientDialoguePolicy()

    policy.process_message("I have a headache.")

    assert policy.state.symptoms == "a headache"
    assert policy.get_missing_fields() == [
        "symptom_onset",
        "age_group",
    ]

    policy.process_message("Since yesterday.")

    assert policy.state.symptoms == "a headache"
    assert policy.state.symptom_onset == "Since yesterday"
    assert policy.get_missing_fields() == ["age_group"]


def test_policy_does_not_handoff_when_information_is_incomplete():
    policy = PatientDialoguePolicy()

    result = policy.process_message(
        "I have a headache. Since yesterday."
    )

    assert result.ready is False
    assert result.handoff is False
    assert result.context is None
    assert result.missing_fields == ["age_group"]


def test_policy_get_context_returns_completed_information():
    policy = PatientDialoguePolicy()

    policy.process_message(
        "I have a headache. Since yesterday. I am an adult."
    )

    assert policy.get_context() == {
        "symptoms": "a headache",
        "symptom_onset": "Since yesterday",
        "age_group": "adult",
    }


def test_policy_get_context_rejects_incomplete_information():
    policy = PatientDialoguePolicy()

    policy.process_message("I have a headache.")

    with pytest.raises(ValueError):
        policy.get_context()


def test_policy_asks_for_age_group_after_symptom_and_onset():
    policy = PatientDialoguePolicy()

    result = policy.process_message(
        "I have a headache. Since yesterday."
    )

    assert result.response == "What is your age group?"
    assert result.missing_fields == ["age_group"]


def test_policy_does_not_ask_for_already_collected_fields():
    policy = PatientDialoguePolicy()

    policy.process_message(
        "I have a headache. Since yesterday. I am an adult."
    )

    assert policy.get_missing_fields() == []
    assert policy.is_ready() is True


def test_natural_follow_up_yesterday_is_understood_as_onset():
    policy = PatientDialoguePolicy()

    result = policy.process_message("I have a headache.")

    assert result.response == "When did your symptoms start?"

    result = policy.process_message("Yesterday.")

    assert result.response == "What is your age group?"
    assert result.missing_fields == ["age_group"]


def test_natural_follow_up_numeric_age_is_converted_to_age_group():
    policy = PatientDialoguePolicy()

    policy.process_message("I have a headache.")
    policy.process_message("Yesterday.")

    result = policy.process_message("I'm 22.")

    assert result.ready is True
    assert result.handoff is True
    assert result.missing_fields == []

    assert result.context == {
        "symptoms": "a headache",
        "symptom_onset": "Yesterday",
        "age_group": "adult",
    }


def test_child_numeric_age_is_detected():
    policy = PatientDialoguePolicy()

    policy.process_message("I have a cough.")
    policy.process_message("Two days ago.")

    result = policy.process_message("I am 10 years old.")

    assert result.ready is True
    assert result.handoff is True
    assert result.context["age_group"] == "child"


def test_teenager_numeric_age_is_detected():
    policy = PatientDialoguePolicy()

    policy.process_message("I have a fever.")
    policy.process_message("Since yesterday.")

    result = policy.process_message("I'm 16.")

    assert result.ready is True
    assert result.handoff is True
    assert result.context["age_group"] == "teenager"


def test_senior_numeric_age_is_detected():
    policy = PatientDialoguePolicy()

    policy.process_message("I have chest discomfort.")
    policy.process_message("Since last night.")

    result = policy.process_message("I am 70 years old.")

    assert result.ready is True
    assert result.handoff is True
    assert result.context["age_group"] == "senior"


def test_information_can_be_provided_across_natural_conversation_turns():
    policy = PatientDialoguePolicy()

    result = policy.process_message(
        "I've been having a headache."
    )

    assert result.response == "When did your symptoms start?"

    result = policy.process_message("Two days ago.")

    assert result.response == "What is your age group?"

    result = policy.process_message("I'm 22.")

    assert result.ready is True
    assert result.handoff is True

    assert result.context == {
        "symptoms": "a headache",
        "symptom_onset": "Two days ago",
        "age_group": "adult",
    }


def test_empty_message_is_rejected():
    policy = PatientDialoguePolicy()

    with pytest.raises(ValueError):
        policy.process_message("")


def test_non_string_message_is_rejected():
    policy = PatientDialoguePolicy()

    with pytest.raises(ValueError):
        policy.process_message(None)