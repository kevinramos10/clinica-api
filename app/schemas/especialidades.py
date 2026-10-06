from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID

class EspecialidadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = Field(default=None)
    nombre: str = Field(min_length=1)