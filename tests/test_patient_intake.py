import pytest

from src.appointment_assistance.patient_intake import (
    PatientIntakeCollector,
)


def test_intake_starts_empty():
    collector = PatientIntakeCollector()

    assert collector.info.symptoms is None
    assert collector.info.symptom_onset is None
    assert collector.info.age_group is None
    assert collector.info.secondary_history is None
    assert collector.info.additional_details is None


def test_intake_starts_with_required_fields_missing():
    collector = PatientIntakeCollector()

    assert collector.missing_fields() == [
        "symptoms",
        "symptom_onset",
        "age_group",
    ]


def test_collector_stores_primary_complaint():
    collector = PatientIntakeCollector()

    collector.update(symptoms="headache")

    assert collector.info.symptoms == "headache"


def test_collector_stores_onset_and_age_group():
    collector = PatientIntakeCollector()

    collector.update(
        symptom_onset="since yesterday",
        age_group="adult",
    )

    assert collector.info.symptom_onset == "since yesterday"
    assert collector.info.age_group == "adult"


def test_collector_stores_optional_secondary_history():
    collector = PatientIntakeCollector()

    collector.update(
        secondary_history="Previous history of asthma",
    )

    assert collector.info.secondary_history == (
        "Previous history of asthma"
    )


def test_collector_stores_optional_additional_details():
    collector = PatientIntakeCollector()

    collector.update(
        additional_details="Pain becomes worse at night",
    )

    assert collector.info.additional_details == (
        "Pain becomes worse at night"
    )


def test_optional_fields_do_not_appear_in_missing_required_fields():
    collector = PatientIntakeCollector()

    collector.update(
        secondary_history="Previous history of asthma",
        additional_details="Pain becomes worse at night",
    )

    assert collector.missing_fields() == [
        "symptoms",
        "symptom_onset",
        "age_group",
    ]


def test_missing_fields_are_updated_after_each_turn():
    collector = PatientIntakeCollector()

    collector.update(symptoms="headache")

    assert collector.missing_fields() == [
        "symptom_onset",
        "age_group",
    ]

    collector.update(symptom_onset="since yesterday")

    assert collector.missing_fields() == [
        "age_group",
    ]


def test_intake_becomes_ready_when_all_required_information_is_collected():
    collector = PatientIntakeCollector()

    collector.update(
        symptoms="headache",
        symptom_onset="since yesterday",
        age_group="adult",
    )

    assert collector.missing_fields() == []
    assert collector.is_ready() is True


def test_intake_is_ready_without_optional_information():
    collector = PatientIntakeCollector()

    collector.update(
        symptoms="headache",
        symptom_onset="since yesterday",
        age_group="adult",
    )

    assert collector.info.secondary_history is None
    assert collector.info.additional_details is None
    assert collector.is_ready() is True


def test_optional_information_does_not_affect_readiness():
    collector = PatientIntakeCollector()

    collector.update(
        symptoms="headache",
        symptom_onset="since yesterday",
        age_group="adult",
        secondary_history="No previous medical history",
        additional_details="Mild pain",
    )

    assert collector.is_ready() is True
    assert collector.missing_fields() == []


def test_update_ignores_empty_values():
    collector = PatientIntakeCollector()

    collector.update(
        symptoms="headache",
        age_group="adult",
    )

    collector.update(
        symptoms="",
        age_group="",
        secondary_history="",
        additional_details="",
    )

    assert collector.info.symptoms == "headache"
    assert collector.info.age_group == "adult"
    assert collector.info.secondary_history is None
    assert collector.info.additional_details is None


def test_next_question_starts_with_symptoms():
    collector = PatientIntakeCollector()

    assert collector.next_question() == (
        "What symptoms are you experiencing?"
    )


def test_next_question_asks_for_symptom_onset():
    collector = PatientIntakeCollector()

    collector.update(symptoms="headache")

    assert collector.next_question() == (
        "When did your symptoms start?"
    )


