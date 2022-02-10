from conexion_bd_mysql import db
from models.televisor import Televisor
from models.cliente import Cliente
from typing import Dict
from flask_sqlalchemy import Pagination
from excepciones_personalizadas.excepciones import NotFound


class TelevisorService:
    NUMBER_OF_ENTITIES = 1

    @staticmethod
    def get_by_id(id: int):
        televisor = Televisor.query.filter_by(id=id).first()
        return televisor

    @staticmethod
    def save(data: Dict):
        televisor = Televisor.constructor(data)
        cliente = Cliente.query.filter_by(id=data['cliente_id']).first()
        if not cliente:
            raise NotFound(f"El cliente con el id: {data['autor_id']} no existe")
        televisor.cliente = cliente
        db.session.add(televisor)
        db.session.commit()

    @staticmethod
    def create(data: Dict):
        televisor = Televisor.constructor(data)
        db.session.add(televisor)
        db.session.commit()

    @staticmethod
    def save(televisor: Televisor):

        db.session.add(televisor)
        db.session.commit()

    @staticmethod
    def get_all_pagination(page):

        pagination: Pagination = Televisor.query.order_by(Televisor.id).paginate(
            page, per_page=TelevisorService.NUMBER_OF_ENTITIES, error_out=False)
        return pagination

    @staticmethod
    def get_televisores_by_cliente_id_with_pagination(id: int, page: int):

        televisores: Pagination = Televisor.query.filter_by(cliente_id=id).paginate(
            page, per_page=TelevisorService.NUMBER_OF_ENTITIES, error_out=False)
        return televisores

    @staticmethod
    def get_televisores_by_cliente_id(id):
        televisores = Televisor.query.filter_by(cliente_id=id).all()
        return televisores
