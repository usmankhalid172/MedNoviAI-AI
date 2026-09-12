from src.appointment_assistance.patient_intake import (
    PatientIntakeCollector,
)


def test_intake_starts_empty():
    collector = PatientIntakeCollector()

    assert collector.info.symptoms is None
    assert collector.info.symptom_onset is None
    assert collector.info.age_group is None


def test_intake_starts_with_all_fields_missing():
    collector = PatientIntakeCollector()

    assert collector.missing_fields() == [
        "symptoms",
        "symptom_onset",
        "age_group",
    ]


def test_collector_stores_symptom_information():
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


def test_intake_becomes_ready_when_all_information_is_collected():
    collector = PatientIntakeCollector()

    collector.update(
        symptoms="headache",
        symptom_onset="since yesterday",
        age_group="adult",
    )

    assert collector.missing_fields() == []
    assert collector.is_ready()


def test_update_ignores_empty_values():
    collector = PatientIntakeCollector()

    collector.update(
        symptoms="headache",
        age_group="adult",
    )

    collector.update(
        symptoms="",
        age_group="",
    )

    assert collector.info.symptoms == "headache"
    assert collector.info.age_group == "adult"

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


def test_next_question_returns_none_when_ready():
    collector = PatientIntakeCollector()

    collector.update(
        symptoms="headache",
        symptom_onset="since yesterday",
        age_group="adult",
    )

    assert collector.next_question() is None

def test_extracts_symptoms_from_message():
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


def test_extracts_multiple_intake_fields_from_one_message():
    collector = PatientIntakeCollector()

    collector.extract_from_message(
        "I have a headache. Since yesterday. I am an adult."
    )

    assert collector.info.symptoms == "a headache"
    assert collector.info.symptom_onset == "Since yesterday"
    assert collector.info.age_group == "adult"

def test_process_message_asks_for_missing_information():
    collector = PatientIntakeCollector()

    response = collector.process_message("I have a headache.")

    assert response == "When did your symptoms start?"


def test_process_message_keeps_information_between_turns():
    collector = PatientIntakeCollector()

    response = collector.process_message("I have a headache.")
    assert response == "When did your symptoms start?"

    response = collector.process_message("Since yesterday.")
    assert response == "What is your age group?"


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
        "symptoms": "a headache",
        "symptom_onset": "Since yesterday",
        "age_group": "adult",
    }


def test_process_message_handles_all_information_in_one_turn():
    collector = PatientIntakeCollector()

    result = collector.process_message(
        "I have a headache. Since yesterday. I am an adult."
    )

    assert result.ready is True
    assert result.missing_fields == []
    assert result.context == {
        "symptoms": "a headache",
        "symptom_onset": "Since yesterday",
        "age_group": "adult",
    }
    
def test_get_context_returns_completed_patient_information():
    collector = PatientIntakeCollector()

    collector.update(
        symptoms="headache",
        symptom_onset="since yesterday",
        age_group="adult",
    )

    context = collector.get_context()

    assert context == {
        "symptoms": "headache",
        "symptom_onset": "since yesterday",
        "age_group": "adult",
    }


def test_get_context_rejects_incomplete_information():
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