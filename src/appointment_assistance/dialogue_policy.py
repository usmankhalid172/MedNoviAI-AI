from dataclasses import dataclass

from src.appointment_assistance.patient_intake import PatientIntakeCollector


@dataclass
class DialogueTurnResult:
    """Result returned after processing one patient dialogue turn."""
    response: str
    missing_fields: list[str]
    ready: bool
    handoff: bool
    context: dict[str, str | None] | None = None
    patient_record: dict[str, str | None] | None = None


class PatientDialoguePolicy:
    """
    Manage multi-turn patient intake conversations.

    The dialogue policy controls the conversation while
    PatientIntakeCollector owns patient information, extraction,
    validation, and structured patient context.

    This keeps the dialogue layer separate from the patient-intake
    data layer while allowing both modules to work together.
    """

    def __init__(self) -> None:
        """Initialize the dialogue policy with a patient intake collector."""
        self.intake = PatientIntakeCollector()

    @property
    def state(self):
        """Expose the current patient intake information."""
        return self.intake.info

    def process_message(self, message: str) -> DialogueTurnResult:
        """
        Process one patient message.

        PatientIntakeCollector extracts and stores information.
        The dialogue policy decides whether to ask another question
        or hand the completed information to the next module.
        """
        result = self.intake.process_message(message)

        if result.ready:
            return DialogueTurnResult(
                response=result.response,
                missing_fields=[],
                ready=True,
                handoff=True,
                context=self.get_context(),
                patient_record=self.get_patient_record(),
            )

        return DialogueTurnResult(
            response=result.response,
            missing_fields=result.missing_fields,
            ready=False,
            handoff=False,
            context=None,
            patient_record=None,
        )

    def get_missing_fields(self) -> list[str]:
        """Return required intake fields that are still missing."""
        return self.intake.missing_fields()

    def is_ready(self) -> bool:
        """Return True when all required intake information is collected."""
        return self.intake.is_ready()

    def get_context(self) -> dict[str, str | None]:
        """
        Return the dialogue-compatible context.

        This preserves the existing dialogue-policy interface.
        """
        if not self.is_ready():
            raise ValueError(
                "Patient intake is incomplete. "
                "Collect all required information first."
            )

        return {
            "symptoms": self.state.symptoms,
            "symptom_onset": self.state.symptom_onset,
            "age_group": self.state.age_group,
        }

    def get_patient_record(self) -> dict[str, str | None]:
        """
        Return the structured patient record from PatientIntakeCollector.

        This is the context intended for downstream recommendation
        or backend modules.
        """
        return self.intake.get_context()