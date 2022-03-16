from flask import Blueprint, request
from models.usuario import Usuario
from services.usuario_service import UsuarioService
from schemas.general_schemas import usuario_schema, usuario_schema_without_roles, role_schema, role_schema_without_usuarios
import bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
import jwt

login_controller = Blueprint('login_controller', __name__)


@login_controller.route("/", methods=['POST'], strict_slashes=False)
def login():
    try:
        # Tengo que validar esto con Marshmallow
        # email = request.get_json()['email']
        # password = request.get_json()['password']

        usuario_dict = usuario_schema_without_roles.load(
            request.get_json(), partial=("id",))
        print(usuario_dict)

        usuario: Usuario = UsuarioService.get_by_email(usuario_dict['email'])
        if usuario:

            if bcrypt.checkpw(usuario_dict['password'].encode('utf-8'), usuario.password.encode('utf-8')):

                roles_list = [role.name for role in usuario.roles]

                access_token = create_access_token(
                    identity={'email': usuario.email, 'authorities': roles_list}, fresh=True)
                refresh_token = create_refresh_token(
                    identity={'email': usuario.email, 'authorities': roles_list})

                return {'access_token': access_token, 'refresh_token': refresh_token}

            else:
                return {'message': 'Invalid Credentials.'}, 401

        else:
            return {'Error': "Usuario no encontrado."}, 404
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
            request.get_json())
        usuario['password'] = bcrypt.hashpw(
            usuario['password'].encode('utf-8'), bcrypt.gensalt())
        UsuarioService.create(usuario)

        return {'message': 'ok'}

    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error