def test_next_question_asks_for_age_group():
    collector = PatientIntakeCollector()

    collector.update(
        symptoms="headache",
        symptom_onset="since yesterday",
    )

    assert collector.next_question() == (
        "What is your age group?"
    )


def test_next_question_returns_none_when_required_fields_are_ready():
    collector = PatientIntakeCollector()

    collector.update(
        symptoms="headache",
        symptom_onset="since yesterday",
        age_group="adult",
    )

    assert collector.next_question() is None


def test_extracts_primary_complaint_from_message():
    collector = PatientIntakeCollector()

    collector.extract_from_message("I have a headache.")

    assert collector.info.symptoms == "a headache"


def test_extracts_symptom_onset_from_message():
    collector = PatientIntakeCollector()

    collector.extract_from_message("Since yesterday.")

    assert collector.info.symptom_onset == "Since yesterday"


def test_extracts_age_group_from_message():
    collector = PatientIntakeCollector()

    collector.extract_from_message("I am an adult.")

    assert collector.info.age_group == "adult"


def test_extracts_multiple_required_fields_from_one_message():
    collector = PatientIntakeCollector()

    collector.extract_from_message(
        "I have a headache. Since yesterday. I am an adult."
    )

    assert collector.info.symptoms == "a headache"
    assert collector.info.symptom_onset == "Since yesterday"
    assert collector.info.age_group == "adult"


def test_process_message_asks_for_missing_information():
    collector = PatientIntakeCollector()

    result = collector.process_message("I have a headache.")

    assert result.response == "When did your symptoms start?"
    assert result.missing_fields == [
        "symptom_onset",
        "age_group",
    ]
    assert result.ready is False
    assert result.context is None


def test_process_message_keeps_information_between_turns():
    collector = PatientIntakeCollector()

    result = collector.process_message("I have a headache.")

    assert result.response == "When did your symptoms start?"

    result = collector.process_message("Since yesterday.")

    assert result.response == "What is your age group?"
    assert result.missing_fields == ["age_group"]
    assert result.ready is False
    assert result.context is None


def test_process_message_completes_after_multiple_turns():
    collector = PatientIntakeCollector()

    collector.process_message("I have a headache.")
    collector.process_message("Since yesterday.")

    result = collector.process_message("I am an adult.")

    assert result.response == (
        "Thank you. I have collected the required patient "
        "information. The information can now be passed to "
        "the recommendation module."
    )
    assert result.missing_fields == []
    assert result.ready is True

    assert result.context == {
        "primary_complaint": "a headache",
        "symptom_onset": "Since yesterday",
        "age_group": "adult",
        "secondary_history": None,
        "additional_details": None,
    }


def test_process_message_handles_all_required_information_in_one_turn():
    collector = PatientIntakeCollector()

    result = collector.process_message(
        "I have a headache. Since yesterday. I am an adult."
    )

    assert result.ready is True
    assert result.missing_fields == []

    assert result.context == {
        "primary_complaint": "a headache",
        "symptom_onset": "Since yesterday",
        "age_group": "adult",
        "secondary_history": None,
        "additional_details": None,
    }


def test_get_context_returns_standardized_patient_information():
    collector = PatientIntakeCollector()

    collector.update(
        symptoms="headache",
        symptom_onset="since yesterday",
        age_group="adult",
    )

    context = collector.get_context()

    assert context == {
        "primary_complaint": "headache",
        "symptom_onset": "since yesterday",
        "age_group": "adult",
        "secondary_history": None,
        "additional_details": None,
    }


def test_get_context_includes_optional_information_when_available():
    collector = PatientIntakeCollector()

    collector.update(
        symptoms="headache",
        symptom_onset="since yesterday",
        age_group="adult",
        secondary_history="No previous history of migraine",
        additional_details="Pain is worse in the morning",
    )

    context = collector.get_context()

    assert context == {
        "primary_complaint": "headache",
        "symptom_onset": "since yesterday",
        "age_group": "adult",
        "secondary_history": "No previous history of migraine",
        "additional_details": "Pain is worse in the morning",
    }


