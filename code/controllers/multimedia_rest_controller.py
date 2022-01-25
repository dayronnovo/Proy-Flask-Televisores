from flask import Blueprint, request, jsonify
from services.multimedia_service import MultimediaService
from marshmallow import ValidationError
from schemas.multimedia_schema import MultimediaSchema
from messages.es_ES import messages

# Creando controlador
multimedia_controller = Blueprint('multimedia_controller', __name__)
# inicializando el MultimediaSchema
multimedia_schema = MultimediaSchema()
multimedia_without_cliente = MultimediaSchema(exclude=("cliente",))


# Metodos
@multimedia_controller.route("/<int:id>")
def get_by_id(id):
    try:
        autor = MultimediaService.get_by_id(id)
        if autor:
            return multimedia_schema.dump(autor)  # Aqui estoy usando Marshmallow
        else:
            return {'Error': messages['not_found'].format(id)}, 404  # Not Found
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error
