from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_serializer, field_validator
from datetime import date, datetime
from app.models.enums import SexoPersona
from uuid import UUID

class PacienteSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = Field(default=None)
    dni: str = Field(min_length=8, max_length=20)
    nombre: str = Field(min_length=1)
    apellidoPaterno: str = Field(min_length=1)
    apellidoMaterno: str = Field(min_length=1)
    telefono: str = Field(min_length=9)
    correo: EmailStr | None = Field(default=None)
    fechaNacimiento: date
    sexo: SexoPersona
    direccion: str | None = Field(default=None)

    @field_validator('fechaNacimiento', mode='before')
    @classmethod
    def validar_fecha(cls, valor):
        if isinstance(valor, str):
            return datetime.strptime(valor, "%d/%m/%Y").date()
        return valor


    def serializar_fecha(self, fecha:date):
        return fecha.strftime("%d/%m/%Y")
