from conexion_bd_mysql import db
from models.televisor import Televisor
from models.cliente import Cliente
from models.historial_de_programacion import HistorialProgramacion
from typing import Dict, List
from flask_sqlalchemy import Pagination
from excepciones_personalizadas.excepciones import NotFound
from sqlalchemy import select
from services.cliente_service import ClienteService
from services.multimedia_service import MultimediaService
from services.televisor_service import TelevisorService

from datetime import datetime


class HistorialDeProgramacionService:
    NUMBER_OF_ENTITIES = 1

    @staticmethod
    def get_historiales_by_cliente_id(id: int):
        # fecha_de_hoy_otro = datetime.today()
        fecha_de_hoy = datetime.today().strftime('%Y-%m-%d')
        fecha_de_hoy_p = datetime.today().strptime(fecha_de_hoy, '%Y-%m-%d')
        # print(f"fecha_de_hoy_otro: {fecha_de_hoy_otro}, tipo: {type(fecha_de_hoy_otro)}")
        # print(f"fecha_de_hoy: {fecha_de_hoy}, tipo: {type(fecha_de_hoy)}")
        # print(f"fecha_de_hoy_p: {fecha_de_hoy_p}, tipo: {type(fecha_de_hoy_p)}")

        stmt = (select(HistorialProgramacion))\
            .where(HistorialProgramacion.cliente_id == id)\
            .where(HistorialProgramacion.fecha == fecha_de_hoy_p)\
            .order_by(HistorialProgramacion.hora_de_inicio)
        results = db.session.execute(stmt).all()

        if results:
            results = [multimedia_tupla[0] for multimedia_tupla in results]

            return results
        else:
            return None

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
