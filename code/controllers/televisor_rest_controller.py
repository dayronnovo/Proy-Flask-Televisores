from flask import Blueprint, request, jsonify
from services.televisor_service import TelevisorService, Televisor, NotFound
from services.multimedia_service import MultimediaService
from schemas.televisor_schemas import TelevisorSchema
from marshmallow import ValidationError
from messages.es_ES import messages
from typing import Dict
from controllers.cliente_rest_controller import cliente_without_televisores
import json
from controllers.multimedia_rest_controller import multimedia_without_televisores

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
        TelevisorService.create(data)

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
        cliente = None
        if len(result.items) > 0:
            cliente = cliente_without_televisores.dump(result.items[0].cliente)

        json_temp = {'content': {'cliente': cliente, 'televisores': televisores},  'pageable': {
            'number': result.page - 1, 'totalPages': result.pages, 'totalEntities': result.total}}

        return json_temp
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@televisor_controller.route("/cliente/<int:id>")
def get_televisores_by_cliente_id(id: int):
    try:
        televisores_temp = TelevisorService.get_televisores_by_cliente_id(id)
        if televisores_temp:
            televisores = televisor_without_multimedias_and_cliente.dump(televisores_temp, many=True)
            cliente_dict = cliente_without_televisores.dump(televisores_temp[0].cliente)
            resp_personalizada = {'cliente': cliente_dict, 'televisores': televisores}
            # print(resp_personalizada)
            # return jsonify(televisores)
            return resp_personalizada
        else:
            return {'Error': messages['empty_bd']}, 400  # Bad Request
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@televisor_controller.route("/remove_multimedias/<int:id>", methods=['PUT'])
def remove(id):
    try:
        # de parametro recibo el id del televisor
        # recibir una lista de multimedias que son las que voy a quitar del televisor

        televisor = TelevisorService.get_by_id(id)

        if televisor:

            if not request.get_json():
                televisor.multimedias.clear()
            else:
                multimedias = televisor.multimedias
                ids_multimedias = request.get_json()['ids']
                for id_multimedia in ids_multimedias:
                    for multimedia in multimedias:
                        if multimedia.id == id_multimedia:
                            multimedias.remove(multimedia)

            TelevisorService.save(televisor)

            MultimediaService.borrarMultimedias()

            return {"Message": messages['entity_deleted'].format("Televisor")}
        else:
            return {'Error': messages['not_found']}, 404  # Not Found
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@televisor_controller.route("/multimedias/<int:id>")
def get_multimedias_by_televisor_id(id: int):
    try:
        televisor = TelevisorService.get_by_id(id)

        if televisor:
            multimedias_dict = multimedia_without_televisores.dump(televisor.multimedias, many=True)

            cliente_dict = cliente_without_televisores.dump(televisor.cliente)
            resp_personalizada = {'cliente': cliente_dict, 'multimedias': multimedias_dict}

            # return jsonify(multimedias_dict)
            return resp_personalizada
        else:
            return {'Error': messages['empty_bd']}, 400  # Bad Request
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error
