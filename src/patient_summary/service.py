from src.patient_summary.schemas import PatientSummary


class PatientSummaryService:
    """Build structured patient summaries from supplied information."""

    def generate(
        self,
        symptoms: list[str],
        duration: str,
        context: str | None,
        recommended_specialty: str,
        safety_disclaimer: str,
    ) -> PatientSummary:
        """Generate a structured summary without diagnosing or prescribing."""

        return PatientSummary(
            symptoms=symptoms,
            duration=duration,
            context=context,
            recommended_specialty=recommended_specialty,
            safety_disclaimer=safety_disclaimer,
        )
