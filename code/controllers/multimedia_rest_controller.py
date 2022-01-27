from flask import Blueprint, request, jsonify
from services.multimedia_service import MultimediaService, NotFound
from marshmallow import ValidationError
from schemas.multimedia_schema import MultimediaSchema
from schemas.archivos_schema import ArchivoSchema
from messages.es_ES import messages
import os
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import uuid


# Creando controlador
multimedia_controller = Blueprint('multimedia_controller', __name__)
# inicializando el MultimediaSchema
multimedia_schema = MultimediaSchema()
multimedia_without_cliente = MultimediaSchema(exclude=("cliente",))

archivo_schema = ArchivoSchema()

CARPETA = os.path.abspath("./code/uploads/")


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


@multimedia_controller.route("/", methods=['POST'], strict_slashes=False)
def create():
    try:

        mult_dict = {'nombre': request.form.get('nombre'), 'time_to_start': request.form.get(
            'time_to_start'), 'cliente_id': request.form.get('cliente_id')}
        data = multimedia_schema.load(mult_dict)
        archivo: FileStorage = archivo_schema.load(request.files)['archivo']

        extension = os.path.splitext(archivo.filename)[1]

        nombre_archivo = secure_filename(f"{uuid.uuid4().hex}{extension}")
        archivo.save(os.path.join(CARPETA, nombre_archivo))

        data['archivo'] = nombre_archivo

        MultimediaService.create(data)
        return {"Message": messages['entity_created'].format("Multimedia")}, 201  # Created
    except NotFound as error:
        return {'Error': f"{error}"}, 404  # Not Found
    except (RequestEntityTooLarge, ValidationError) as error:
        return {'Error': f"{error}"}, 400  # Bad Request
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error
