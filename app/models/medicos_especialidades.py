from app.extensions import db
from sqlalchemy import Column, types, ForeignKey
from sqlalchemy.orm import relationship

class MedicoEspecialidad(db.Model):

    __tablename__ = 'medicos_especialidades'


    medicoId = Column(
        ForeignKey(column='medicos.id'),
        nullable=False,
        name='medico_id',
        primary_key=True,
        type_=types.Integer
    )

    especialidadId = Column(
        ForeignKey(column='especialidades.id'),
        nullable=False,
        name='especialidad_id',
        primary_key=True,
        type_=types.Integer
    )

    medicos = relationship('Medico', backref='medico_especialidad')

    especialidadese = relationship('Especialidad', backref='medico_especialidad')

    