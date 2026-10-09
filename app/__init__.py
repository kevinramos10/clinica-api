
from flask import Flask
from .config import config_map
from .extensions import db, migrate
from flask_restful import Api
from .api import (
    PacientesController, PacienteController,
    MedicosController, MedicoController,
    EspecialidadesController, EspecialidadController,
    MedicosEspecialidadesController, MedicoEspecialidadController,
    ConsultoriosController, ConsultorioController,
    CitasController, CitaController,
    RegistroController, UsuariosController, LoginController,
    CambiarPasswordController, DeleteController,
    HistorialController, HistorialesController
)
from .models import *
from flask_jwt_extended import JWTManager


def create_app(env="development"):
    app = Flask(__name__)

    app.config.from_object(config_map[env])
    JWTManager(app)

    api = Api(app)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/')
    def inicio():
        return "Hola, flask"

    # Pacientes
    api.add_resource(PacientesController, '/pacientes')
    api.add_resource(PacienteController, '/pacientes/<uuid:id>')

    # Médicos
    api.add_resource(MedicosController, '/medicos')
    api.add_resource(MedicoController, '/medicos/<uuid:id>')

    # Especialidades
    api.add_resource(EspecialidadesController, '/especialidades')
    api.add_resource(EspecialidadController, '/especialidades/<uuid:id>')

    # Médico-Especialidad
    api.add_resource(MedicosEspecialidadesController, '/medico-especialidades')
    api.add_resource(
        MedicoEspecialidadController,
        '/medico-especialidad/<uuid:idMedico>/<uuid:idEspecialidad>'
    )

    # Consultorios
    api.add_resource(ConsultoriosController, '/consultorios')
    api.add_resource(ConsultorioController, '/consultorios/<uuid:id>')

    # Citas
    api.add_resource(CitasController, '/citas')
    api.add_resource(CitaController, '/citas/<uuid:id>')

    # Usuarios
    api.add_resource(UsuariosController, '/usuarios')
    api.add_resource(RegistroController, '/registro')
    api.add_resource(LoginController, '/login')
    api.add_resource(CambiarPasswordController, '/password')
    api.add_resource(DeleteController, '/delete/<uuid:id>')

    # Historiales
    api.add_resource(HistorialesController, '/historiales')
    api.add_resource(HistorialController, '/historiales/<uuid:id>')

    return app