def test_get_context_rejects_incomplete_required_information():
    collector = PatientIntakeCollector()

    collector.update(
        symptoms="headache",
        symptom_onset="since yesterday",
    )

    try:
        collector.get_context()
        assert False
    except ValueError:
        assert True


# ---------------------------------------------------------
# Sep 11: Finalized dialogue and structured patient data
# ---------------------------------------------------------


def test_process_message_sets_handoff_false_when_intake_is_incomplete():
    collector = PatientIntakeCollector()

    result = collector.process_message("I have a headache.")

    assert result.ready is False
    assert result.handoff is False
    assert result.context is None


def test_process_message_sets_handoff_true_when_intake_is_complete():
    collector = PatientIntakeCollector()

    result = collector.process_message(
        "I have a headache. Since yesterday. I am an adult."
    )

    assert result.ready is True
    assert result.handoff is True
    assert result.context is not None


def test_extracts_natural_symptom_statement():
    collector = PatientIntakeCollector()

    collector.extract_from_message(
        "I've been having a headache."
    )

    assert collector.info.symptoms == "a headache"


def test_extracts_yesterday_as_symptom_onset():
    collector = PatientIntakeCollector()

    collector.extract_from_message("Yesterday.")

    assert collector.info.symptom_onset == "Yesterday"


def test_extracts_two_days_ago_as_symptom_onset():
    collector = PatientIntakeCollector()

    collector.extract_from_message("Two days ago.")

    assert collector.info.symptom_onset == "Two days ago"


def test_extracts_numeric_adult_age_group():
    collector = PatientIntakeCollector()

    collector.extract_from_message("I'm 22.")

    assert collector.info.age_group == "adult"


def test_extracts_numeric_child_age_group():
    collector = PatientIntakeCollector()

    collector.extract_from_message("I am 10 years old.")

    assert collector.info.age_group == "child"


def test_extracts_numeric_teenager_age_group():
    collector = PatientIntakeCollector()

    collector.extract_from_message("I am 16 years old.")

    assert collector.info.age_group == "teenager"


def test_extracts_numeric_senior_age_group():
    collector = PatientIntakeCollector()

    collector.extract_from_message("I am 70 years old.")

    assert collector.info.age_group == "senior"


def test_processes_natural_multi_turn_patient_dialogue():
    collector = PatientIntakeCollector()

    result = collector.process_message(
        "I've been having a headache."
    )

    assert result.ready is False
    assert result.response == "When did your symptoms start?"

    result = collector.process_message("Two days ago.")

    assert result.ready is False
    assert result.response == "What is your age group?"

    result = collector.process_message("I'm 22.")

    assert result.ready is True
    assert result.handoff is True
    assert result.missing_fields == []

    assert result.context == {
        "primary_complaint": "a headache",
        "symptom_onset": "Two days ago",
        "age_group": "adult",
        "secondary_history": None,
        "additional_details": None,
    }


def test_structured_patient_data_includes_optional_information():
    collector = PatientIntakeCollector()

    collector.update(
        symptoms="headache",
        symptom_onset="yesterday",
        age_group="adult",
        secondary_history="History of migraine",
        additional_details="Pain is worse in the morning",
    )

    result = collector.process_message(
        "I am an adult."
    )

    assert result.ready is True
    assert result.handoff is True

    assert result.context == {
        "primary_complaint": "headache",
        "symptom_onset": "yesterday",
        "age_group": "adult",
        "secondary_history": "History of migraine",
        "additional_details": "Pain is worse in the morning",
    }

    # ---------------------------------------------------------
# Sep 13: Finalized multi-turn intake and backend handoff
# ---------------------------------------------------------


