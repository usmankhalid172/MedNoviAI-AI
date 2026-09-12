from enum import Enum


class DoctorInformationIntent(str, Enum):
    """Supported doctor-information lookup intents."""

    PROFILE = "profile"
    SCHEDULE = "schedule"
    UNKNOWN = "unknown"


_INTENT_KEYWORDS = {
    DoctorInformationIntent.PROFILE: (
        "profile",
        "qualification",
        "qualifications",
        "specialty",
        "specialization",
        "experience",
        "clinic",
        "address",
        "consultation fee",
    ),
    DoctorInformationIntent.SCHEDULE: (
        "schedule",
        "working hours",
        "working days",
        "timing",
        "timings",
        "availability",
        "available",
        "when is the doctor available",
        "doctor's hours",
    ),
}


def detect_intent(message: str) -> DoctorInformationIntent:
    """Detect the primary doctor-information lookup intent."""

    if not isinstance(message, str):
        raise ValueError("message must be a string")

    normalized_message = " ".join(message.lower().strip().split())

    if not normalized_message:
        raise ValueError("message must not be empty")

    for keyword in _INTENT_KEYWORDS[DoctorInformationIntent.SCHEDULE]:
        if keyword in normalized_message:
            return DoctorInformationIntent.SCHEDULE

    for keyword in _INTENT_KEYWORDS[DoctorInformationIntent.PROFILE]:
        if keyword in normalized_message:
            return DoctorInformationIntent.PROFILE

    return DoctorInformationIntent.UNKNOWN