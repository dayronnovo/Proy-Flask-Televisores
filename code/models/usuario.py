from conexion_bd_mysql import db
from models.role import association_table_usuario_role
from typing import List


class Usuario(db.Model):

    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    # relacion con multimedia
    roles: List = db.relationship(
        "Role", secondary=association_table_usuario_role, back_populates="usuarios")

    def __init__(self, id, user_name, email, password, active) -> None:
        self.id = id
        self.user_name = user_name
        self.email = email
        self.password = password
        self.active = active

    @classmethod
    def constructor(cls, data):
        return cls(data.get('id'), data['user_name'], data['email'], data['password'], data['active'])

    def __repr__(self) -> str:
        return f"Usuario => [id: {self.id}, user_name: {self.user_name}, email: {self.email}, password: {self.password}, active: {self.active}]"
