from models.televisor import Televisor
from models.multimedia import Multimedia
from models.cliente import Cliente
from conexion_bd_mysql import db
from excepciones_personalizadas.excepciones import NotFound
from messages.es_ES import messages
from typing import Dict, List
from flask_sqlalchemy import Pagination
from werkzeug.datastructures import FileStorage
import json
import os
from sqlalchemy import delete, select

CARPETA = os.path.abspath("./code/uploads/")


class MultimediaService:
    NUMBER_OF_ENTITIES = 1

    @staticmethod
    def get_by_id(id: int):
        multimedia = Multimedia.query.filter_by(id=id).first()
        return multimedia

    @staticmethod
    def create(data: Dict, idsClientes: Dict):
        # print(data)
        # print(idsClientes)

        multimedia = Multimedia.constructor(data)
        Televisor.query.filter_by(cliente_id=id).all()
        televisores = Televisor.query.filter(Televisor.id.in_(idsClientes['ids'])).all()

        multimedia.televisores = televisores

        db.session.add(multimedia)
        db.session.commit()

    @staticmethod
    def borrarMultimedias():
        # Ver mas tarde como hacerlo mejor
        multimedias_empty_tuplas = db.engine.execute(
            "SELECT m.id, m.archivo FROM  multimedias m WHERE m.id NOT IN (SELECT tlm.multimedia_id FROM televisor_multimedia tlm)").all()
        ids_list = []

        for multimedia in multimedias_empty_tuplas:
            os.remove(os.path.join(CARPETA, multimedia[1]))
            ids_list.append(multimedia[0])

        sql1 = delete(Multimedia).where(Multimedia.id.in_(ids_list))
        db.session.execute(sql1)
        db.session.commit()

    @staticmethod
    def getMultimediasByClienteId(id):
        stmt = (select(Multimedia)).join(Televisor.multimedias).join(Televisor.cliente).where(Cliente.id == id)
        results = db.session.execute(stmt).unique().all()
        # Lo que devuelve
        # [(Multimedia => [id: 68, archivo: 4a011513e36f45ae905afb592be47c0f.png],), (Multimedia => [id: 69, archivo: 6500e83ebe82410c97079050f4fc69c8.png],), (Multimedia => [id: 70, archivo: 2c693cc38a3c48a0ae360629d19b8c7d.png],), (Multimedia => [id: 71, archivo: d867d9166cf44f15961487545c6b559a.png],)]

        results = [multimedia_tupla[0] for multimedia_tupla in results]

        return results

    # @staticmethod
    # def delete(ids: List):
    #     sql1 = delete(Multimedia).where(Multimedia.id.in_(ids))
    #     db.session.execute(sql1)
    #     db.session.commit()

        # @staticmethod
        # def get_multimedias_by_televisor_id_with_pagination(id: int, page: int):

        #     multimedias: Pagination = Multimedia.query.filter_by(cliente_id=id).paginate(
        #         page, per_page=MultimediaService.NUMBER_OF_ENTITIES, error_out=False)

        #     print(multimedias)
        #     return multimedias
