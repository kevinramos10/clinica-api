from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Annotated
from uuid import UUID

ListaIds = Annotated[list[UUID], Field(min_length=1, max_length=100)]

class MedicosEspecialidadesSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    medicoId: UUID
    especialidadIds: ListaIds = Field()

    @field_validator('especialidadIds')

    def eliminar_duplicados(cls, valor):

        return list(set(valor))
