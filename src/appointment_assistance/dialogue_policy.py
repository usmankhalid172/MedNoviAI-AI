from dataclasses import dataclass
import re


@dataclass
class DialogueTurnResult:
    """Result returned after processing one patient dialogue turn."""

    response: str
    missing_fields: list[str]
    ready: bool
    handoff: bool
    context: dict[str, str] | None = None


@dataclass
class DialogueState:
    """Information collected by the dialogue policy across turns."""

    symptoms: str | None = None
    symptom_onset: str | None = None
    age_group: str | None = None


class PatientDialoguePolicy:
    """
    Manage multi-turn patient intake conversations.

    This policy is intentionally self-contained so it does not modify
    or depend on the previous patient_intake.py implementation.

    The state and result format are kept simple so that this policy
    can later be connected to PatientIntakeCollector.
    """

    REQUIRED_FIELDS = [
        "symptoms",
        "symptom_onset",
        "age_group",
    ]

    def __init__(self) -> None:
        """Initialize an empty dialogue state."""

        self.state = DialogueState()

    def process_message(self, message: str) -> DialogueTurnResult:
        """
        Process one patient message.

        The policy:
        1. Validates the message.
        2. Extracts any useful information.
        3. Preserves information from previous turns.
        4. Finds missing intake information.
        5. Asks the next relevant follow-up question.
        6. Hands off when all required information is collected.
        """

        if not isinstance(message, str):
            raise ValueError("message must be a string")

        normalized_message = " ".join(message.strip().split())

        if not normalized_message:
            raise ValueError("message must not be empty")

        self._extract_information(normalized_message)

        missing_fields = self.get_missing_fields()

        if not missing_fields:
            return DialogueTurnResult(
                response=(
                    "Thank you. I have collected the required patient "
                    "information. The information can now be passed to "
                    "the recommendation module."
                ),
                missing_fields=[],
                ready=True,
                handoff=True,
                context=self.get_context(),
            )

        return DialogueTurnResult(
            response=self._next_question(missing_fields),
            missing_fields=missing_fields,
            ready=False,
            handoff=False,
            context=None,
        )

    def _extract_information(self, message: str) -> None:
        """Extract useful patient information from the current message."""

        self._extract_symptoms(message)
        self._extract_symptom_onset(message)
        self._extract_age_group(message)

    def _extract_symptoms(self, message: str) -> None:
        """Extract symptoms from natural patient statements."""

        symptom_patterns = [
            r"\b(?:i have|i am having|i'm having|"
            r"i've been having|i have been having|"
            r"experiencing|suffering from)\s+(.+?)(?:\.|$)",
        ]

        for pattern in symptom_patterns:
            match = re.search(pattern, message, re.IGNORECASE)

            if match:
                symptoms = match.group(1).strip()

                if symptoms:
                    self.state.symptoms = symptoms

                return

    def _extract_symptom_onset(self, message: str) -> None:
        """Extract symptom onset from complete or short follow-up answers."""

        onset_patterns = [
            r"\b("
            r"since\s+.+?"
            r"|started\s+.+?"
            r"|for\s+\d+\s+(?:day|days|week|weeks|month|months)"
            r"|for\s+(?:a|one|two|three|four|five|six|seven)\s+"
            r"(?:day|days|week|weeks|month|months)"
            r"|.+?\s+ago"
            r"|yesterday"
            r"|today"
            r"|last\s+(?:night|evening|week|month)"
            r"|this\s+(?:morning|afternoon|evening)"
            r")\b",
        ]

        for pattern in onset_patterns:
            match = re.search(pattern, message, re.IGNORECASE)

            if match:
                onset = match.group(1).strip()

                if onset:
                    self.state.symptom_onset = onset

                return

    def _extract_age_group(self, message: str) -> None:
        """Extract an explicit age group or infer it from a numeric age."""

        age_group_match = re.search(
            r"\b("
            r"child|children|teenager|teen|adult|senior|elderly"
            r")\b",
            message,
            re.IGNORECASE,
        )

        if age_group_match:
            age_group = age_group_match.group(1).lower()

            if age_group in {"child", "children"}:
                age_group = "child"
            elif age_group in {"teenager", "teen"}:
                age_group = "teenager"
            elif age_group == "elderly":
                age_group = "senior"

            self.state.age_group = age_group
            return

        age_match = re.search(
            r"\b(?:i'?m|i am)?\s*(\d{1,3})\s*(?:years?\s*old)?\b",
            message,
            re.IGNORECASE,
        )

        if age_match:
            age = int(age_match.group(1))

            if 0 <= age <= 12:
                self.state.age_group = "child"
            elif 13 <= age <= 17:
                self.state.age_group = "teenager"
            elif 18 <= age <= 64:
                self.state.age_group = "adult"
            elif age >= 65:
                self.state.age_group = "senior"

    def get_missing_fields(self) -> list[str]:
        """Return the intake fields that are still missing."""

        missing_fields = []

        if not self.state.symptoms:
            missing_fields.append("symptoms")

        if not self.state.symptom_onset:
            missing_fields.append("symptom_onset")

        if not self.state.age_group:
            missing_fields.append("age_group")

        return missing_fields

    def is_ready(self) -> bool:
        """Return True when all required information is available."""

        return not self.get_missing_fields()

    def get_context(self) -> dict[str, str]:
        """
        Return completed patient information for recommendation handoff.

        Raises:
            ValueError: If required information is still missing.
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

    def _next_question(self, missing_fields: list[str]) -> str:
        """Select the most appropriate follow-up question."""

        if "symptoms" in missing_fields:
            return "What symptoms are you experiencing?"

        if "symptom_onset" in missing_fields:
            return "When did your symptoms start?"

        if "age_group" in missing_fields:
            return "What is your age group?"

        return "Could you provide more information about your symptoms?"