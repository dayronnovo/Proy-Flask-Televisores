from conexion_bd_mysql import db
from models.televisor import Televisor
from models.cliente import Cliente
from models.historial_de_programacion import HistorialProgramacion
from typing import Dict, List
from flask_sqlalchemy import Pagination
from excepciones_personalizadas.excepciones import NotFound
from sqlalchemy import select, desc
from services.cliente_service import ClienteService
from services.multimedia_service import MultimediaService
from services.televisor_service import TelevisorService

from datetime import datetime


class HistorialDeProgramacionService:
    NUMBER_OF_ENTITIES = 2

    @staticmethod
    def get_historiales_by_cliente_id(id: int, page, fecha):
        print("Ejecutando metodo")
        # fecha_de_hoy_otro = datetime.today()
        # fecha_de_hoy = datetime.today().strftime('%Y-%m-%d')
        # fecha_de_hoy_p = datetime.today().strptime(fecha_de_hoy, '%Y-%m-%d')

        historial_paginacion: Pagination = HistorialProgramacion.query\
            .where(HistorialProgramacion.cliente_id == id)\
            .where(HistorialProgramacion.fecha == fecha)\
            .order_by(desc(HistorialProgramacion.hora_de_inicio))\
            .paginate(
                page=page, per_page=HistorialDeProgramacionService.NUMBER_OF_ENTITIES, error_out=False)

        print(historial_paginacion.items)

        return historial_paginacion

    @staticmethod
    def create(data: Dict, multimedias, televisores, cliente_id):

        historial = HistorialProgramacion.constructor(data)

        cliente = ClienteService.get_by_id(cliente_id)
        multimedias = MultimediaService.get_by_ids(multimedias)
        televisores = TelevisorService.get_by_ids(televisores)

        historial.cliente = cliente
        historial.multimedias = multimedias
        historial.televisores = televisores

        db.session.add(historial)
        db.session.commit()
