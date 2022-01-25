from flask import Blueprint, request, jsonify
from models.cliente import Cliente
from services.cliente_service import ClienteService
from marshmallow import ValidationError
from schemas.cliente_schemas import ClienteSchema
from messages.es_ES import messages

# Creando controlador
cliente_controller = Blueprint('cliente_controller', __name__)
# inicializando el ClienteSchema
cliente_schema = ClienteSchema()
cliente_without_multimedias = ClienteSchema(exclude=("multimedias",))


# Metodos
@cliente_controller.route("/<int:id>")
def get_by_id(id):
    try:
        autor = ClienteService.get_by_id(id)
        if autor:
            return cliente_schema.dump(autor)  # Aqui estoy usando Marshmallow
        else:
            return {'Error': messages['not_found'].format(id)}, 404  # Not Found
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error
