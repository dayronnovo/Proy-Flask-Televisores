from flask import Blueprint, request
from services.cliente_service import ClienteService, Cliente
from marshmallow import ValidationError
from schemas.cliente_schemas import ClienteSchema
from messages.es_ES import messages
from typing import Dict
from math import ceil

# Creando controlador
cliente_controller = Blueprint('cliente_controller', __name__)
# inicializando el ClienteSchema
cliente_schema = ClienteSchema()
cliente_without_televisores = ClienteSchema(exclude=("televisores",))


# Metodos
@cliente_controller.route("/<int:id>")
def get_by_id(id: int):
    try:
        cliente: Cliente = ClienteService.get_by_id(id)
        if cliente:
            return cliente_schema.dump(cliente)  # Aqui estoy usando Marshmallow
        else:
            return {'Error': messages['not_found'].format(id)}, 404  # Not Found
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@cliente_controller.route("/", methods=['POST'], strict_slashes=False)
def create():
    try:
        # Ya aqui estoy validando con Marshmallow
        data: Dict = cliente_schema.load(request.get_json(), partial=("id",))
        ClienteService.save(data)

        return {"Message": messages['entity_created'].format("Cliente")}, 201  # Created
    except ValidationError as error:
        return {'Error': f"{error}"}, 400  # Bad Request
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@cliente_controller.route("/", methods=['PUT'], strict_slashes=False)
def update():
    try:
        # Ya aqui estoy validando con Marshmallow
        data: Dict = cliente_schema.load(request.get_json())
        cliente: Cliente = ClienteService.get_by_id(data['id'])
        if not cliente:
            return {'Error': messages['not_found'].format(id)}, 404

        cliente.nombre = data['nombre']
        ClienteService.update(data)

        return {"Message": messages['"entity_updated'].format("Cliente")}, 201  # Created
    except ValidationError as error:
        return {'Error': f"{error}"}, 400  # Bad Request
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@cliente_controller.route("/page/<int:page>")
def get_all_pagination(page=1):
    try:

        result = ClienteService.get_all_pagination(page)
        # autores = cliente_schema.dump(result, many=True)
        autores = cliente_without_televisores.dump(result.items, many=True)
        # Formando el JSON
        json_temp = {'content': autores,  'pageable': {
            'number': result.page - 1, 'totalPages': result.pages, 'totalEntities': result.total}}
        #  ceil(result.total/result.per_page)
        return json_temp

    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error
