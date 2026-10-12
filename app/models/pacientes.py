from app.extensions import db
from sqlalchemy import Column, types
from .enums import SexoPersona
from uuid import uuid4

class Paciente(db.Model):
    __tablename__ = 'pacientes'

    id = Column(type_=types.UUID(), default=uuid4, primary_key=True)
    dni = Column(unique=True, nullable=False, type_=types.VARCHAR(20))
    nombre = Column(nullable=False, type_=types.Text)
    apellidoPaterno = Column(name='apellido_paterno', nullable=False, type_=types.Text)
    apellidoMaterno = Column(name='apellido_materno', nullable=False, type_=types.Text)
    telefono = Column(nullable=False, type_=types.Text)
    correo = Column(unique=True, type_=types.Text)
    fechaNacimiento = Column(name='fecha_nacimiento', nullable=False, type_=types.Date)
    sexo = Column(nullable=False, type_=types.Enum(SexoPersona))
    direccion = Column(type_=types.Text)
