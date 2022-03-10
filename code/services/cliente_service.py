from models.cliente import Cliente
from models.multimedia import Multimedia
from conexion_bd_mysql import db
from typing import Dict
from flask_sqlalchemy import Pagination


class ClienteService:
    NUMBER_OF_ENTITIES = 2

    @staticmethod
    def get_by_id(id: int):
        cliente = Cliente.query.filter_by(id=id).first()
        return cliente

    @staticmethod
    def save(data: Dict):
        data = Cliente.constructor(data)
        db.session.add(data)
        db.session.commit()

    @staticmethod
    def update(data: Cliente):
        db.session.commit()

    @staticmethod
    def get_all_pagination(page):

        pagination: Pagination = Cliente.query.order_by(Cliente.id).paginate(
            page, per_page=ClienteService.NUMBER_OF_ENTITIES, error_out=False)

        return pagination

    @staticmethod
    def agregar_multimedias_a_un_cliente(data_dict: Dict, cliente_id):
        cliente: Cliente = ClienteService.get_by_id(cliente_id)
        multimedia: Multimedia = Multimedia.constructor(data_dict)

        cliente.multimedias.append(multimedia)

        db.session.add(cliente)
        db.session.commit()
