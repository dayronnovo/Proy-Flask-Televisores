from models.televisor import Televisor
from models.multimedia import Multimedia
from models.cliente import Cliente
from conexion_bd_mysql import db
from excepciones_personalizadas.excepciones import NotFound
from messages.es_ES import messages
from typing import Dict
from flask_sqlalchemy import Pagination
from werkzeug.datastructures import FileStorage
import json


class MultimediaService:
    NUMBER_OF_ENTITIES = 1

    @staticmethod
    def get_by_id(id: int):
        multimedia = Multimedia.query.filter_by(id=id).first()
        return multimedia

    @staticmethod
    def create(data: Dict, idsClientes: Dict):
        # print(data)
        print(idsClientes)

        multimedia = Multimedia.constructor(data)
        Televisor.query.filter_by(cliente_id=id).all()
        televisores = Televisor.query.filter(Televisor.id.in_(idsClientes['ids'])).all()

        multimedia.televisores = televisores

        db.session.add(multimedia)
        db.session.commit()

        # @staticmethod
        # def get_multimedias_by_cliente_id(id: int, page: int):

        #     multimedias: Pagination = Multimedia.query.filter_by(cliente_id=id).paginate(
        #         page, per_page=MultimediaService.NUMBER_OF_ENTITIES, error_out=False)
        #     return multimedias
