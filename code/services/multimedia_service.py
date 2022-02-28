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
    def getMultimediasByClienteId(id):
        stmt = (select(Multimedia)).join(
            Multimedia.cliente).where(Cliente.id == id)
        results = db.session.execute(stmt).unique().all()
        # Lo que devuelve
        # [(Multimedia => [id: 68, archivo: 4a011513e36f45ae905afb592be47c0f.png],), (Multimedia => [id: 69, archivo: 6500e83ebe82410c97079050f4fc69c8.png],), (Multimedia => [id: 70, archivo: 2c693cc38a3c48a0ae360629d19b8c7d.png],), (Multimedia => [id: 71, archivo: d867d9166cf44f15961487545c6b559a.png],)]

        results = [multimedia_tupla[0] for multimedia_tupla in results]

        return results


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
