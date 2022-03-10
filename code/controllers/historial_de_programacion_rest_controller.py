from flask import Blueprint, request, jsonify
from models.historial_de_programacion import HistorialProgramacion
from models.multimedia import Multimedia
from services.televisor_service import TelevisorService, Televisor, NotFound
from services.multimedia_service import MultimediaService
from services.historial_de_programacion_service import HistorialDeProgramacionService
from marshmallow import ValidationError
from messages.es_ES import messages
from typing import Dict
from flask_sqlalchemy import Pagination
from schemas.general_schemas import historial_programacion_without_cliente_multimedia_televisor, historial_programacion_without_cliente, historial_programacion, historial_programacion_without_cliente_televisor, televisor_without_multimedias_cliente_historiales

# Creando controlador
historial_de_programacion_controller = Blueprint(
    'historial_de_programacion_controller', __name__)


@historial_de_programacion_controller.route("/<int:id>/<int:page>", methods=['PUT'], strict_slashes=False)
def get_historiales_by_cliente_id(id: int, page: int):

    try:
        result = HistorialDeProgramacionService.get_historiales_by_cliente_id(
            id, page, request.get_json()['fecha'])

        lista_de_historiales_map = []

        for historial in result.items:

            historial_map = historial_programacion_without_cliente_televisor.dump(
                historial)

            result_televisores: Pagination = TelevisorService.getTelevisoresByHistorialIdWithPagination(
                historial.id, 1)

            result_televisores_map = televisor_without_multimedias_cliente_historiales.dump(
                result_televisores.items, many=True)

            historial_map['televisores_pagination'] = {'televisores': result_televisores_map, 'pageable': {
                'number': result_televisores.page - 1, 'totalPages': result_televisores.pages, 'totalEntities': result_televisores.total, 'has_next': result_televisores.has_next, 'has_prev': result_televisores.has_prev}}

            lista_de_historiales_map.append(historial_map)

        json_temp = {'historiales': lista_de_historiales_map,  'pageable': {
            'number': result.page - 1, 'totalPages': result.pages, 'totalEntities': result.total}}

        return json_temp

    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@historial_de_programacion_controller.route("/", methods=['POST'], strict_slashes=False)
def create():
    try:
        if(request.get_json()['hora_de_inicio'] == 'null'):
            request.get_json()['hora_de_inicio'] = '00:00:00'

        historial_programacion_dict = {'hora_de_inicio': request.get_json(
        )['hora_de_inicio'], 'time_id': request.get_json()['time_id']}

        data: Dict = historial_programacion_without_cliente_multimedia_televisor.load(
            historial_programacion_dict, partial=("id"))

        HistorialDeProgramacionService.create(
            data, request.get_json()['multimedias'], request.get_json()['televisores'], request.get_json()['cliente'])

        # Created
        return {"Message": messages['entity_created'].format("Televisor")}, 201
    except NotFound as error:
        return {'Error': f"{error}"}, 404  # NotFound
    except ValidationError as error:
        return {'Error': f"{error}"}, 400  # Bad Request
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@historial_de_programacion_controller.route("/<int:id>", methods=['DELETE'])
def delete(id: int):
    try:

        historial: HistorialProgramacion = HistorialDeProgramacionService.getById(
            id)
        if historial:
            historial.multimedias.clear()
            historial.televisores.clear()

            HistorialDeProgramacionService.update()
            HistorialDeProgramacionService.delete(historial.id)
            return {"Message": "Historial eliminado con exito."}, 200
        else:
            # Not Found
            return {'Error': messages['not_found'].format(id)}, 404
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error
