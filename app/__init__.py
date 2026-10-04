from flask import Flask
from .config import config_map
from .extensions import db, migrate
from flask_restful import Api
from .api import PacientesController, PacienteController, MedicosController, MedicoController, EspecialidadesController, EspecialidadController, MedicosEspecialidadesController
from .models import *

def create_app(env = "development"):
    app = Flask(__name__)

    api = Api(app)

    app.config.from_object(config_map[env])

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/')
    def inicio():
        return "Hola, flask"

    #Pacientes
    api.add_resource(PacientesController, '/pacientes')
    api.add_resource(PacienteController, '/pacientes/<int:id>')

    #Medicos
    api.add_resource(MedicosController, '/medicos')
    api.add_resource(MedicoController, '/medicos/<int:id>')

    #Especialidad
    api.add_resource(EspecialidadesController, '/especialidades')
    api.add_resource(EspecialidadController, '/especialidades/<int:id>')

    #Medico-Especialidad
    api.add_resource(MedicosEspecialidadesController, '/medico-especialidades')
    
    return app
