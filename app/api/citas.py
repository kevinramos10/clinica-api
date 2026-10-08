from flask_restful import Resource, request
from app.models import Cita, Paciente, Medico, Consultorio
from app.extensions import db
from app.schemas import CitaSchema
from pydantic import ValidationError, TypeAdapter
from app.models.enums import EstadoCita, EstadoMedico
from datetime import date, datetime, timedelta

duracionCita = timedelta(minutes=30)

def validarRelaciones(dataValidada):

    pacienteEncontrado = db.session.query(Paciente).filter(Paciente.id == dataValidada.pacienteId).first()

    if not pacienteEncontrado:
        return f'El paciente {dataValidada.pacienteId} no existe'

    medicoEncontrado = db.session.query(Medico).filter(
        Medico.id == dataValidada.medicoId,
        Medico.estado == EstadoMedico.Activo
    ).first()

    if not medicoEncontrado:
        return f'El medico {dataValidada.medicoId} no existe o no esta activo'

    consultorioEncontrado = db.session.query(Consultorio).filter(Consultorio.id == dataValidada.consultorioId).first()

    if not consultorioEncontrado:
        return f'El consultorio {dataValidada.consultorioId} no existe'

    return None

def validarHorario(dataValidada, idCita = None):

    if dataValidada.estado == EstadoCita.Cancelada:
        return None

    inicioCita = datetime.combine(dataValidada.fecha, dataValidada.horaInicio)

    horaDesde = (inicioCita - duracionCita).time()
    horaHasta = (inicioCita + duracionCita).time()

    citasEnHorario = db.session.query(Cita).filter(
        Cita.fecha == dataValidada.fecha,
        Cita.horaInicio > horaDesde,
        Cita.horaInicio < horaHasta,
        Cita.estado != EstadoCita.Cancelada
    )

    if idCita:
        citasEnHorario = citasEnHorario.filter(Cita.id != idCita)

    if citasEnHorario.filter(Cita.medicoId == dataValidada.medicoId).first():
        return 'El medico ya tiene una cita en ese horario'

    if citasEnHorario.filter(Cita.consultorioId == dataValidada.consultorioId).first():
        return 'El consultorio ya esta ocupado en ese horario'

    if citasEnHorario.filter(Cita.pacienteId == dataValidada.pacienteId).first():
        return 'El paciente ya tiene una cita en ese horario'

    return None

class CitasController(Resource):

    def get(self):

        citas = db.session.query(Cita).filter(
            Cita.estado != EstadoCita.Cancelada
        ).all()

        adaptador = TypeAdapter(list[CitaSchema])

        informacion = adaptador.validate_python(citas)

        return{
            'content': adaptador.dump_python(informacion, mode='json')
        }

    def post(self):
        data = request.get_json()

        try:
            dataValidada = CitaSchema.model_validate(data)

            mensajeError = validarRelaciones(dataValidada)

            if mensajeError:
                return{
                    "message": mensajeError
                }, 400

            mensajeError = validarHorario(dataValidada)

            if mensajeError:
                return{
                    "message": mensajeError
                }, 400

            nuevaCita = Cita(**dataValidada.model_dump())

            db.session.add(nuevaCita)

            db.session.commit()

            resultado = CitaSchema.model_validate(nuevaCita).model_dump(mode='json')

            return{
                "message": "Cita creada exitosamente",
                "content": resultado
            }, 201

        except ValidationError as error:
            return{
                "message": "Error al crear la cita",
                "content": error.errors()
            }, 400

class CitaController(Resource):

    def get(self, id):

        citaEncontrada = db.session.query(Cita).filter(Cita.id == id).first()

        if not citaEncontrada:
            return{
                'message': 'Cita con ese id no existe'
            }, 404

        resultado = {
            "id": str(citaEncontrada.id),
            "fecha": date.strftime(citaEncontrada.fecha, "%Y-%m-%d"),
            "horaInicio": citaEncontrada.horaInicio.strftime("%H:%M"),
            "motivo": citaEncontrada.motivo,
            "estado": citaEncontrada.estado.value,
            "paciente": {
                "id": str(citaEncontrada.paciente.id),
                "dni": citaEncontrada.paciente.dni,
                "nombre": citaEncontrada.paciente.nombre,
                "apellidoPaterno": citaEncontrada.paciente.apellidoPaterno,
                "apellidoMaterno": citaEncontrada.paciente.apellidoMaterno
            },
            "medico": {
                "id": str(citaEncontrada.medico.id),
                "nombre": citaEncontrada.medico.nombre,
                "apellidoPaterno": citaEncontrada.medico.apellidoPaterno,
                "apellidoMaterno": citaEncontrada.medico.apellidoMaterno
            },
            "consultorio": {
                "id": str(citaEncontrada.consultorio.id),
                "numero": citaEncontrada.consultorio.numero,
                "piso": citaEncontrada.consultorio.piso
            }
        }

        return{
            'content': resultado
        }

    def put(self, id):

        cita = db.session.query(Cita).filter(Cita.id == id).first()

        if not cita:
            return{
                "message": "Cita no encontrada"
            }, 404

        data = request.get_json()

        try:
            dataValidada = CitaSchema.model_validate(data)

            mensajeError = validarRelaciones(dataValidada)

            if mensajeError:
                return{
                    "message": mensajeError
                }, 400

            mensajeError = validarHorario(dataValidada, id)

            if mensajeError:
                return{
                    "message": mensajeError
                }, 400

            cita.pacienteId = dataValidada.pacienteId
            cita.medicoId = dataValidada.medicoId
            cita.consultorioId = dataValidada.consultorioId
            cita.fecha = dataValidada.fecha
            cita.horaInicio = dataValidada.horaInicio
            cita.motivo = dataValidada.motivo
            cita.estado = dataValidada.estado

            db.session.commit()

            resultado = CitaSchema.model_validate(cita).model_dump(mode='json')

            return{
                "message": "Cita modificada exitosamente",
                "content": resultado
            }

        except ValidationError as error:
            return{
                "message": "Error al modificar la cita",
                "content": error.errors()
            }, 400

    def delete(self, id):

        cita = db.session.query(Cita).filter(
            Cita.id == id,
            Cita.estado == EstadoCita.Confirmada
        ).first()

        if not cita:
            return{
                "message": "Cita no encontrada"
            }, 404

        cita.estado = EstadoCita.Cancelada

        db.session.commit()

        return{
            "message": "Cita cancelada exitosamente"
        }
