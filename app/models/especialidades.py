from app.extensions import db
from sqlalchemy import Column, types

class Especialidad(db.Model):
    __tablename__='especialidades'

    id = Column(autoincrement=True, primary_key=True, type_=types.Integer)
    nombre = Column(unique=True, nullable=False, type_=types.Text)
    