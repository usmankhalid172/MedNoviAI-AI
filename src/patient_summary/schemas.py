from pydantic import BaseModel, ConfigDict, Field


class PatientSummary(BaseModel):
    """Structured summary of patient-reported information."""

    model_config = ConfigDict(extra="forbid")

    symptoms: list[str] = Field(default_factory=list)
    duration: str
    context: str | None = None
    recommended_specialty: str
    safety_disclaimer: str
