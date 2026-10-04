from flask_restful import Resource, request
from app.extensions import db
from app.models import MedicoEspecialidad, Especialidad
from app.schemas import MedicosEspecialidadesSchema
from pydantic import ValidationError

class MedicosEspecialidadesController(Resource):

    def post(self):

        try:
            dataValidada = MedicosEspecialidadesSchema.model_validate(request.get_json())

            registros = db.session.query(MedicoEspecialidad).with_entities(
                MedicoEspecialidad.especialidadId
            ).filter(
                MedicoEspecialidad.medicoId == dataValidada.medicoId
            ).all()

            registrosIds = [fila[0] for fila in registros]

            especialidadesAAgregar = []

            for especialidadId in dataValidada.especialidadIds:
                if especialidadId not in registrosIds:
                    especialidadesAAgregar.append(especialidadId)

            for especialidad in especialidadesAAgregar:

                especialidadEncontrada = db.session.query(Especialidad).with_entities(
                    Especialidad.id
                ).filter(
                    Especialidad.id == especialidad
                ).first()

                if not especialidadEncontrada:
                    return{
                        'meesage': f'La especialidad {especialidad} no existe'
                    }, 400

                nuevoMedicoEspecialidad = MedicoEspecialidad(
                    especialidadId = especialidad,
                    medicoId = dataValidada.medicoId
                )

                db.session.add(nuevoMedicoEspecialidad)

            db.session.commit()
            return {
                'message': 'Especialidades agregadas al medico exitosamente'
            }, 201

        except ValidationError as error:
            return {
                'message':'Error al asignar las especialidades al medico',
                'content': error.errors()
            }

