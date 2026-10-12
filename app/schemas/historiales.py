from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID

class HistorialSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = Field(default=None)
    citaId: UUID
    diagnostico: str | None = Field(default=None)
    tratamiento: str | None = Field(default=None)
    observaciones: str | None = Field(default=None)
    fechaRegistro: datetime | None = Field(default=None)