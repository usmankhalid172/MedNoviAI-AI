from pydantic import BaseModel, ConfigDict, Field


class DoctorConversationContext(BaseModel):
    """Active context for multi-turn doctor-information queries."""

    model_config = ConfigDict(extra="forbid")

    active_doctor: str | None = None
    active_doctor_id: str | None = None
    active_specialty: str | None = None
    last_intent: str | None = None
    previous_queries: list[str] = Field(default_factory=list)