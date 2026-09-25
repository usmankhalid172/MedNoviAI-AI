from dataclasses import dataclass
import json
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

    CLARIFICATION_MESSAGES = {
        "symptoms": (
            "I need a little more information about your symptoms. "
            "Please describe what you are experiencing. "
            "What symptoms are you experiencing?"
        ),
        "symptom_onset": (
            "I need to know when your symptoms started. "
            "For example, you can say 'yesterday' or 'two days ago'. "
            "When did your symptoms start?"
        ),
        "age_group": (
            "I still need your age group. "
            "You can provide your age or say child, teenager, adult, or senior. "
            "What is your age group?"
        ),
    }

    OFF_TOPIC_MESSAGES = {
        "symptoms": (
            "Let's continue with your patient information. "
            "Please describe the symptoms you are experiencing."
        ),
        "symptom_onset": (
            "Let's continue with your patient information. "
            "Please tell me when your symptoms started."
        ),
        "age_group": (
            "Let's continue with your patient information. "
            "Please provide your age or age group."
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
        "i don't remember",
        "i dont remember",
        "not certain",
        "uncertain",
    }

    OFF_TOPIC_PHRASES = {
        "what time is it",
        "what is the time",
        "what day is it",
        "who are you",
        "what are you",
        "where are you",
        "thank you",
        "thanks",
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
        "okay thanks",
        "ok thanks",
    }

    def __init__(self) -> None:
        self.info = PatientIntakeInformation()

        # Dialogue history used to maintain state continuity.
        # The collected patient information remains the source of truth.
        self.dialogue_history: list[dict[str, str | None]] = []

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

        if normalized_message in self.AMBIGUOUS_RESPONSES:
            return True

        ambiguous_patterns = (
            r"^i\s+(really\s+)?don't\s+know$",
            r"^i\s+(really\s+)?dont\s+know$",
            r"^i\s+(really\s+)?am\s+not\s+sure$",
            r"^i\s+(really\s+)?['’]?m\s+not\s+sure$",
            r"^i\s+cannot\s+say$",
            r"^i\s+can't\s+say$",
            r"^i\s+cant\s+say$",
            r"^i\s+don't\s+remember$",
            r"^i\s+dont\s+remember$",
            r"^not\s+really\s+sure$",
            r"^not\s+quite\s+sure$",
        )

        return any(
            re.fullmatch(pattern, normalized_message)
            for pattern in ambiguous_patterns
        )

    def _is_off_topic_response(self, message: str) -> bool:
        """Return True when a message is clearly unrelated to patient intake."""

        normalized_message = self._normalize_message(message).lower()

        if normalized_message in self.OFF_TOPIC_PHRASES:
            return True

        off_topic_patterns = (
            r"^what\s+time\s+does\s+.*\s+(close|open)$",
            r"^what\s+is\s+your\s+name\??$",
            r"^who\s+are\s+you\??$",
            r"^can\s+you\s+help\s+me\s+with\s+.*$",
            r"^tell\s+me\s+about\s+.*$",
        )

        return any(
            re.fullmatch(pattern, normalized_message)
            for pattern in off_topic_patterns
        )

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

        Explicit information is extracted first. If no progress is made,
        the active missing field is used to interpret short follow-up
        answers. Ambiguous and off-topic responses never overwrite
        existing patient information.
        """

        normalized_message = self._normalize_message(message)
        missing_before = self.missing_fields()

        # Explicitly handle clearly ambiguous/off-topic messages first.
        is_ambiguous = self._is_ambiguous_response(normalized_message)
        is_off_topic = self._is_off_topic_response(normalized_message)

        # Extract explicit patient information only when the message is
        # not clearly off-topic or ambiguous.
        progress_made = False

        if not is_ambiguous and not is_off_topic:
            self.extract_from_message(normalized_message)

            missing_after_extraction = self.missing_fields()

            progress_made = (
                len(missing_after_extraction)
                < len(missing_before)
            )

            # Use active-field context for short follow-up answers.
            if missing_before and not progress_made:
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

            result = PatientIntakeTurnResult(
                response=response,
                missing_fields=[],
                ready=True,
                context=self.get_backend_record(),
                handoff=True,
                fallback=False,
            )

            self._record_dialogue_turn(
                normalized_message,
                result,
            )

            return result

        if not progress_made and missing_fields:
            active_field = missing_fields[0]

            if is_ambiguous:
                response = self.CLARIFICATION_MESSAGES.get(
                    active_field,
                    self.FALLBACK_MESSAGES.get(
                        active_field,
                        "Please provide the missing patient information.",
                    ),
                )

            elif is_off_topic:
                response = self.OFF_TOPIC_MESSAGES.get(
                    active_field,
                    "Let's continue with the patient information.",
                )

            else:
                fallback = self.FALLBACK_MESSAGES.get(
                    active_field,
                    "Please provide the missing patient information.",
                )

                next_question = self.next_question()
                response = f"{fallback} {next_question}"

            result = PatientIntakeTurnResult(
                response=response,
                missing_fields=missing_fields,
                ready=False,
                context=None,
                handoff=False,
                fallback=True,
            )

            self._record_dialogue_turn(
                normalized_message,
                result,
            )

            return result

        result = PatientIntakeTurnResult(
            response=self.next_question(),
            missing_fields=missing_fields,
            ready=False,
            context=None,
            handoff=False,
            fallback=False,
        )

        self._record_dialogue_turn(
            normalized_message,
            result,
        )

        return result

    def _record_dialogue_turn(
        self,
        message: str,
        result: PatientIntakeTurnResult,
    ) -> None:
        """
        Store lightweight dialogue history for state continuity.

        The history is informational only. PatientIntakeInformation
        remains the source of truth for backend data.
        """

        self.dialogue_history.append(
            {
                "message": message,
                "response": result.response,
                "ready": str(result.ready),
                "handoff": str(result.handoff),
            }
        )

    def get_dialogue_history(self) -> list[dict[str, str | None]]:
        """
        Return the current dialogue history.

        A copy is returned so callers cannot accidentally modify
        the internal conversation state.
        """

        return list(self.dialogue_history)

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

        The dictionary uses stable keys expected by the backend layer.
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

    def get_backend_json(self) -> str:
        """
        Return the completed patient record as JSON.

        Python None values are serialized as JSON null so the resulting
        structure can be passed cleanly to a .NET backend.
        """

        return json.dumps(
            self.get_backend_record(),
            ensure_ascii=False,
        )

    def next_question(self) -> str | None:
        """Return the next question needed to complete required intake."""

        if not self.info.symptoms:
            return "What symptoms are you experiencing?"

        if not self.info.symptom_onset:
            return "When did your symptoms start?"

        if not self.info.age_group:
            return "What is your age group?"

        return None