def test_short_follow_up_answer_is_used_for_symptom_onset():
    collector = PatientIntakeCollector()

    collector.process_message("I have a headache.")

    result = collector.process_message("Yesterday")

    assert result.ready is False
    assert result.missing_fields == ["age_group"]
    assert collector.info.symptom_onset == "Yesterday"


def test_short_follow_up_answer_is_used_for_age_group():
    collector = PatientIntakeCollector()

    collector.process_message("I have a headache.")
    collector.process_message("Yesterday")

    result = collector.process_message("Adult")

    assert result.ready is True
    assert result.handoff is True
    assert collector.info.age_group == "adult"


def test_numeric_follow_up_answer_is_converted_to_age_group():
    collector = PatientIntakeCollector()

    collector.process_message("I have a headache.")
    collector.process_message("Two days ago.")

    result = collector.process_message("22")

    assert result.ready is True
    assert result.handoff is True
    assert collector.info.age_group == "adult"


def test_follow_up_question_changes_after_each_collected_field():
    collector = PatientIntakeCollector()

    result = collector.process_message("I have a fever.")

    assert result.response == "When did your symptoms start?"

    result = collector.process_message("Since yesterday.")

    assert result.response == "What is your age group?"

    result = collector.process_message("I am an adult.")

    assert result.ready is True
    assert result.response == (
        "Thank you. I have collected the required patient "
        "information. The information can now be passed to "
        "the recommendation module."
    )


def test_backend_record_returns_standardized_storage_structure():
    collector = PatientIntakeCollector()

    collector.update(
        symptoms="headache",
        symptom_onset="since yesterday",
        age_group="adult",
    )

    record = collector.get_backend_record()

    assert record == {
        "primary_complaint": "headache",
        "symptom_onset": "since yesterday",
        "age_group": "adult",
        "secondary_history": None,
        "additional_details": None,
    }


def test_backend_record_includes_optional_information():
    collector = PatientIntakeCollector()

    collector.update(
        symptoms="headache",
        symptom_onset="since yesterday",
        age_group="adult",
        secondary_history="History of migraine",
        additional_details="Pain is worse at night",
    )

    assert collector.get_backend_record() == {
        "primary_complaint": "headache",
        "symptom_onset": "since yesterday",
        "age_group": "adult",
        "secondary_history": "History of migraine",
        "additional_details": "Pain is worse at night",
    }


def test_backend_record_rejects_incomplete_intake():
    collector = PatientIntakeCollector()

    collector.update(symptoms="headache")

    with pytest.raises(ValueError):
        collector.get_backend_record()


def test_completed_process_message_returns_backend_record():
    collector = PatientIntakeCollector()

    result = collector.process_message(
        "I have a headache. Since yesterday. I am an adult."
    )

    assert result.ready is True
    assert result.handoff is True

    assert result.context == collector.get_backend_record()


def test_multi_turn_data_is_preserved_for_backend_handoff():
    collector = PatientIntakeCollector()

    collector.process_message("I have a cough.")
    collector.process_message("Two days ago.")

    result = collector.process_message("I'm 22.")

    assert result.ready is True
    assert result.handoff is True

    assert result.context == {
        "primary_complaint": "a cough",
        "symptom_onset": "Two days ago",
        "age_group": "adult",
        "secondary_history": None,
        "additional_details": None,
    }

# ---------------------------------------------------------
# Sep 15: Graceful fallback and active dialogue state
# ---------------------------------------------------------


def test_off_topic_message_does_not_fill_symptoms():
    collector = PatientIntakeCollector()

    result = collector.process_message(
        "What time does the clinic close?"
    )

    assert result.ready is False
    assert result.handoff is False
    assert result.missing_fields == [
        "symptoms",
        "symptom_onset",
        "age_group",
    ]

    assert collector.info.symptoms is None
    assert collector.info.symptom_onset is None
    assert collector.info.age_group is None


