from app.extensions import db
from sqlalchemy import Column, types
from uuid import uuid4

class Especialidad(db.Model):
    __tablename__='especialidades'

    id = Column(primary_key=True, type_=types.UUID(), default=uuid4)
    nombre = Column(unique=True, nullable=False, type_=types.Text)
    