from pydantic import BaseModel, Field, ConfigDict
from datetime import date, time
from app.models.enums import EstadoCita
from uuid import UUID

class CitaSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = Field(default=None)
    pacienteId: UUID
    medicoId: UUID
    consultorioId: UUID
    fecha: date
    horaInicio: time
    motivo: str | None = Field(default=None)
    estado: EstadoCita = Field(default=EstadoCita.Confirmada)
