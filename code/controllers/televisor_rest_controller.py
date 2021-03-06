from flask import Blueprint, request, jsonify
from services.televisor_service import TelevisorService, Televisor, NotFound
from services.multimedia_service import MultimediaService
from marshmallow import ValidationError
from messages.es_ES import messages
from typing import Dict
from schemas.general_schemas import televisor_without_multimedias_and_cliente, televisor_without_multimedias_cliente_historiales

from flask_jwt_extended import jwt_required
from configs.jwt_config import admin_required

# Creando controlador
televisor_controller = Blueprint('televisor_controller', __name__)


@televisor_controller.route("/<int:id>")
@jwt_required(fresh=True)
def getById(id: int):
    try:
        televisor: Televisor = TelevisorService.get_by_id(id)
        if televisor:
            # Aqui estoy usando Marshmallow
            return televisor_without_multimedias_cliente_historiales.dump(televisor)
        else:
            # Not Found
            return {'Error': messages['not_found'].format(id)}, 404
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


# Obtengo una lista de televisores con paginacion.
@televisor_controller.route("/cliente/<int:id>/<int:page>")
@admin_required()
@jwt_required(fresh=True)
def getTelevisoresByClienteIdWithPagination(id: int, page: int):
    try:
        result = TelevisorService.get_televisores_by_cliente_id_with_pagination(
            id, page)
        televisores = televisor_without_multimedias_and_cliente.dump(
            result.items, many=True)

        json_temp = {'televisores': televisores,  'pageable': {
            'number': result.page - 1, 'totalPages': result.pages, 'totalEntities': result.total, 'has_next': result.has_next, 'has_prev': result.has_prev}}

        return json_temp
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@televisor_controller.route("/<int:cliente_id>", methods=['POST'], strict_slashes=False)
def create(cliente_id):
    try:

        data: Dict = televisor_without_multimedias_and_cliente.load(
            request.get_json(), partial=("id",))
        TelevisorService.create(data, cliente_id)

        # Created
        return {"Message": messages['entity_created'].format("Televisor")}, 201
    except NotFound as error:
        return {'Error': f"{error}"}, 404  # NotFound
    except ValidationError as error:
        return {'Error': f"{error}"}, 400  # Bad Request
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@televisor_controller.route("/", methods=['PUT'], strict_slashes=False)
def update():
    try:
        # Ya aqui estoy validando con Marshmallow
        data: Dict = televisor_without_multimedias_and_cliente.load(
            request.get_json(), partial=("cliente_id",))
        televisor: Televisor = TelevisorService.get_by_id(data['id'])
        if not televisor:
            return {'Error': messages['not_found'].format(id)}, 404

        televisor.ubicacion = data['ubicacion']
        TelevisorService.update(data)

        # Created
        return {"Message": messages['entity_updated'].format("Cliente")}, 201
    except ValidationError as error:
        return {'Error': f"{error}"}, 400  # Bad Request
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error

# Agrego y quito Multimedias de un Televisor.


@televisor_controller.route("/update/multimedias", methods=['PUT'])
def update_multimedias():
    try:
        if request.get_json().get('televisores') and request.get_json().get('multimedias'):

            televisores = TelevisorService.get_by_ids(
                request.get_json()['televisores'])
            multimedias = MultimediaService.get_by_ids(
                request.get_json()['multimedias'])

            if televisores and multimedias:
                for televisor in televisores:

                    televisor.multimedias = multimedias

                    TelevisorService.update(televisor)

                return {"Message": "Televisor actualizado con exito."}
            else:
                # Not Found
                return {'Error': "No se encontraron los televisores o las multimedias."}, 404
        else:
            return {'Error': "Es obligatorio enviar los ids de los televisores y de las multimedias."}, 400
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@televisor_controller.route("/cliente/<int:id>")
def get_televisores_by_cliente_id(id: int):
    try:
        televisores_temp = TelevisorService.get_televisores_by_cliente_id(id)
        if televisores_temp:
            televisores = televisor_without_multimedias_and_cliente.dump(
                televisores_temp, many=True)
            return jsonify(televisores)

        else:
            return {'Error': messages['empty_bd']}, 400  # Bad Request
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@televisor_controller.route("/historial/<int:id>/<int:page>")
def getTelevisoresByHistorialIdWithPagination(id: int, page: int):
    try:
        result = TelevisorService.getTelevisoresByHistorialIdWithPagination(
            id, page)
        televisores = televisor_without_multimedias_cliente_historiales.dump(
            result.items, many=True)

        json_temp = {'televisores': televisores,  'pageable': {
            'number': result.page - 1, 'totalPages': result.pages, 'totalEntities': result.total, 'has_next': result.has_next, 'has_prev': result.has_prev}}

        return json_temp
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error
