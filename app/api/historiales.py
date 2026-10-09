from flask_restful import Resource, request
from app.models import Historial, Cita
from app.extensions import db
from app.schemas import HistorialSchema
from pydantic import ValidationError, TypeAdapter
from app.models.enums import EstadoCita

def validarCita(dataValidada):

    citaEncontrada = db.session.query(Cita).filter(Cita.id == dataValidada.citaId).first()

    if not citaEncontrada:
        return f'La cita {dataValidada.citaId} no existe'

    if citaEncontrada.estado == EstadoCita.Cancelada:
        return 'No se puede registrar un historial de una cita cancelada'

    historialEncontrado = db.session.query(Historial).filter(Historial.citaId == dataValidada.citaId).first()

    if historialEncontrado:
        return 'La cita ya tiene un historial registrado'

    return None

class HistorialesController(Resource):

    def get(self):

        historiales = db.session.query(Historial).all()

        adaptador = TypeAdapter(list[HistorialSchema])

        informacion = adaptador.validate_python(historiales)

        return{
            'content': adaptador.dump_python(informacion, mode='json')
        }

    def post(self):
        data = request.get_json()

        try:
            dataValidada = HistorialSchema.model_validate(data)

            mensajeError = validarCita(dataValidada)

            if mensajeError:
                return{
                    "message": mensajeError
                }, 400

            nuevoHistorial = Historial(**dataValidada.model_dump())

            db.session.add(nuevoHistorial)

            db.session.commit()

            resultado = HistorialSchema.model_validate(nuevoHistorial).model_dump(mode='json')

            return{
                "message": "Historial creado exitosamente",
                "content": resultado
            }, 201

        except ValidationError as error:
            return{
                "message": "Error al crear el historial",
                "content": error.errors()
            }, 400

class HistorialController(Resource):

    def get(self, id):

        historialEncontrado = db.session.query(Historial).filter(Historial.id == id).first()

        if not historialEncontrado:
            return{
                'message': 'Historial con ese id no existe'
            }, 404

        cita = historialEncontrado.cita

        resultado = {
            "id": str(historialEncontrado.id),
            "diagnostico": historialEncontrado.diagnostico,
            "tratamiento": historialEncontrado.tratamiento,
            "observaciones": historialEncontrado.observaciones,
            "fechaRegistro": historialEncontrado.fechaRegistro.strftime("%Y-%m-%d %H:%M"),
            "cita": {
                "id": str(cita.id),
                "fecha": cita.fecha.strftime("%Y-%m-%d"),
                "horaInicio": cita.horaInicio.strftime("%H:%M"),
                "motivo": cita.motivo,
                "estado": cita.estado.value
            },
            "paciente": {
                "id": str(cita.paciente.id),
                "dni": cita.paciente.dni,
                "nombre": cita.paciente.nombre,
                "apellidoPaterno": cita.paciente.apellidoPaterno,
                "apellidoMaterno": cita.paciente.apellidoMaterno
            },
            "medico": {
                "id": str(cita.medico.id),
                "nombre": cita.medico.nombre,
                "apellidoPaterno": cita.medico.apellidoPaterno,
                "apellidoMaterno": cita.medico.apellidoMaterno
            }
        }

        return{
            'content': resultado
        }