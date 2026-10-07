from flask_restful import Resource, request
from app.models import Consultorio
from app.extensions import db
from app.schemas import ConsultorioSchema
from pydantic import ValidationError, TypeAdapter

class ConsultoriosController(Resource):

    def get(self):

        consultorios = db.session.query(Consultorio).all()

        adaptador = TypeAdapter(list[ConsultorioSchema])

        informacion = adaptador.validate_python(consultorios)

        return{
            'content': adaptador.dump_python(informacion, mode='json')
        }

    def post(self):
        data = request.get_json()

        try:
            dataValidada = ConsultorioSchema.model_validate(data)

            nuevoConsultorio = Consultorio(**dataValidada.model_dump())

            db.session.add(nuevoConsultorio)

            db.session.commit()

            resultado = ConsultorioSchema.model_validate(nuevoConsultorio).model_dump(mode='json')

            return{
                "message": "Consultorio creado exitosamente",
                "content": resultado
            }, 201

        except ValidationError as error:
            return{
                "message": "Error al crear el consultorio",
                "content": error.errors()
            }, 400

class ConsultorioController(Resource):

    def get(self, id):

        consultorioEncontrado = db.session.query(Consultorio).filter(Consultorio.id == id).first()

        if not consultorioEncontrado:
            return{
                'message': 'Consultorio con ese id no existe'
            }, 404

        resultado = ConsultorioSchema.model_validate(consultorioEncontrado).model_dump(mode='json')

        return{
            'content': resultado
        }

    def put(self, id):

        consultorio = db.session.query(Consultorio).filter(Consultorio.id == id).first()

        if not consultorio:
            return{
                "message": "Consultorio no encontrado"
            }, 404

        data = request.get_json()

        try:
            dataValidada = ConsultorioSchema.model_validate(data)

            consultorio.numero = dataValidada.numero
            consultorio.piso = dataValidada.piso

            db.session.commit()

            resultado = ConsultorioSchema.model_validate(consultorio).model_dump(mode='json')

            return{
                "message": "Consultorio modificado exitosamente",
                "content": resultado
            }

        except ValidationError as error:
            return{
                "message": "Error al modificar el consultorio",
                "content": error.errors()
            }, 400

    def delete(self, id):

        consultorio = db.session.query(Consultorio).filter(Consultorio.id == id).first()

        if not consultorio:
            return{
                "message": "Consultorio no encontrado"
            }, 404

        db.session.delete(consultorio)
        db.session.commit()

        return{
            "message": "Consultorio eliminado exitosamente"
        }
