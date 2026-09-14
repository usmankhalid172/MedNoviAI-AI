from src.doctor_information.context import DoctorConversationContext
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
        context: DoctorConversationContext | None = None,
    ) -> DoctorInformationResponse:
        """Process a doctor-information query using supplied data and context."""

        if context is None:
            context = DoctorConversationContext()

        intent = detect_intent(query)

        if intent == DoctorInformationIntent.UNKNOWN:
            if context.active_doctor:
                return DoctorInformationResponse(
                    doctor=None,
                    schedule=None,
                    requested_information="unknown",
                    information_available=False,
                    message=(
                        f"I can help with information about {context.active_doctor}. "
                        "Please specify whether you need the doctor's profile or schedule."
                    ),
                )

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

            context.active_doctor = doctor.doctor_name
            context.active_doctor_id = doctor.doctor_id
            context.last_intent = intent.value

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
                message=(
                    f"The schedule for {context.active_doctor} is not available."
                    if context.active_doctor
                    else "The requested doctor schedule is not available."
                ),
            )

        context.active_doctor = schedule.doctor_name
        context.active_doctor_id = schedule.doctor_id
        context.last_intent = intent.value

        return DoctorInformationResponse(
            doctor=None,
            schedule=schedule,
            requested_information="schedule",
            information_available=True,
            message="Doctor schedule information retrieved successfully.",
        )