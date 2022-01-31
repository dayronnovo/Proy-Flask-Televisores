from models.multimedia import Multimedia
from models.cliente import Cliente
from conexion_bd_mysql import db
from excepciones_personalizadas.excepciones import NotFound
from messages.es_ES import messages
from typing import Dict
from flask_sqlalchemy import Pagination


class MultimediaService:
    NUMBER_OF_ENTITIES = 1

    @staticmethod
    def get_by_id(id: int):
        multimedia = Multimedia.query.filter_by(id=id).first()
        return multimedia

    @staticmethod
    def create(data: Dict):
        multimedia = Multimedia.constructor(data)

        cliente = Cliente.query.filter_by(id=data['cliente_id']).first()
        if not cliente:
            raise NotFound(messages['not_found'].format(data['cliente_id']))
        multimedia.cliente = cliente

        db.session.add(multimedia)
        db.session.commit()

    @staticmethod
    def get_all():
        multimedias = Multimedia.query.all()
        return multimedias

    @staticmethod
    def get_multimedias_by_cliente_id(id: int, page: int):

        multimedias: Pagination = Multimedia.query.filter_by(cliente_id=id).paginate(
            page, per_page=MultimediaService.NUMBER_OF_ENTITIES, error_out=False)
        return multimedias

    # @staticmethod
    # def get_all_pagination(page):

    #     pagination = Multimedia.query.order_by(Multimedia.id.desc()).paginate(
    #         page, per_page=MultimediaService.NUMBER_OF_ENTITIES, error_out=False)

    #     return pagination.items
