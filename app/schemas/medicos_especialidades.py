from pydantic import BaseModel, Field, ConfigDict, PositiveInt, field_validator

from typing import Annotated

ListaIds = Annotated[list[PositiveInt], Field(min_length=1, max_length=100)]

class MedicosEspecialidadesSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    medicoId: int = Field(min=1)
    especialidadIds: ListaIds = Field()

    @field_validator('especialidadIds')

    def eliminar_duplicados(cls, valor):

        return list(set(valor))
