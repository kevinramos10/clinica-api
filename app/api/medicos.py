from flask_restful import Resource, request
from app.models import Medico
from app.extensions import db
from app.schemas import MedicoSchema
from pydantic import ValidationError, TypeAdapter
from app.models.enums import EstadoMedico
from sqlalchemy import or_
from datetime import date
from app.util import paginationInfo

class MedicosController(Resource):

    def get(self):

        pagina = int(request.args.get('page', 1))
        porPagina = int(request.args.get('perPage', 10))

        offset = (pagina - 1) * porPagina
        limit = porPagina

        medicos = db.session.query(Medico).filter(
            or_(
                Medico.estado == EstadoMedico.Activo,
                Medico.estado == EstadoMedico.De_Vacaciones
            )            
        ).offset(offset).limit(limit).all()

        total = db.session.query(Medico).filter(
            or_(
                Medico.estado == EstadoMedico.Activo,
                Medico.estado == EstadoMedico.De_Vacaciones
            )
        ).count()

        pageInfo = paginationInfo(total, pagina, porPagina)

        adaptador = TypeAdapter(list[MedicoSchema])

        informacion = adaptador.validate_python(medicos)

        return{
            'content': adaptador.dump_python(informacion, mode='json'),
            'pageInfo': pageInfo
        }

    def post(self):
        data = request.get_json()

        try:
            dataValidada = MedicoSchema.model_validate(data)

            nuevoMedico = Medico(**dataValidada.model_dump())

            db.session.add(nuevoMedico)

            db.session.commit()

            resultado = MedicoSchema.model_validate(nuevoMedico).model_dump(mode='json')

            return{
                "message": "Medico creado exitosamente",
                "content": resultado
            }, 201

        except ValidationError as error:
            return{
                "message": "Error al crear el medico",
                "content": error.errors()
            }

class MedicoController(Resource):

    def put(self, id):

        medico = db.session.query(Medico).filter(Medico.id == id).first()

        if not medico:
            return{
                "message": "Medico no encontrado"
            }, 404

        data = request.get_json()

        dataValidada = MedicoSchema.model_validate(data)

        medico.dni = dataValidada.dni
        medico.colegiatura = dataValidada.colegiatura
        medico.nombre = dataValidada.nombre
        medico.apellidoPaterno = dataValidada.apellidoPaterno
        medico.apellidoMaterno = dataValidada.apellidoMaterno
        medico.sexo = dataValidada.sexo
        medico.telefono = dataValidada.telefono
        medico.correo = dataValidada.correo
        medico.fechaNacimiento = dataValidada.fechaNacimiento
        medico.estado = dataValidada.estado

        db.session.commit()

        resultado = MedicoSchema.model_validate(medico).model_dump(mode='json')

        return{
            "message": "Medico modificado exitosamente",
            "content": resultado
        }


    def delete(self, id):
        medico = db.session.query(Medico).filter(
            Medico.id == id, 
            Medico.estado == EstadoMedico.Activo
        ).first()

        if not medico:
            return{
                "message": "Medico no encontrado"
            }, 404

        db.session.query(Medico).filter(medico.id == id).update({
            Medico.estado: EstadoMedico.Inactivo
        })

        db.session.commit()

        return{
            "message": "Medico eliminado exitosamente"
        }

    def get(self, id):

        medicoEncontrado = db.session.query(Medico).filter(Medico.id == id).first()

        if not medicoEncontrado:
            return{
                'message': 'Medico con ese id no existe'
            }, 404

        especialidades = []

        for medicoEspecilidad in medicoEncontrado.medico_especialidades:
            especialidades.append({
                "id": str(medicoEspecilidad.especialidad.id),
                "nombre": medicoEspecilidad.especialidad.nombre
            })

        resultado = {
            "id": str(medicoEncontrado.id),
            "dni": medicoEncontrado.dni,
            "colegiatura": medicoEncontrado.colegiatura,
            "nombre": medicoEncontrado.nombre,
            "apellidoPaterno": medicoEncontrado.apellidoPaterno,
            "apellidoMaterno": medicoEncontrado.apellidoMaterno,
            "sexo": medicoEncontrado.sexo.value,
            "telefono": medicoEncontrado.telefono,
            "correo": medicoEncontrado.correo,
            "fechaNacimiento": date.strftime(medicoEncontrado.fechaNacimiento, "%Y-%m-%d") ,
            "estado": medicoEncontrado.estado.value,
            "especialidades": especialidades
        }

        return{
            'content': resultado
        }
        