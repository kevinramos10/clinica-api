from app.extensions import db
from sqlalchemy import Column, types, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4

class Historial(db.Model):
    __tablename__ = 'historiales'
    
    id = Column(primary_key=True, type_=types.UUID(), default=uuid4)

    citaId = Column(
            ForeignKey(column='citas.id'),
            nullable=False,
            name='cita_id',
            type_=types.UUID(),
            unique=True
        )

    diagnostico = Column(type_=types.Text)
    tratamiento = Column(type_=types.Text)
    observaciones = Column(type_=types.Text)
    fechaRegistro = Column(name='fecha_registro', nullable=False, type_=types.DateTime, default=datetime.now)

    cita = relationship('Cita', backref=db.backref('historial'))