from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID
from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import field_serializer

class HistorialSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = Field(default=None)
    citaId: UUID
    diagnostico: str | None = Field(default=None)
    tratamiento: str | None = Field(default=None)
    observaciones: str | None = Field(default=None)
    fechaRegistro: datetime | None = Field(default=None)

class HistorialRegisterSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = Field(default=None)
    citaId: UUID
    diagnostico: str | None = Field(default=None)
    tratamiento: str | None = Field(default=None)
    observaciones: str | None = Field(default=None)
    fechaRegistro: datetime = Field(
        default_factory=lambda: datetime.now(ZoneInfo("America/Lima"))
    )

    @field_serializer('fechaRegistro', when_used='json')
    def serializar_fecha(self, fecha:datetime):
        return fecha.strftime("%d/%m/%Y %H:%M:%S")