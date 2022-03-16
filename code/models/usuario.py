from conexion_bd_mysql import db
from models.role import association_table_usuario_role
from typing import List


class Usuario(db.Model):

    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # user_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    # relacion con multimedia
    roles: List = db.relationship(
        "Role", secondary=association_table_usuario_role, back_populates="usuarios")

    def __init__(self, id, email, password) -> None:
        self.id = id
        self.email = email
        self.password = password

    @classmethod
    def constructor(cls, data):
        return cls(data.get('id'), data['email'], data['password'])

    def __repr__(self) -> str:
        return f"Usuario => [id: {self.id}, email: {self.email}, password: {self.password}]"
