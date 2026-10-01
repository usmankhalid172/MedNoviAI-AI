from pydantic import BaseModel, ConfigDict, Field


class DoctorProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Structured doctor information supplied by the backend."""

    doctor_id: str | None = None
    doctor_name: str
    specialty: str | None = None
    qualifications: list[str] = Field(default_factory=list)
    experience: str | None = None
    clinic: str | None = None
    address: str | None = None
    consultation_fee: str | None = None


class DoctorSchedule(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Doctor schedule information supplied by the backend."""

    doctor_id: str | None = None
    doctor_name: str
    schedule: dict[str, list[str]] = Field(default_factory=dict)


class DoctorInformationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Structured response for doctor profile or schedule lookups."""

    doctor: DoctorProfile | None = None
    schedule: DoctorSchedule | None = None
    requested_information: str
    information_available: bool
    message: str