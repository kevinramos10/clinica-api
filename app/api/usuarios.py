from flask_restful import Resource, request
from app.models import Usuario
from app.extensions import db
from pydantic import ValidationError, TypeAdapter
from app.util import paginationInfo
from app.schemas import UsuarioSchema, LoginUsuarioSchema, CambiarPasswordSchema
from app.models.enums import RolUsuario, EstadoUsuario
from bcrypt import gensalt, hashpw, checkpw
from flask_jwt_extended import create_access_token, verify_jwt_in_request, get_jwt_identity, jwt_required

class UsuariosController(Resource):

    def get(self):
        verify_jwt_in_request(optional=True)

        idUsuario = get_jwt_identity()

        if idUsuario:
            usuario = db.session.query(Usuario).filter(
                Usuario.id == idUsuario,
                Usuario.estado == EstadoUsuario.Activo
            ).first()

            if not usuario:
                return {
                    'message': 'Usuario no encontrado'
                }, 404
            
            return {
                'content': UsuarioSchema.model_validate(usuario).model_dump(mode='json')
            }

        pagina = int(request.args.get('page', 1))
        porPagina = int(request.args.get('perPage', 10))

        offset = (pagina - 1) * porPagina
        limit = porPagina

        usuarios = db.session.query(Usuario).filter(
            Usuario.estado == EstadoUsuario.Activo
        ).offset(offset).limit(limit).all()

        total = db.session.query(Usuario).filter(
            Usuario.estado == EstadoUsuario.Activo
        ).count()

        pageInfo = paginationInfo(total, pagina, porPagina)

        adaptador = TypeAdapter(list[UsuarioSchema])

        informacion = adaptador.validate_python(usuarios)

        return{
            'content': adaptador.dump_python(informacion, mode='json'),
            'pageInfo': pageInfo
        }    

class RegistroController(Resource):
    
    def post(self):
        try:
            dataValidada = UsuarioSchema.model_validate(request.get_json())

            rol = dataValidada.rol

            if rol == RolUsuario.Medico:
                prefijo = "MED"
            elif rol == RolUsuario.Admin:
                prefijo = 'ADM'
            elif rol == RolUsuario.Recepcionista:
                prefijo = 'RECP'

            cantidad = db.session.query(Usuario).filter(Usuario.rol == rol).count()

            numero = cantidad + 1

            usuario = f"{prefijo}{numero:02d}"

            password = hashpw(dataValidada.password.encode(), gensalt()).decode()

            nuevoUsuario = Usuario(
                user=usuario,
                **dataValidada.model_dump(exclude={"password"}),
                password = password
            )

            db.session.add(nuevoUsuario)
            db.session.commit()

            return {
                'message': 'Usuario registrado exitosamente',
                'user': usuario
            }, 201
        except ValidationError as error:
            return{
                'message': 'Error al crear el usuario',
                'content': error.errors(include_context=False)
            }, 400


class LoginController(Resource):

    def post(self):
        try:
            dataValidada = LoginUsuarioSchema.model_validate(request.get_json())

            usuarioEncontrado = db.session.query(Usuario).filter(
                Usuario.user == dataValidada.user,
                Usuario.estado == EstadoUsuario.Activo
            ).first()

            if not usuarioEncontrado:
                return{
                    'message': 'Usuario no existe o esta inactivo'
                }, 404

            password = dataValidada.password.encode()
            hashedPassword = usuarioEncontrado.password.encode()

            esLaPassword = checkpw(password, hashedPassword)

            if esLaPassword:

                token = create_access_token(
                    identity=str(usuarioEncontrado.id)
                )
                
                return {
                    'message': 'Bienvenido',
                    'token': token
                }, 200
            
            else:
                return {
                    'message': 'Credenciales incorrectas'
                }, 401

        except ValidationError as error:
            return{
                'message': 'Error al crear el usuario',
                'content': error.errors(include_context=False)
            }, 400

class CambiarPasswordController(Resource):
    @jwt_required()
    def put(self):
        try:
            dataValidada = CambiarPasswordSchema.model_validate(request.get_json())

            idUsuario = get_jwt_identity()

            usuario = db.session.query(Usuario).filter(
                Usuario.id == idUsuario,
                Usuario.estado == EstadoUsuario.Activo
            ).first()

            if not usuario:
                return {
                    'message': 'Usuario no encontrado'
                }, 404

            passwordActual = dataValidada.passwordActual.encode()
            passwordGuardada = usuario.password.encode()

            if not checkpw(passwordActual, passwordGuardada):
                return {
                    'message': 'La contraseña actual es incorrecta'
                }, 401

            usuario.password = hashpw(dataValidada.passwordNueva.encode(), gensalt()).decode()

            db.session.commit()

            return {'message': 'Contraseña actualizada correctamente'}, 200
        
        except ValidationError as error:
            return {
                'message': 'Datos inválidos',
                'content': error.errors(include_context=False)
            }, 400

class DeleteController(Resource):
    def delete(self, id):
        usuario = db.session.query(Usuario).filter(
            Usuario.id == id,
            Usuario.estado == EstadoUsuario.Activo
        ).first()

        if not usuario:
            return {
                'message': 'Usuario no encontrado o inactivo'
            }, 404

        usuario.estado = EstadoUsuario.Inactivo
        db.session.commit()

        return {
            'message': 'Usuario desactivado correctamente'
        }, 200


















    