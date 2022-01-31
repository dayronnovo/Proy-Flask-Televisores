from flask import Blueprint, request, send_from_directory, jsonify
from services.multimedia_service import MultimediaService, NotFound, Multimedia
from marshmallow import ValidationError
from schemas.multimedia_schema import MultimediaSchema
from schemas.archivos_schema import ArchivoSchema
from messages.es_ES import messages
import os
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import uuid
from typing import Dict
from math import ceil
from controllers.cliente_rest_controller import cliente_without_multimedias


# Creando controlador
multimedia_controller = Blueprint('multimedia_controller', __name__)
# inicializando el MultimediaSchema
multimedia_schema = MultimediaSchema()
multimedia_without_cliente = MultimediaSchema(exclude=("cliente",))

archivo_schema = ArchivoSchema()

CARPETA = os.path.abspath("./code/uploads/")


# Metodos
@multimedia_controller.route("/<int:id>")
def get_by_id(id: int):
    try:
        multimedia: Multimedia = MultimediaService.get_by_id(id)
        if multimedia:
            return multimedia_schema.dump(multimedia)  # Aqui estoy usando Marshmallow
        else:
            return {'Error': messages['not_found'].format(id)}, 404  # Not Found
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@multimedia_controller.route("/", methods=['POST'], strict_slashes=False)
def create():
    try:
        # Obtengo los parametros por Form-Data y creo un dict para poder validar la entrada.
        # Importante Valido el entity y el archivo por separado
        mult_dict = {'nombre': request.form.get('nombre'), 'time_to_start': request.form.get(
            'time_to_start'), 'cliente_id': request.form.get('cliente_id')}
        data: Dict = multimedia_schema.load(mult_dict)
        archivo: FileStorage = archivo_schema.load(request.files)['archivo']

        extension: str = os.path.splitext(archivo.filename)[1]

        nombre_archivo: str = secure_filename(f"{uuid.uuid4().hex}{extension}")
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


@multimedia_controller.route("/file/<int:id>")
def get_file(id: int):
    try:
        multimedia: Multimedia = MultimediaService.get_by_id(id)
        if multimedia:
            return send_from_directory("uploads", multimedia.archivo, as_attachment=True)
        else:
            return {'Error': messages['not_found'].format(id)}, 404  # Not Found
    except FileNotFoundError as error:
        return {'Error': "La imagen no existe."}, 404  # Not Found
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@multimedia_controller.route("/cliente/<int:id>/<int:page>")
def get_multimedias_by_cliente_id(id: int, page: int):
    try:
        result = MultimediaService.get_multimedias_by_cliente_id(id, page)
        multimedias = multimedia_without_cliente.dump(result.items, many=True)

        cliente = cliente_without_multimedias.dump(result.items[0].cliente)

        json_temp = {'content': {'cliente': cliente, 'multimedias': multimedias},  'pageable': {
            'number': result.page - 1, 'totalPages': ceil(result.total/result.per_page)}}

        return json_temp

    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error

# @multimedia_controller.route("/page/<int:page>")
# def get_all_pagination(page=1):
#     try:
#         result = MultimediaService.get_all_pagination(page)
#         # multimedia = multimedia_schema.dump(result, many=True)
#         multimedia = multimedia_without_cliente.dump(result, many=True)
#         return jsonify(multimedia)

#     except Exception as error:
#         return {'Error': f"{error}"}, 500  # Internal Error
