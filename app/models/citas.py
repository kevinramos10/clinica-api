from app.extensions import db
from sqlalchemy import Column, types, ForeignKey
from sqlalchemy.orm import relationship
from .enums import EstadoCita
from uuid import uuid4

class Cita(db.Model):
    __tablename__ = 'citas'

    id = Column(primary_key=True, type_=types.UUID(), default=uuid4)

    pacienteId = Column(
        ForeignKey(column='pacientes.id'),
        nullable=False,
        name='paciente_id',
        type_=types.UUID()
    )

    medicoId = Column(
        ForeignKey(column='medicos.id'),
        nullable=False,
        name='medico_id',
        type_=types.UUID()
    )

    consultorioId = Column(
        ForeignKey(column='consultorios.id'),
        nullable=False,
        name='consultorio_id',
        type_=types.UUID()
    )

    fecha = Column(nullable=False, type_=types.Date)
    horaInicio = Column(name='hora_inicio', nullable=False, type_=types.Time)
    motivo = Column(type_=types.Text)
    estado = Column(nullable=False, type_=types.Enum(EstadoCita), default=EstadoCita.Confirmada)

    paciente = relationship('Paciente', backref='citas')

    medico = relationship('Medico', backref='citas')

    consultorio = relationship('Consultorio', backref='citas')
