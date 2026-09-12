from src.doctor_information.intents import (
    DoctorInformationIntent,
    detect_intent,
)
from src.doctor_information.schemas import (
    DoctorInformationResponse,
    DoctorProfile,
    DoctorSchedule,
)


class DoctorInformationService:
    """Handle grounded doctor profile and schedule lookups."""

    def process(
        self,
        query: str,
        doctor: DoctorProfile | None = None,
        schedule: DoctorSchedule | None = None,
    ) -> DoctorInformationResponse:
        """Process a doctor-information query using only supplied data."""

        intent = detect_intent(query)

        if intent == DoctorInformationIntent.UNKNOWN:
            return DoctorInformationResponse(
                doctor=None,
                schedule=None,
                requested_information="unknown",
                information_available=False,
                message="Please specify whether you need the doctor's profile or schedule.",
            )

        if intent == DoctorInformationIntent.PROFILE:
            if doctor is None:
                return DoctorInformationResponse(
                    doctor=None,
                    schedule=None,
                    requested_information="profile",
                    information_available=False,
                    message="The requested doctor profile information is not available.",
                )

            return DoctorInformationResponse(
                doctor=doctor,
                schedule=None,
                requested_information="profile",
                information_available=True,
                message="Doctor profile information retrieved successfully.",
            )

        if schedule is None:
            return DoctorInformationResponse(
                doctor=None,
                schedule=None,
                requested_information="schedule",
                information_available=False,
                message="The requested doctor schedule is not available.",
            )

        return DoctorInformationResponse(
            doctor=None,
            schedule=schedule,
            requested_information="schedule",
            information_available=True,
            message="Doctor schedule information retrieved successfully.",
        )