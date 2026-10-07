from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID

class ConsultorioSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = Field(default=None)
    numero: str = Field(min_length=1)
    piso: int = Field(ge=0)
