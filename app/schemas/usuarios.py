from pydantic import BaseModel, Field, ConfigDict, model_validator
from app.models.enums import RolUsuario, EstadoUsuario
from uuid import UUID

class UsuarioRespuestaSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user: str
    rol: RolUsuario
    estado: EstadoUsuario
    medico_id: UUID | None = None

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

class ResetPasswordSchema(BaseModel):
    user: str

class ConfirmResetPasswordSchema(BaseModel):
    token: str
    password: str = Field(min_length=8)
    confirmarPassword: str = Field(min_length=8)

    @model_validator(mode="after")
    def validar_Password(self):
        if self.password != self.confirmarPassword:
            raise ValueError("Las constraseñas no coinciden")

        return self
