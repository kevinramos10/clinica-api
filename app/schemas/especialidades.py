from pydantic import BaseModel, Field, ConfigDict


class EspecialidadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = Field(default=None)
    nombre: str = Field(min_length=1)