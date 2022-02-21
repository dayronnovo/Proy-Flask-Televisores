from flask import Blueprint, request, jsonify
from models.multimedia import Multimedia
from services.televisor_service import TelevisorService, Televisor, NotFound
from services.multimedia_service import MultimediaService
from marshmallow import ValidationError
from messages.es_ES import messages
from typing import Dict
from schemas.general_schemas import televisor_schema, televisor_without_multimedias, televisor_without_multimedias_and_cliente, multimedia_without_televisores_and_cliente, cliente_without_televisores

# Creando controlador
televisor_controller = Blueprint('televisor_controller', __name__)


# Devuelve un objeto Televisor con su Cliente.
@televisor_controller.route("/<int:id>")
def get_by_id(id: int):
    try:
        televisor: Televisor = TelevisorService.get_by_id(id)
        if televisor:
            return televisor_without_multimedias.dump(televisor)  # Aqui estoy usando Marshmallow
        else:
            return {'Error': messages['not_found'].format(id)}, 404  # Not Found
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


# Obtengo una lista de televisores con paginacion.
@televisor_controller.route("/cliente/<int:id>/<int:page>")
def get_televisores_by_cliente_id_with_pagination(id: int, page: int):
    try:
        result = TelevisorService.get_televisores_by_cliente_id_with_pagination(id, page)
        televisores = televisor_without_multimedias_and_cliente.dump(result.items, many=True)
        cliente = None
        if len(result.items) > 0:
            cliente = cliente_without_televisores.dump(result.items[0].cliente)

        json_temp = {'content': {'cliente': cliente, 'televisores': televisores},  'pageable': {
            'number': result.page - 1, 'totalPages': result.pages, 'totalEntities': result.total}}

        return json_temp
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


# Este todavia no lo estoy usando.
@televisor_controller.route("/", methods=['POST'], strict_slashes=False)
def create():
    try:

        data: Dict = televisor_without_multimedias.load(request.get_json(), partial=("id",))
        TelevisorService.create(data)

        return {"Message": messages['entity_created'].format("Televisor")}, 201  # Created
    except NotFound as error:
        return {'Error': f"{error}"}, 404  # NotFound
    except ValidationError as error:
        return {'Error': f"{error}"}, 400  # Bad Request
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


# Agrego y quito Multimedias de un Televisor.
@televisor_controller.route("/update/multimedias", methods=['PUT'])
def update():
    try:

        # print(request.get_json())
        # print(request.get_json()['televisores'])
        # print(request.get_json()['multimedias'])
        if request.get_json().get('televisores') and request.get_json().get('multimedias'):

            televisores = TelevisorService.get_by_ids(request.get_json()['televisores'])
            multimedias = MultimediaService.get_by_ids(request.get_json()['multimedias'])

            if televisores and multimedias:
                for televisor in televisores:

                    televisor.multimedias = multimedias

                    TelevisorService.save(televisor)

                return {"Message": "Televisor actualizado con exito."}
            else:
                return {'Error': "No se encontraron los televisores o las multimedias."}, 404  # Not Found
        else:
            return {'Error': "Es obligatorio enviar los ids de los televisores y de las multimedias."}, 400
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


# Obtengo todos los televisores de un cliente con su Cliente. Lo uso en el ReutilizarMultimediasComponent.
@televisor_controller.route("/cliente/<int:id>")
def get_televisores_by_cliente_id(id: int):
    try:
        televisores_temp = TelevisorService.get_televisores_by_cliente_id(id)
        if televisores_temp:
            televisores = televisor_without_multimedias_and_cliente.dump(televisores_temp, many=True)
            return jsonify(televisores)

        else:
            return {'Error': messages['empty_bd']}, 400  # Bad Request
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error
