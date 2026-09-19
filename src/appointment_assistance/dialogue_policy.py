from dataclasses import dataclass

from src.appointment_assistance.patient_intake import PatientIntakeCollector


class DialogueResponses:
	"""Centralized response templates for patient dialogue."""

	INCOMPLETE = "Please provide the missing patient information."
	READY = (
		"Thank you. I have collected the required patient information. "
		"The information can now be passed to the recommendation module."
	)
	MISSING_SYMPTOMS = "What symptoms are you experiencing?"
	MISSING_ONSET = "When did your symptoms start?"
	MISSING_AGE = "What is your age group?"


@dataclass
class DialogueTurnResult:
	"""Result returned after processing one dialogue turn."""

	response: str
	missing_fields: list[str]
	ready: bool
	handoff: bool
	context: dict[str, str | None] | None = None
	patient_record: dict[str, str | None] | None = None


class PatientDialoguePolicy:
	"""Manage multi-turn patient intake conversations."""

	def __init__(self) -> None:
		"""Initialize the dialogue policy with a patient intake collector."""
		self.intake = PatientIntakeCollector()

	@property
	def state(self):
		"""Expose the current patient intake information."""
		return self.intake.info

	def process_message(self, message: str) -> DialogueTurnResult:
		"""Process a patient message and maintain dialogue state."""
		result = self.intake.process_message(message)

		if result.ready:
			return DialogueTurnResult(
				response=DialogueResponses.READY,
				missing_fields=[],
				ready=True,
				handoff=True,
				context=self.get_context(),
				patient_record=self.get_patient_record(),
			)

		next_question = self.get_next_question()
		if result.fallback and self.state.symptoms:
			response = result.response
		else:
			response = next_question or result.response

		return DialogueTurnResult(
			response=response,
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
		"""Return the dialogue-compatible context."""
		if not self.is_ready():
			raise ValueError(
				"Patient intake is incomplete. Collect all required information first."
			)
		return {
			"symptoms": self.state.symptoms,
			"symptom_onset": self.state.symptom_onset,
			"age_group": self.state.age_group,
		}

	def get_patient_record(self) -> dict[str, str | None]:
		"""Return the structured patient record."""
		return self.intake.get_context()

	def get_next_question(self) -> str | None:
		"""Return the next question required to complete patient intake."""
		missing_fields = self.get_missing_fields()
		if not missing_fields:
			return None

		questions = {
			"symptoms": DialogueResponses.MISSING_SYMPTOMS,
			"symptom_onset": DialogueResponses.MISSING_ONSET,
			"age_group": DialogueResponses.MISSING_AGE,
		}
		return questions.get(missing_fields[0])