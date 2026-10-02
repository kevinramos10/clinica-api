from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from app.models.enums import SexoPersona

class PacienteSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = Field(default=None)
    dni: str = Field(max_length=20)
    nombre: str = Field(min_length=1)
    apellidoPaterno: str = Field(min_length=1)
    apellidoMaterno: str = Field(min_length=1)
    telefono: str = Field(min_length=9)
    correo: str | None = Field(default=None)
    fechaNacimiento: date
    sexo: SexoPersona
    direccion: str | None = Field(default=None)
