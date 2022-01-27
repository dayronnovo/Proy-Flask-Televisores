from models.cliente import Cliente
from conexion_bd_mysql import db
from typing import Dict


class ClienteService:

    @staticmethod
    def get_by_id(id: int):
        cliente = Cliente.query.filter_by(id=id).first()
        return cliente

    @staticmethod
    def create(data: Dict):
        cliente = Cliente.constructor(data)
        db.session.add(cliente)
        db.session.commit()

    @staticmethod
    def get_all():
        clientes = Cliente.query.all()
        return clientes
