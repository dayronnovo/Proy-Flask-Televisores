from flask import Blueprint, request, jsonify
from models.multimedia import Multimedia
from services.televisor_service import TelevisorService, Televisor, NotFound
from services.multimedia_service import MultimediaService
from marshmallow import ValidationError
from messages.es_ES import messages
from typing import Dict
from schemas.general_schemas import televisor_schema, televisor_without_multimedias, televisor_without_multimedias_and_cliente, multimedia_without_televisores, cliente_without_televisores

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
@televisor_controller.route("/update/multimedias/<int:id>", methods=['PUT'])
def update(id):
    try:
        # de parametro recibo el id del televisor
        # recibir una lista de multimedias que son las que voy a quitar del televisor

        televisor = TelevisorService.get_by_id(id)

        if televisor:

            multimedias = televisor.multimedias
            if len(request.get_json()['ids']) > 0:

                multimedias_temp = multimedia_without_televisores.dump(request.get_json()['ids'], many=True)

                ids_temp_multimedias = []
                multimedias_temp = [Multimedia.constructor(multimedia) for multimedia in multimedias_temp]

                for multimedia in multimedias:
                    if multimedia not in multimedias_temp:
                        multimedias.remove(multimedia)

                for multimedia in multimedias_temp:
                    if multimedia not in multimedias:
                        ids_temp_multimedias.append(multimedia.id)

                multimedias_para_agregar = MultimediaService.get_by_ids(ids_temp_multimedias)

                multimedias.extend(multimedias_para_agregar)
            else:
                multimedias.clear()

            TelevisorService.save(televisor)

            MultimediaService.borrarMultimedias()

            return {"Message": "Televisor actualizado con exito."}
        else:
            return {'Error': messages['not_found']}, 404  # Not Found
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


# Obtengo todos los televisores de un cliente con su Cliente. Lo uso en el ReutilizarMultimediasComponent.
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
