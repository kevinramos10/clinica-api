from app.extensions import db
from sqlalchemy import Column, types
from .enums import SexoPersona

class Paciente(db.Model):
    __tablename__ = 'pacientes'

    id = Column(autoincrement=True, primary_key=True, type_=types.Integer)
    dni = Column(unique=True, nullable=False, type_=types.VARCHAR(20))
    nombre = Column(nullable=False, type_=types.Text)
    apellidoPaterno = Column(name='apellido_paterno', nullable=False, type_=types.Text)
    apellidoMaterno = Column(name='apellido_materno', nullable=False, type_=types.Text)
    telefono = Column(nullable=False, type_=types.Text)
    correo = Column(unique=True, type_=types.Text)
    fechaNacimiento = Column(name='fecha_nacimiento', nullable=False, type_=types.Date)
    sexo = Column(nullable=False, type_=types.Enum(SexoPersona))
    direccion = Column(type_=types.Text)
