from flask import Blueprint, request, send_from_directory, jsonify
from services.televisor_service import TelevisorService, Televisor, NotFound
from schemas.televisor_schemas import TelevisorSchema
from marshmallow import ValidationError
from messages.es_ES import messages
from typing import Dict
from controllers.cliente_rest_controller import cliente_without_televisores


# Creando controlador
televisor_controller = Blueprint('televisor_controller', __name__)
# inicializando el MultimediaSchema
televisor_schema = TelevisorSchema()
televisor_without_multimedias = TelevisorSchema(exclude=("multimedias",))
televisor_without_multimedias_and_cliente = TelevisorSchema(exclude=("multimedias", "cliente"))


# Metodos
@televisor_controller.route("/<int:id>")
def get_by_id(id: int):
    try:
        televisor: Televisor = TelevisorService.get_by_id(id)
        if televisor:
            return televisor_schema.dump(televisor)  # Aqui estoy usando Marshmallow
        else:
            return {'Error': messages['not_found'].format(id)}, 404  # Not Found
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@televisor_controller.route("/", methods=['POST'], strict_slashes=False)
def create():
    try:

        data: Dict = televisor_without_multimedias.load(request.get_json(), partial=("id",))
        TelevisorService.save(data)

        return {"Message": messages['entity_created'].format("Televisor")}, 201  # Created
    except NotFound as error:
        return {'Error': f"{error}"}, 404  # NotFound
    except ValidationError as error:
        return {'Error': f"{error}"}, 400  # Bad Request
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@televisor_controller.route("/cliente/<int:id>/<int:page>")
def get_televisores_by_cliente_id_with_pagination(id: int, page: int):
    try:
        result = TelevisorService.get_televisores_by_cliente_id_with_pagination(id, page)
        televisores = televisor_without_multimedias_and_cliente.dump(result.items, many=True)
        cliente = cliente_without_televisores.dump(result.items[0].cliente)

        json_temp = {'content': {'cliente': cliente, 'televisores': televisores},  'pageable': {
            'number': result.page - 1, 'totalPages': result.pages, 'totalEntities': result.total}}

        return json_temp
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@televisor_controller.route("/cliente/<int:id>")
def get_televisores_by_cliente_id(id: int):
    try:
        televisores = TelevisorService.get_televisores_by_cliente_id(id)
        if televisores:
            televisores = televisor_without_multimedias_and_cliente.dump(televisores, many=True)
            return jsonify(televisores)
        else:
            return {'Error': messages['empty_bd']}, 400  # Bad Request
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error
