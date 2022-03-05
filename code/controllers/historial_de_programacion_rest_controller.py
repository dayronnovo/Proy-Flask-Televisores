from flask import Blueprint, request, jsonify
from models.multimedia import Multimedia
from services.televisor_service import TelevisorService, Televisor, NotFound
from services.multimedia_service import MultimediaService
from services.historial_de_programacion_service import HistorialDeProgramacionService
from marshmallow import ValidationError
from messages.es_ES import messages
from typing import Dict
from schemas.general_schemas import historial_programacion_without_cliente_multimedia_televisor, historial_programacion_without_cliente, historial_programacion

# Creando controlador
historial_de_programacion_controller = Blueprint(
    'historial_de_programacion_controller', __name__)


@historial_de_programacion_controller.route("/<int:id>/<int:page>", methods=['PUT'], strict_slashes=False)
def get_historiales_by_cliente_id(id: int, page: int):
    # print("Controlador: ")
    # print(request.get_json())
    # print(id)
    # print(page)

    try:
        result = HistorialDeProgramacionService.get_historiales_by_cliente_id(
            id, page, request.get_json()['fecha'])

        historial_programacion_dict = historial_programacion_without_cliente.dump(
            result.items, many=True)

        json_temp = {'historiales': historial_programacion_dict,  'pageable': {
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
