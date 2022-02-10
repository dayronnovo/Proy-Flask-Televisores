from models.cliente import Cliente
from conexion_bd_mysql import db
from typing import Dict, Union
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
        # error_out = True, si la página especificada no tiene contenido, se producirá un error 404; de lo contrario, se devolverá una lista vacía. (Yo quiero la lista vacia.)

        # return pagination.items  # items es una lista de objs del entity
        return pagination
