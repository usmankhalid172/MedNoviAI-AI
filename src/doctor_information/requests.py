from pydantic import BaseModel, ConfigDict, Field


class DoctorInformationRequest(BaseModel):
    """Request for a doctor profile or schedule lookup."""

    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1)
    doctor_name: str | None = None
    doctor_id: str | None = None
    information_type: str