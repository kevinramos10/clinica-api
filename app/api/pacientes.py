from flask_restful import Resource, request
from app.models import Paciente
from app.extensions import db
from app.schemas import PacienteSchema
from pydantic import ValidationError, TypeAdapter
from app.util import paginationInfo
from sqlalchemy.exc import IntegrityError

class PacientesController(Resource):
    
    def get(self):

        pagina = int(request.args.get('page', 1))
        porPagina = int(request.args.get('perPage', 10))

        offset = (pagina - 1) * porPagina
        limit = porPagina

        pacientes = db.session.query(Paciente).offset(offset).limit(limit).all()

        total = db.session.query(Paciente).count()

        pageInfo = paginationInfo(total, pagina, porPagina)

        adaptador = TypeAdapter(list[PacienteSchema])

        informacion = adaptador.validate_python(pacientes)

        return{
            'content': adaptador.dump_python(informacion, mode='json'),
            'pageInfo': pageInfo
        }

    def post(self):
        data = request.get_json()

        try:
            dataValidada = PacienteSchema.model_validate(data)

            dniExistente = db.session.query(Paciente).filter(Paciente.dni == dataValidada.dni).first()
            if dniExistente:
                return{
                    "message": "El DNI ya está registrado"
                }, 409

            if dataValidada.correo:
                correoExistente = db.session.query(Paciente).filter(Paciente.correo == dataValidada.correo).first()
                if correoExistente:
                    return{
                        "message": "El Correo ya está registrado"
                    }, 409

            nuevoPaciente = Paciente(**dataValidada.model_dump())

            db.session.add(nuevoPaciente)

            db.session.commit()

            resultado = PacienteSchema.model_validate(nuevoPaciente).model_dump(mode='json')

            return{
                "message": "Paciente creado exitosamente",
                "content": resultado
            }, 201

        except ValidationError as error:
            return{
                "message": "Error al crear el paciente",
                "content": error.errors()
            }

        except IntegrityError:
            db.session.rollback()
            return{
                "message": "El DNI o correo ya está registrado"
            }, 409

class PacienteController(Resource):
    
    def put(self, id):

        paciente = db.session.query(Paciente).filter(Paciente.id == id).first()

        if not paciente:
            return{
                "message": "Paciente no encontrado"
            }, 404        
        
        data = request.get_json()

        try:
            dataValidada = PacienteSchema.model_validate(data)

            dniExistente = db.session.query(Paciente).filter(Paciente.dni == dataValidada.dni).first()
            if dniExistente:
                return{
                    "message": "El DNI ya está registrado"
                }, 409

            if dataValidada.correo:
                correoExistente = db.session.query(Paciente).filter(Paciente.correo == dataValidada.correo).first()
                if correoExistente:
                    return{
                        "message": "El Correo ya está registrado"
                    }, 409

            paciente.dni = dataValidada.dni
            paciente.nombre = dataValidada.nombre
            paciente.apellidoPaterno = dataValidada.apellidoPaterno
            paciente.apellidoMaterno = dataValidada.apellidoMaterno
            paciente.telefono = dataValidada.telefono
            paciente.correo = dataValidada.correo
            paciente.fechaNacimiento = dataValidada.fechaNacimiento
            paciente.sexo = dataValidada.sexo
            paciente.direccion = dataValidada.direccion

            db.session.commit()

            resultado = PacienteSchema.model_validate(paciente).model_dump(mode='json')

            return{
                "message": "Paciente modificado exitosamente",
                "content": resultado
            }
        except ValidationError as error:
            return{
                "message": "Error al validar los datos del paciente",
                "content": error.errors()
            }

        except IntegrityError:
            db.session.rollback()
            return {
                "message": "El DNI o correo ya está registrado"
            }, 409

