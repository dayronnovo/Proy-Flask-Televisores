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
historial_de_programacion_controller = Blueprint('historial_de_programacion_controller', __name__)


# Devuelve un objeto Televisor con su Cliente.
@historial_de_programacion_controller.route("/<int:id>")
def get_historiales_by_cliente_id(id: int):
    try:
        historiales_programacion = HistorialDeProgramacionService.get_historiales_by_cliente_id(id)
        if historiales_programacion:
            historiales_programacion = historial_programacion_without_cliente.dump(
                historiales_programacion, many=True)
            return jsonify(historiales_programacion)
        else:
            return {'Error': messages['not_found'].format(id)}, 404  # Not Found
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@historial_de_programacion_controller.route("/", methods=['POST'], strict_slashes=False)
def create():
    try:
        print(request.get_json())
        historial_programacion_dict = {'hora_de_inicio': request.get_json(
        )['hora_de_inicio'], 'time_id': request.get_json()['time_id']}

        data: Dict = historial_programacion_without_cliente_multimedia_televisor.load(
            historial_programacion_dict, partial=("id"))

        HistorialDeProgramacionService.create(
            data, request.get_json()['multimedias'], request.get_json()['televisores'], request.get_json()['cliente'])

        return {"Message": messages['entity_created'].format("Televisor")}, 201  # Created
    except NotFound as error:
        return {'Error': f"{error}"}, 404  # NotFound
    except ValidationError as error:
        return {'Error': f"{error}"}, 400  # Bad Request
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error
