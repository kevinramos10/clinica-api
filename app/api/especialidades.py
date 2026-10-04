from flask_restful import Resource, request
from app.models import Especialidad
from app.extensions import db
from app.schemas import EspecialidadSchema
from pydantic import ValidationError, TypeAdapter

class EspecialidadesController(Resource):

    def get(self):

        especialidades = db.session.query(Especialidad).all()

        adaptador = TypeAdapter(list[EspecialidadSchema])

        informacion = adaptador.validate_python(especialidades)

        return{
            'content': adaptador.dump_python(informacion, mode="json")
        }

    def post(self):

        data = request.get_json()

        try:
            dataValidada = EspecialidadSchema.model_validate(data)

            nuevaEspecilidad = Especialidad(**dataValidada.model_dump())

            db.session.add(nuevaEspecilidad)

            db.session.commit()

            resultado = EspecialidadSchema.model_validate(nuevaEspecilidad).model_dump(mode='json')

            return{
                "message": "Especialidad creada exitosamente",
                "content": resultado
            }, 201

        except ValidationError as error:
            return{
                "message": "Error al crear la especialidad",
                "content": error.errors()
            }

class EspecialidadController(Resource):

    def put(self, id):

        especialidad = db.session.query(Especialidad).filter(Especialidad.id == id).first()

        if not especialidad:
            return{
                "message": "Especialidad no encontrada"
            }, 404

        data = request.get_json()

        dataValidada = EspecialidadSchema.model_validate(data)

        especialidad.nombre = dataValidada.nombre

        db.session.commit()

        resultado = EspecialidadSchema.model_validate(especialidad).model_dump(mode='json')

        return{
            "message": "Especialidad modificada exitosamente",
            "content": resultado
        }

    def delete(self, id):

        especialidad = db.session.query(Especialidad).filter(Especialidad.id == id).first()

        if not especialidad:
            return{
                "message": "Especialidad no encontrada"
            },404

        db.session.delete(especialidad)
        db.session.commit()

        return{
            "message": "Especialidad eliminada exitosamente"
        }

        