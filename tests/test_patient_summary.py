from src.patient_summary.schemas import PatientSummary
from src.patient_summary.service import PatientSummaryService


def test_patient_summary_contains_required_information():
    result = PatientSummaryService().generate(
        symptoms=["fever", "cough"],
        duration="3 days",
        context="Symptoms started after recent travel.",
        recommended_specialty="General Medicine",
        safety_disclaimer="This summary is not a diagnosis or prescription.",
    )

    assert isinstance(result, PatientSummary)
    assert result.symptoms == ["fever", "cough"]
    assert result.duration == "3 days"
    assert result.context == "Symptoms started after recent travel."
    assert result.recommended_specialty == "General Medicine"
    assert result.safety_disclaimer == (
        "This summary is not a diagnosis or prescription."
    )


def test_patient_summary_allows_missing_optional_context():
    result = PatientSummaryService().generate(
        symptoms=["headache"],
        duration="1 day",
        context=None,
        recommended_specialty="General Medicine",
        safety_disclaimer="Seek emergency care for severe or life-threatening symptoms.",
    )

    assert result.context is None
    assert result.symptoms == ["headache"]


def test_patient_summary_rejects_unexpected_fields():
    try:
        PatientSummary(
            symptoms=["fever"],
            duration="2 days",
            recommended_specialty="General Medicine",
            safety_disclaimer="This is not a diagnosis.",
            unexpected_field="not allowed",
        )
        assert False
    except Exception:
        assert True


def test_patient_summary_can_be_serialized_to_json():
    result = PatientSummaryService().generate(
        symptoms=["chest discomfort"],
        duration="1 hour",
        context="Symptoms began during physical activity.",
        recommended_specialty="Cardiology",
        safety_disclaimer="This is not a diagnosis or prescription.",
    )

    data = result.model_dump()

    assert data["symptoms"] == ["chest discomfort"]
    assert data["duration"] == "1 hour"
    assert data["recommended_specialty"] == "Cardiology"
    assert data["safety_disclaimer"] == "This is not a diagnosis or prescription."