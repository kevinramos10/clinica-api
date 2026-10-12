from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from app.models.enums import SexoPersona, EstadoMedico
from uuid import UUID

class MedicoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = Field(default=None)
    dni: str = Field(max_length=20)
    colegiatura: str = Field(max_length=20)
    nombre: str = Field(min_length=1)
    apellidoPaterno: str = Field(min_length=1)
    apellidoMaterno: str = Field(min_length=1)
    sexo: SexoPersona
    telefono: str = Field(min_length=9)
    correo: str
    fechaNacimiento: date
    estado: EstadoMedico
    



