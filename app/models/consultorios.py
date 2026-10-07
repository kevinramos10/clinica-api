from app.extensions import db
from sqlalchemy import Column, types
from uuid import uuid4

class Consultorio(db.Model):
    __tablename__ = 'consultorios'

    id = Column(primary_key=True, type_=types.UUID(), default=uuid4)
    numero = Column(unique=True, nullable=False, type_=types.VARCHAR(10))
    piso = Column(nullable=False, type_=types.Integer)
