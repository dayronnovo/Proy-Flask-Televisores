from conexion_bd_mysql import db
from models.televisor import Televisor
from models.cliente import Cliente
from models.multimedia import Multimedia
from models.historial_de_programacion import HistorialProgramacion
from typing import Dict, List
from flask_sqlalchemy import Pagination
from excepciones_personalizadas.excepciones import NotFound
from sqlalchemy import select
from services.cliente_service import ClienteService


class TelevisorService:
    NUMBER_OF_ENTITIES = 1

    @staticmethod
    def get_by_id(id: int):
        televisor = Televisor.query.filter_by(id=id).first()
        return televisor

    @staticmethod
    def create(data: Dict, cliente_id: int):
        televisor = Televisor.constructor(data)

        cliente: Cliente = ClienteService.get_by_id(cliente_id)
        if cliente:
            televisor.cliente = cliente

        db.session.add(televisor)
        db.session.commit()

    @staticmethod
    def get_televisores_by_cliente_id(id):
        televisores = Televisor.query.filter_by(cliente_id=id).all()
        return televisores

    @staticmethod
    def update(televisor: Televisor):
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
    def getMultimediasByClienteId(id):
        stmt = (select(Multimedia)).join(Televisor.multimedias).join(
            Televisor.cliente).where(Cliente.id == id)
        results = db.session.execute(stmt).unique().all()

        results = [multimedia_tupla[0] for multimedia_tupla in results]

        return results

    @staticmethod
    def get_by_ids(ids: List):

        stmt = (select(Televisor)).where(Televisor.id.in_(ids))
        results = db.session.execute(stmt).all()

        results = [televisor_tupla[0] for televisor_tupla in results]

        return results

    @staticmethod
    def getTelevisoresByHistorialIdWithPagination(id: int, page: int):

        televisores: Pagination = Televisor.query\
            .join(Televisor.historiales)\
            .where(HistorialProgramacion.id == id)\
            .paginate(
                page, per_page=TelevisorService.NUMBER_OF_ENTITIES, error_out=False)

        return televisores