def test_off_topic_message_keeps_symptom_question_active():
    collector = PatientIntakeCollector()

    result = collector.process_message(
        "I want to know the clinic address."
    )

    assert result.response == (
        "I need a little more information about your symptoms. "
        "Please describe what you are experiencing. "
        "What symptoms are you experiencing?"
    )

    assert result.missing_fields == [
        "symptoms",
        "symptom_onset",
        "age_group",
    ]


def test_off_topic_message_does_not_overwrite_existing_symptoms():
    collector = PatientIntakeCollector()

    collector.process_message("I have a headache.")

    result = collector.process_message(
        "Can you tell me your hospital timings?"
    )

    assert result.ready is False
    assert result.handoff is False

    assert collector.info.symptoms == "a headache"
    assert collector.info.symptom_onset is None
    assert collector.info.age_group is None

    assert result.missing_fields == [
        "symptom_onset",
        "age_group",
    ]


def test_ambiguous_onset_keeps_onset_missing():
    collector = PatientIntakeCollector()

    collector.process_message("I have a headache.")

    result = collector.process_message(
        "I don't know."
    )

    assert result.ready is False
    assert result.handoff is False

    assert collector.info.symptoms == "a headache"
    assert collector.info.symptom_onset is None

    assert result.missing_fields == [
        "symptom_onset",
        "age_group",
    ]


def test_ambiguous_onset_returns_graceful_fallback():
    collector = PatientIntakeCollector()

    collector.process_message("I have a headache.")

    result = collector.process_message(
        "Not sure."
    )

    assert result.response == (
        "I need to know when your symptoms started. "
        "For example, you can say 'yesterday' or 'two days ago'. "
        "When did your symptoms start?"
    )


def test_ambiguous_age_keeps_age_missing():
    collector = PatientIntakeCollector()

    collector.process_message("I have a headache.")
    collector.process_message("Yesterday.")

    result = collector.process_message(
        "I don't want to say."
    )

    assert result.ready is False
    assert result.handoff is False
    assert collector.info.age_group is None

    assert result.missing_fields == ["age_group"]


def test_ambiguous_age_returns_graceful_fallback():
    collector = PatientIntakeCollector()

    collector.process_message("I have a headache.")
    collector.process_message("Yesterday.")

    result = collector.process_message(
        "I don't know."
    )

    assert result.response == (
        "I still need your age group. "
        "You can provide your age or say child, teenager, adult, or senior. "
        "What is your age group?"
    )


def test_valid_answer_after_off_topic_message_continues_dialogue():
    collector = PatientIntakeCollector()

    collector.process_message("I have a headache.")

    collector.process_message(
        "Can you tell me the clinic address?"
    )

    result = collector.process_message("Yesterday.")

    assert result.ready is False
    assert result.handoff is False
    assert result.missing_fields == ["age_group"]

    assert collector.info.symptoms == "a headache"
    assert collector.info.symptom_onset == "Yesterday"


def test_valid_answer_after_ambiguous_age_completes_intake():
    collector = PatientIntakeCollector()

    collector.process_message("I have a headache.")
    collector.process_message("Yesterday.")
    collector.process_message("Not sure.")

    result = collector.process_message("I am 22.")

    assert result.ready is True
    assert result.handoff is True
    assert result.missing_fields == []

    assert result.context["primary_complaint"] == "a headache"
    assert result.context["symptom_onset"] == "Yesterday"
    assert result.context["age_group"] == "adult"


def test_off_topic_message_does_not_reset_existing_dialogue_state():
    collector = PatientIntakeCollector()

    collector.process_message(
        "I have a fever. Since yesterday."
    )

    assert collector.info.symptoms == "a fever"
    assert collector.info.symptom_onset == "Since yesterday"
    assert collector.info.age_group is None

    result = collector.process_message(
        "What services do you provide?"
    )

    assert result.ready is False
    assert result.handoff is False

    assert collector.info.symptoms == "a fever"
    assert collector.info.symptom_onset == "Since yesterday"
    assert collector.info.age_group is None

    assert result.missing_fields == ["age_group"]