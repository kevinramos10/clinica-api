from app.extensions import db
from sqlalchemy import Column, types, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4
from .enums import RolUsuario, EstadoUsuario

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = Column(type_=types.UUID(), default=uuid4, primary_key=True)
    user = Column(type_=types.VARCHAR(10), nullable=False, unique=True)
    password = Column(type_=types.Text, nullable=False)
    rol = Column(type_=types.Enum(RolUsuario), nullable=False)
    estado = Column(type_=types.Enum(EstadoUsuario), nullable=False, default=EstadoUsuario.Activo)
    medicoId = Column(ForeignKey('medicos.id'), name='medico_id', type_=types.UUID(), unique=True, nullable=True)

    medico = relationship('Medico', backref='usuario')