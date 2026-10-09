from pydantic import BaseModel, Field, ConfigDict
from app.models.enums import RolUsuario, EstadoUsuario
from uuid import UUID


class UsuarioSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = Field(default=None)
    password: str
    rol: RolUsuario
    estado: EstadoUsuario = Field(default=EstadoUsuario.Activo)
    medicoId: UUID | None = Field(default=None)

class LoginUsuarioSchema(BaseModel):
    user: str
    password: str

class CambiarPasswordSchema(BaseModel):
    passwordActual: str
    passwordNueva: str