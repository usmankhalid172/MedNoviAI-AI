from dataclasses import dataclass

import re


@dataclass
class PatientIntakeTurnResult:
    """Result returned after processing one patient message."""

    response: str
    missing_fields: list[str]
    ready: bool
    context: dict[str, str | None] | None = None
    handoff: bool = False
    fallback: bool = False


@dataclass
class PatientIntakeInformation:
    """Structured information collected during patient intake."""

    # Required intake fields
    symptoms: str | None = None
    symptom_onset: str | None = None
    age_group: str | None = None

    # Optional intake fields
    secondary_history: str | None = None
    additional_details: str | None = None


class PatientIntakeCollector:
    """
    Collect patient information across multiple conversation turns.
    """

    REQUIRED_FIELDS = [
        "symptoms",
        "symptom_onset",
        "age_group",
    ]

    FALLBACK_MESSAGES = {
        "symptoms": (
            "I need a little more information about your symptoms. "
            "Please describe what you are experiencing."
        ),
        "symptom_onset": (
            "I need to know when your symptoms started. "
            "For example, you can say 'yesterday' or 'two days ago'."
        ),
        "age_group": (
            "I still need your age group. "
            "You can provide your age or say child, teenager, adult, or senior."
        ),
    }

    AMBIGUOUS_RESPONSES = {
        "i don't know",
        "i dont know",
        "not sure",
        "i'm not sure",
        "im not sure",
        "maybe",
        "don't know",
        "dont know",
        "unsure",
        "no idea",
        "i have no idea",
        "cannot say",
        "can't say",
        "cant say",
    }

    def __init__(self) -> None:
        self.info = PatientIntakeInformation()

    def update(
        self,
        symptoms: str | None = None,
        symptom_onset: str | None = None,
        age_group: str | None = None,
        secondary_history: str | None = None,
        additional_details: str | None = None,
    ) -> PatientIntakeInformation:
        """Update required and optional patient intake information."""

        if symptoms:
            self.info.symptoms = symptoms.strip()

        if symptom_onset:
            self.info.symptom_onset = symptom_onset.strip()

        if age_group:
            self.info.age_group = age_group.strip()

        if secondary_history:
            self.info.secondary_history = secondary_history.strip()

        if additional_details:
            self.info.additional_details = additional_details.strip()

        return self.info

    def _normalize_message(self, message: str) -> str:
        """Normalize whitespace and validate a patient message."""

        if not isinstance(message, str):
            raise ValueError("message must be a string")

        normalized_message = " ".join(message.strip().split())

        if not normalized_message:
            raise ValueError("message must not be empty")

        return normalized_message

    def _is_ambiguous_response(self, message: str) -> bool:
        """Return True when a patient gives a non-informative response."""

        normalized_message = self._normalize_message(message).lower()

        return normalized_message in self.AMBIGUOUS_RESPONSES

    def _extract_age_group(self, message: str) -> str | None:
        """Extract or derive an age group from a patient message."""

        age_match = re.search(
            r"\b("
            r"child|children|teenager|teen|adult|senior|elderly"
            r")\b",
            message,
            re.IGNORECASE,
        )

        if age_match:
            age_group = age_match.group(1).lower()

            if age_group in {"child", "children"}:
                return "child"

            if age_group in {"teenager", "teen"}:
                return "teenager"

            if age_group == "elderly":
                return "senior"

            return age_group

        numeric_age_match = re.search(
            r"\b(?:i'?m|i am)?\s*(\d{1,3})"
            r"\s*(?:years?\s*old)?\b",
            message,
            re.IGNORECASE,
        )

        if numeric_age_match:
            age = int(numeric_age_match.group(1))

            if 0 <= age <= 12:
                return "child"

            if 13 <= age <= 17:
                return "teenager"

            if 18 <= age <= 64:
                return "adult"

            if age >= 65:
                return "senior"

        return None

    def _extract_onset(self, message: str) -> str | None:
        """Extract symptom onset information."""

        onset_patterns = [
            r"since\s+[^.?!]+",
            r"started\s+[^.?!]+",
            r"for\s+\d+\s+(?:day|days|week|weeks|month|months)",
            r"for\s+(?:a|one|two|three|four|five|six|seven)\s+"
            r"(?:day|days|week|weeks|month|months)",
            r"[^.?!]+?\s+ago",
            r"yesterday",
            r"today",
            r"last\s+(?:night|evening|week|month)",
            r"this\s+(?:morning|afternoon|evening)",
        ]

        for pattern in onset_patterns:
            onset_match = re.search(
                pattern,
                message,
                re.IGNORECASE,
            )

            if onset_match:
                return onset_match.group(0).strip().rstrip(".,!?")

        return None

    def extract_from_message(
        self,
        message: str,
    ) -> PatientIntakeInformation:
        """Extract patient intake information from a message."""

        normalized_message = self._normalize_message(message)

        extracted = {}

        # Primary complaint / symptoms
        symptom_match = re.search(
            r"\b(?:i have|i am having|i'm having|"
            r"i've been having|i have been having|"
            r"experiencing|suffering from)\s+"
            r"(.+?)(?:\.|$)",
            normalized_message,
            re.IGNORECASE,
        )

        if symptom_match:
            extracted["symptoms"] = symptom_match.group(1).strip()

        # Symptom onset
        onset = self._extract_onset(normalized_message)

        if onset:
            extracted["symptom_onset"] = onset

        # Age group
        age_group = self._extract_age_group(normalized_message)

        if age_group:
            extracted["age_group"] = age_group

        return self.update(**extracted)

    def _extract_follow_up_answer(
        self,
        message: str,
    ) -> bool:
        """
        Interpret a short patient response using the currently
        missing required field as dialogue context.

        Returns True when the response supplied valid information
        for the currently active field.
        """

        normalized_message = self._normalize_message(message)
        missing = self.missing_fields()

        if not missing:
            return False

        active_field = missing[0]

        if active_field == "symptoms":
            symptom_indicators = (
                "pain",
                "ache",
                "headache",
                "fever",
                "cough",
                "cold",
                "nausea",
                "vomiting",
                "dizziness",
                "fatigue",
                "weakness",
                "rash",
                "bleeding",
                "swelling",
                "sore",
                "soreness",
                "painful",
                "difficulty",
                "shortness",
                "breathing",
                "diarrhea",
                "constipation",
                "infection",
                "itching",
                "itchy",
                "cramps",
                "cramping",
                "congestion",
                "migraine",
                "stomach",
                "throat",
                "chest",
                "back",
            )

            message_lower = normalized_message.lower()

            if any(
                indicator in message_lower
                for indicator in symptom_indicators
            ):
                self.update(symptoms=normalized_message)
                return True

            return False

        if active_field == "symptom_onset":
            onset = self._extract_onset(normalized_message)

            if onset:
                self.update(symptom_onset=onset)
                return True

            return False

        if active_field == "age_group":
            age_group = self._extract_age_group(normalized_message)

            if age_group:
                self.update(age_group=age_group)
                return True

            return False

        return False

    def process_message(
        self,
        message: str,
    ) -> PatientIntakeTurnResult:
        """
        Process one patient message using multi-turn dialogue context.

        The collector extracts explicit information first, then uses
        the active missing field to interpret valid short follow-up
        answers. Ambiguous or off-topic input does not overwrite
        existing patient information.
        """

        normalized_message = self._normalize_message(message)

        # Remember which required fields were missing before
        # processing this turn.
        missing_before = self.missing_fields()

        # First extract information explicitly stated in the message.
        self.extract_from_message(normalized_message)

        missing_after_extraction = self.missing_fields()

        progress_made = len(missing_after_extraction) < len(missing_before)

        # Only use contextual follow-up interpretation when the
        # message did not explicitly provide any missing field.
        #
        # Explicitly ambiguous responses are skipped so they cannot
        # accidentally be interpreted as patient information.
        if missing_before and not progress_made:
            if not self._is_ambiguous_response(normalized_message):
                progress_made = self._extract_follow_up_answer(
                    normalized_message
                )

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
                missing_fields=[],
                ready=True,
                context=self.get_backend_record(),
                handoff=True,
                fallback=False,
            )

        if not progress_made and missing_fields:
            active_field = missing_fields[0]

            fallback = self.FALLBACK_MESSAGES.get(
                active_field,
                "Please provide the missing patient information.",
            )

            next_question = self.next_question()
            response = f"{fallback} {next_question}"

            return PatientIntakeTurnResult(
                response=response,
                missing_fields=missing_fields,
                ready=False,
                context=None,
                handoff=False,
                fallback=True,
            )

        return PatientIntakeTurnResult(
            response=self.next_question(),
            missing_fields=missing_fields,
            ready=False,
            context=None,
            handoff=False,
            fallback=False,
        )

    def missing_fields(self) -> list[str]:
        """Return required intake information that is still missing."""

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

    def get_context(self) -> dict[str, str | None]:
        """
        Return structured patient data.

        This method is kept for backward compatibility with the
        existing dialogue and recommendation interfaces.
        """

        return self.get_backend_record()

    def get_backend_record(self) -> dict[str, str | None]:
        """
        Return the finalized patient record for backend storage handoff.
        """

        if not self.is_ready():
            raise ValueError(
                "Patient intake is incomplete. "
                "Collect all required information first."
            )

        return {
            "primary_complaint": self.info.symptoms,
            "symptom_onset": self.info.symptom_onset,
            "age_group": self.info.age_group,
            "secondary_history": self.info.secondary_history,
            "additional_details": self.info.additional_details,
        }

    def next_question(self) -> str | None:
        """Return the next question needed to complete required intake."""

        if not self.info.symptoms:
            return "What symptoms are you experiencing?"

        if not self.info.symptom_onset:
            return "When did your symptoms start?"

        if not self.info.age_group:
            return "What is your age group?"

        return None