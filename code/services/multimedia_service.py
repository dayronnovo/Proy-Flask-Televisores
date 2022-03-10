from math import ceil
from flask import session
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
from sqlalchemy.sql import text
from schemas.general_schemas import multimedia_without_televisores_and_cliente_historial

CARPETA = os.path.abspath("./code/uploads/")


class MultimediaService:
    NUMBER_OF_ENTITIES = 2

    @staticmethod
    def getById(id: int):
        multimedia = Multimedia.query.filter_by(id=id).first()
        return multimedia

    @staticmethod
    def getImagenesByClienteId(cliente_id):

        stmt = select(Multimedia).join(Multimedia.cliente).where(
            Cliente.id == cliente_id).where(Multimedia.tipo_archivo.contains('image'))
        results = db.session.execute(stmt).all()
        if len(results) > 0:
            results = [multimedia_tupla[0] for multimedia_tupla in results]

            return results
        else:
            return None

    @staticmethod
    def getVideosByClienteId(cliente_id):

        stmt = select(Multimedia).join(Multimedia.cliente).where(
            Cliente.id == cliente_id).where(Multimedia.tipo_archivo.contains('video'))
        results = db.session.execute(stmt).all()
        if len(results) > 0:
            results = [multimedia_tupla[0] for multimedia_tupla in results]

            return results
        else:
            return None


# ======================================================================
# ======================================================================


    @staticmethod
    def get_by_ids(ids: List):

        stmt = (select(Multimedia)).where(Multimedia.id.in_(ids))
        results = db.session.execute(stmt).all()

        results = [multimedia_tupla[0] for multimedia_tupla in results]
        return results

    @staticmethod
    def create(data: Dict, idsClientes: Dict):
        # print(data)
        # print(idsClientes)

        multimedia = Multimedia.constructor(data)
        televisores = Televisor.query.filter(
            Televisor.id.in_(idsClientes['ids'])).all()

        multimedia.televisores = televisores

        db.session.add(multimedia)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()

    # @staticmethod
    # def borrarMultimedias():
    #     # Ver mas tarde como hacerlo mejor
    #     multimedias_empty_tuplas = db.engine.execute(
    #         "SELECT m.id, m.archivo FROM  multimedias m WHERE m.id NOT IN (SELECT tlm.multimedia_id FROM televisor_multimedia tlm)").all()
    #     ids_list = []

    #     for multimedia in multimedias_empty_tuplas:
    #         os.remove(os.path.join(CARPETA, multimedia[1]))
    #         ids_list.append(multimedia[0])

    #     sql1 = delete(Multimedia).where(Multimedia.id.in_(ids_list))
    #     db.session.execute(sql1)
    #     db.session.commit()


# Obtengo todas las multimedias del cliente. Lo uso en el ReutilizarMultimediasComponent para poder marcar en el checked

    @staticmethod
    def getMultimediasByClienteIdWithPagination(id: int, page: int):

        # print(f"Page: {page}")
        # print(f"Id: {id}")

        pagina = 0 if page == 0 or page == 1 else page - 2

        consulta_multimedias = text(
            "SELECT mult.id, mult.archivo, mult.tipo_archivo FROM multimedias mult JOIN clientes clit ON clit.id = mult.cliente_id WHERE  clit.id = :id AND mult.id NOT IN  (SELECT tel_mult.multimedia_id FROM televisor_multimedia tel_mult) LIMIT :page, :por_pagina")

        consulta_total_entities = text(
            "SELECT count(mult.id) FROM multimedias mult JOIN clientes   clit ON clit.id = mult.cliente_id WHERE  clit.id = :id AND mult.id not IN (SELECT tel_mult.multimedia_id FROM televisor_multimedia tel_mult)")

        multimedias_empty_tuplas = db.engine.execute(
            consulta_multimedias, {'id': id, 'page': (pagina) * MultimediaService.NUMBER_OF_ENTITIES, 'por_pagina': MultimediaService.NUMBER_OF_ENTITIES}).all()
        total_entities = db.engine.execute(
            consulta_total_entities, {'id': id}).one()[0]

        multimedias_objetos = [Multimedia.constructor({'id': multimedia_tupla[0], 'archivo':multimedia_tupla[1], 'tipo_archivo': multimedia_tupla[2]})
                               for multimedia_tupla in multimedias_empty_tuplas]

        totalPages = ceil(total_entities/MultimediaService.NUMBER_OF_ENTITIES)
        hasNext = totalPages != pagina + 1
        hasPrev = pagina + 1 > 1

        multimedias_json = multimedia_without_televisores_and_cliente_historial.dump(
            multimedias_objetos, many=True)

        return {'multimedias': multimedias_json,  'pageable': {
            'number': pagina + 1, 'totalPages': totalPages, 'totalEntities': total_entities, 'has_next': hasNext, 'has_prev': hasPrev}}

        # ============================================

        # multimedias: Pagination = Multimedia.query\
        #     .join(Multimedia.cliente)\
        #     .join(Multimedia.televisores)\
        #     .from_self(Multimedia)\
        #     .where(Multimedia.id.in_)\
        #     .paginate(
        #     page, per_page=MultimediaService.NUMBER_OF_ENTITIES, error_out=False)
        # return None
        # return multimedias
    # @staticmethod
    # def getMultimediasByClienteId(id):
    #     stmt = (select(Multimedia)).join(
    #         Multimedia.cliente).where(Cliente.id == id)
    #     results = db.session.execute(stmt).unique().all()
    #     # Lo que devuelve
    #     # [(Multimedia => [id: 68, archivo: 4a011513e36f45ae905afb592be47c0f.png],), (Multimedia => [id: 69, archivo: 6500e83ebe82410c97079050f4fc69c8.png],), (Multimedia => [id: 70, archivo: 2c693cc38a3c48a0ae360629d19b8c7d.png],), (Multimedia => [id: 71, archivo: d867d9166cf44f15961487545c6b559a.png],)]

    #     results = [multimedia_tupla[0] for multimedia_tupla in results]

    #     return results


