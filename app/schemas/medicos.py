from pydantic import BaseModel, Field, ConfigDict, EmailStr
from datetime import date
from app.models.enums import SexoPersona, EstadoMedico
from uuid import UUID

class MedicoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = Field(default=None)
    dni: str = Field(min_length=8, max_length=20)
    colegiatura: str = Field(min_length=1, max_length=20)
    nombre: str = Field(min_length=1)
    apellidoPaterno: str = Field(min_length=1)
    apellidoMaterno: str = Field(min_length=1)
    sexo: SexoPersona
    telefono: str = Field(min_length=9)
    correo: EmailStr
    fechaNacimiento: date
    estado: EstadoMedico = Field(default=EstadoMedico.Activo)
    



