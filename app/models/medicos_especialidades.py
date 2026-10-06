from app.extensions import db
from sqlalchemy import Column, types, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4

class MedicoEspecialidad(db.Model):

    __tablename__ = 'medicos_especialidades'


    medicoId = Column(
        ForeignKey(column='medicos.id'),
        nullable=False,
        name='medico_id',
        primary_key=True,
        type_=types.UUID()
    )

    especialidadId = Column(
        ForeignKey(column='especialidades.id'),
        nullable=False,
        name='especialidad_id',
        primary_key=True,
        type_=types.Integer
    )

    medico = relationship('Medico', backref='medico_especialidades')

    especialidad = relationship('Especialidad', backref='medico_especialidades')

    