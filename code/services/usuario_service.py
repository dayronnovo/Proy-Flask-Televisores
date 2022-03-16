import string
from models.role import Role
from models.usuario import Usuario
from typing import Dict
from conexion_bd_mysql import db


class UsuarioService:

    @staticmethod
    def get_by_email(email: string):
        usuario = Usuario.query.filter_by(email=email).one()
        return usuario

    @staticmethod
    def create(usuario: Dict):
        usuario = Usuario.constructor(usuario)
        role_user = Role.query.filter_by(name='user').one()
        usuario.roles.append(role_user)

        db.session.add(usuario)
        db.session.commit()
