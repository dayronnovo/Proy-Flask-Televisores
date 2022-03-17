import string
from models.role import Role
from models.usuario import Usuario
from typing import Dict
from conexion_bd_mysql import db
from sqlalchemy import or_, select
from excepciones_personalizadas.excepciones import NotFound


class UsuarioService:

    @staticmethod
    def get_by_email(user_email: string):
        # usuario = Usuario.query.filter(
        #     or_(user_name=user_email, email=user_email)).one()

        stmt = (select(Usuario)).filter(
            or_(Usuario.user_name == user_email, Usuario.email == user_email))
        result = db.session.execute(stmt).first()
        if not result:
            raise NotFound
        return result[0]

    @staticmethod
    def create(usuario: Dict):
        usuario = Usuario.constructor(usuario)
        role_user = Role.query.filter_by(name='user').one()
        usuario.roles.append(role_user)

        db.session.add(usuario)
        db.session.commit()
