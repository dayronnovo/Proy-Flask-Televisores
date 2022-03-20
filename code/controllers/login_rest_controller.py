from flask import Blueprint, request
from excepciones_personalizadas.excepciones import NotFound
from models.usuario import Usuario
from services.usuario_service import UsuarioService
from schemas.general_schemas import usuario_schema, usuario_schema_without_roles, role_schema, role_schema_without_usuarios
import bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
import jwt
from configs.basic_config import auth
login_controller = Blueprint('login_controller', __name__)


@login_controller.route("/", methods=['POST'], strict_slashes=False)
@auth.login_required
def login():
    try:

        user_email = request.form.get('user_email')
        password = request.form.get('password')

        if not (user_email and password):
            # Bad Request
            return {'Error': "user_email or password required"}, 400

        usuario: Usuario = UsuarioService.get_by_email(user_email)

        if bcrypt.checkpw(password.encode('utf-8'), usuario.password.encode('utf-8')):

            roles_list = [role.name for role in usuario.roles]

            access_token = create_access_token(
                identity={'user_name': usuario.user_name, 'email': usuario.email, 'active': usuario.active, 'authorities': roles_list}, fresh=True)
            refresh_token = create_refresh_token(
                identity={'user_name': usuario.user_name, 'email': usuario.email, 'active': usuario.active, 'authorities': roles_list})

            return {'access_token': access_token, 'refresh_token': refresh_token, 'client': auth.current_user()}

        else:
            return {'message': 'Invalid Credentials.'}, 401

    except NotFound as error:
        return {'message': 'Invalid Credentials.'}, 401
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@login_controller.route("/refresh", methods=['POST'], strict_slashes=False)
@jwt_required(refresh=True)
def refresh_token():
    try:

        identity = get_jwt_identity()

        access_token = create_access_token(
            identity=identity, fresh=False)
        refresh_token = create_refresh_token(
            identity=identity)

        return {'access_token': access_token, 'refresh_token': refresh_token}

        # return {'Error': "Usuario no encontrado."}, 404
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@login_controller.route("/create", methods=['POST'], strict_slashes=False)
def register():
    try:

        usuario: Usuario = usuario_schema_without_roles.load(
            request.get_json(), partial=("id",))
        usuario['password'] = bcrypt.hashpw(
            usuario['password'].encode('utf-8'), bcrypt.gensalt())
        UsuarioService.create(usuario)

        return {'message': 'Usuario creado con exito.'}

    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error
