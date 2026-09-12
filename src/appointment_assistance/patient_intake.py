from dataclasses import dataclass
import re


@dataclass
class PatientIntakeTurnResult:
    """Result returned after processing one patient message."""

    response: str
    missing_fields: list[str]
    ready: bool
    context: dict[str, str] | None = None


@dataclass
class PatientIntakeInformation:
    """Information collected during patient symptom intake."""

    symptoms: str | None = None
    symptom_onset: str | None = None
    age_group: str | None = None

class PatientIntakeCollector:
    """Collect patient information across multiple conversation turns."""

    def __init__(self) -> None:
        self.info = PatientIntakeInformation()

    def update(
        self,
        symptoms: str | None = None,
        symptom_onset: str | None = None,
        age_group: str | None = None,
    ) -> PatientIntakeInformation:
        """Update the information collected from the patient."""

        if symptoms:
            self.info.symptoms = symptoms.strip()

        if symptom_onset:
            self.info.symptom_onset = symptom_onset.strip()

        if age_group:
            self.info.age_group = age_group.strip()

        return self.info

    def extract_from_message(self, message: str) -> PatientIntakeInformation:
        """Extract basic patient intake information from a message."""

        if not isinstance(message, str):
            raise ValueError("message must be a string")

        normalized_message = " ".join(message.strip().split())

        if not normalized_message:
            raise ValueError("message must not be empty")

        extracted = {}

        # Examples:
        # "I have a headache"
        # "I am experiencing fever and cough"
        symptom_match = re.search(
            r"\b(?:i have|i am having|i'm having|experiencing|suffering from)\s+"
            r"(.+?)(?:\.|$)",
            normalized_message,
            re.IGNORECASE,
        )

        if symptom_match:
            extracted["symptoms"] = symptom_match.group(1).strip()

        # Examples:
        # "since yesterday"
        # "started yesterday"
        # "for two days"
        onset_match = re.search(
            r"\b("
            r"since\s+.+?"
            r"|started\s+.+?"
            r"|for\s+\d+\s+(?:day|days|week|weeks|month|months)"
            r")"
            r"(?:\.|$)",
            normalized_message,
            re.IGNORECASE,
        )

        if onset_match:
            extracted["symptom_onset"] = onset_match.group(1).strip()

        # Examples:
        # "I am an adult"
        # "adult"
        # "I'm a child"
        age_match = re.search(
            r"\b("
            r"child|children|teenager|teen|adult|senior|elderly"
            r")\b",
            normalized_message,
            re.IGNORECASE,
        )

        if age_match:
            age_group = age_match.group(1).lower()

            if age_group in {"child", "children"}:
                age_group = "child"
            elif age_group in {"teenager", "teen"}:
                age_group = "teenager"
            elif age_group == "elderly":
                age_group = "senior"

            extracted["age_group"] = age_group

        return self.update(**extracted)

    def missing_fields(self) -> list[str]:
        """Return the intake information that is still missing."""

        missing = []

        if not self.info.symptoms:
            missing.append("symptoms")

        if not self.info.symptom_onset:
            missing.append("symptom_onset")

        if not self.info.age_group:
            missing.append("age_group")

        return missing

    def is_ready(self) -> bool:
        """Return True when all required intake information is collected."""

        return not self.missing_fields()
    
    def get_context(self) -> dict[str, str]:
        """Return completed patient information for the recommendation module."""

        if not self.is_ready():
            raise ValueError(
                "Patient intake is incomplete. "
                "Collect all required information first."
            )

        return {
            "symptoms": self.info.symptoms,
            "symptom_onset": self.info.symptom_onset,
            "age_group": self.info.age_group,
        }
    
    def next_question(self) -> str | None:
        """Return the next question needed to complete patient intake."""

        if not self.info.symptoms:
            return "What symptoms are you experiencing?"

        if not self.info.symptom_onset:
            return "When did your symptoms start?"

        if not self.info.age_group:
            return "What is your age group?"

        return None

    def process_message(self, message: str) -> PatientIntakeTurnResult:
        """Process one patient message and return the dialogue result."""

        self.extract_from_message(message)

        missing_fields = self.missing_fields()
        ready = not missing_fields

        if ready:
            response = (
                "Thank you. I have collected the required patient "
                "information. The information can now be passed to "
                "the recommendation module."
            )

            return PatientIntakeTurnResult(
                response=response,
                missing_fields=missing_fields,
                ready=ready,
                context=self.get_context(),
            )

        return PatientIntakeTurnResult(
            response=self.next_question(),
            missing_fields=missing_fields,
            ready=ready,
            context=None,
        )