# Obtengo todas las multimedias del televisor. Lo uso en el ReutilizarMultimediasComponent para poder marcar en el checked


    @staticmethod
    def getMultimediasByTelevisorId(id):
        stmt = (select(Multimedia)).join(Televisor.multimedias).join(Televisor.cliente).where(
            Televisor.id == id)
        results = db.session.execute(stmt).all()

        if results:
            results = [multimedia_tupla[0] for multimedia_tupla in results]
            return results
        else:
            return None


# Obtengo todas las imagenes del televisor. Lo uso en el ImagenesComponent para poder marcar en el checked. Es necesareo separarlos para obligar a que se deban escoger imagenes o videos. Nunca los dos juntos.

    @staticmethod
    def getImagenesByTelevisorId(id):
        stmt = (select(Multimedia, Televisor, Cliente)).join(Televisor.multimedias).join(Televisor.cliente).where(
            Televisor.id == id).where(Multimedia.tipo_archivo.contains('image'))
        results = db.session.execute(stmt).all()
        if len(results) > 0:
            multimedias = [multimedia_tupla[0] for multimedia_tupla in results]
            televisor = results[0][1]
            cliente = results[0][2]
            mapa = {'cliente': cliente, 'televisor': televisor,
                    'multimedias': multimedias}
            return mapa
        else:
            return None

    @staticmethod
    def delete(multimedias):

        ids_list = []
        for multimedia in multimedias:
            os.remove(os.path.join(CARPETA, multimedia.archivo))
            ids_list.append(multimedia.id)

        sql1 = delete(Multimedia).where(Multimedia.id.in_(ids_list))
        db.session.execute(sql1)
        db.session.commit()


# Obtengo todos los videos del televisor. Lo uso en el ImagenesComponent para poder marcar en el checked. Es necesareo separarlos para obligar a que se deban escoger imagenes o videos. Nunca los dos juntos.

    @staticmethod
    def getVideosByTelevisorId(id):
        stmt = (select(Multimedia, Televisor, Cliente)).join(Televisor.multimedias).join(Televisor.cliente).where(
            Televisor.id == id).where(Multimedia.tipo_archivo.contains('video'))
        results = db.session.execute(stmt).all()
        if len(results) > 0:
            multimedias = [multimedia_tupla[0] for multimedia_tupla in results]
            televisor = results[0][1]
            cliente = results[0][2]
            mapa = {'cliente': cliente, 'televisor': televisor,
                    'multimedias': multimedias}
            return mapa
        else:
            return None

# =========================================================
#                 Eliminar varios entities
# =========================================================

    # @staticmethod
    # def get_by_ids(ids: List, televisor_id: int):

    #     stmt = (select(Multimedia)).join(Televisor.multimedias).where(
    #         Televisor.id == televisor_id).where(Multimedia.id.in_(ids))
    #     results = db.session.execute(stmt).unique().all()

    #     if len(results) > 0:
    #         results = [multimedia_tupla[0] for multimedia_tupla in results]

    #         return results
    #     else:
    #         return None

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


# =========================================================
#             Los dejo como muestra del join
# =========================================================

    # @staticmethod
    # def getImagenesByTelevisorId(id):
    #     stmt = (select(Multimedia, Televisor)).join(Televisor.multimedias).join(Televisor.cliente).where(
    #         Televisor.id == id).where(Multimedia.tipo_archivo.contains('image'))
    #     results = db.session.execute(stmt).all()
    #     if len(results) > 0:
    #         multimedias = [multimedia_tupla[0] for multimedia_tupla in results]
    #         televisor = results[0][1]
    #         cliente = results[0][2]
    #         mapa = {'cliente': cliente, 'televisor': televisor, 'multimedias': multimedias}
    #         return mapa
    #     else:
    #         return None

    # @staticmethod
    # def getVideosByTelevisorId(id):
    #     stmt = (select(Multimedia, Televisor)).join(Televisor.multimedias).join(Televisor.cliente).where(
    #         Televisor.id == id).where(Multimedia.tipo_archivo.contains('video'))
    #     results = db.session.execute(stmt).all()
    #     if len(results) > 0:
    #         multimedias = [multimedia_tupla[0] for multimedia_tupla in results]
    #         televisor = results[0][1]
    #         cliente = results[0][2]
    #         mapa = {'cliente': cliente, 'televisor': televisor, 'multimedias': multimedias}
    #         return mapa
    #     else:
    #         return None


#     @staticmethod
#     def getMultimediasByTelevisorId(id):
#         stmt = (select(Multimedia, Televisor, Cliente)).join(Televisor.multimedias).join(Televisor.cliente).where(
#             Televisor.id == id)
#         results = db.session.execute(stmt).all()
#         if len(results) > 0:
#             multimedias = [multimedia_tupla[0] for multimedia_tupla in results]
#             televisor = results[0][1]
#             cliente = results[0][2]
#             mapa = {'cliente': cliente, 'televisor': televisor, 'multimedias': multimedias}
#             return mapa
#         else:
#             return None
