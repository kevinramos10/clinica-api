from app.extensions import db
from sqlalchemy import Column, types
from .enums import SexoPersona, EstadoMedico
from uuid import uuid4

class Medico(db.Model):
    __tablename__='medicos'

    id = Column(primary_key=True, type_=types.UUID(), default=uuid4)
    dni = Column(unique=True, nullable=False, type_=types.VARCHAR(20))
    colegiatura = Column(unique=True, nullable=False, type_=types.VARCHAR(20))
    nombre = Column(nullable=False, type_=types.Text)
    apellidoPaterno = Column(name='apellido_paterno', nullable=False, type_=types.Text)
    apellidoMaterno = Column(name='apellido_materno', nullable=False, type_=types.Text)
    sexo = Column(nullable=False, type_=types.Enum(SexoPersona))
    telefono = Column(nullable=False, type_=types.Text)
    correo = Column(nullable=False, unique=True, type_=types.Text)
    fechaNacimiento = Column(name='fecha_nacimiento', nullable=False, type_=types.Date)
    estado = Column(nullable=False, type_=types.Enum(EstadoMedico), default=EstadoMedico.Activo)




