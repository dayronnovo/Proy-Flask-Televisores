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
import json

# from controllers.cliente_rest_controller import cliente_without_multimedias


# Creando controlador
multimedia_controller = Blueprint('multimedia_controller', __name__)
# inicializando el MultimediaSchema
multimedia_schema = MultimediaSchema()
multimedia_without_televisores = MultimediaSchema(exclude=("televisores",))
# inicializando el ArchivoSchema
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
        #  De esta Forma probe como recibir files lo dejo como comentario
        # prueba: FileStorage = request.files['televisor']
        # televisor_json = json.load(request.files['televisor'])
        # print(televisor_json)
        # print(request.files['archivo'])

        # Tengo que crearlo asi porque Marchmallow siempre recibe un JSON si envio solo el
        request_temp = {'archivo': request.files['archivo']}
        # validar el archivo con Marshmallow y luego obtengo el FileStoraged del dict
        archivo = archivo_schema.load(request_temp)['archivo']

        extension: str = os.path.splitext(archivo.filename)[1]

        nombre_archivo: str = secure_filename(f"{uuid.uuid4().hex}{extension}")
        # archivo.save(os.path.join(CARPETA, nombre_archivo))

        MultimediaService.create({'archivo': nombre_archivo}, json.load(request.files['televisor']))
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


# @multimedia_controller.route("/cliente/<int:id>/<int:page>")
# def get_multimedias_by_cliente_id(id: int, page: int):
#     try:
#         result = MultimediaService.get_multimedias_by_cliente_id(id, page)
#         multimedias = multimedia_without_cliente.dump(result.items, many=True)

#         cliente = cliente_without_multimedias.dump(result.items[0].cliente)

#         json_temp = {'content': {'cliente': cliente, 'multimedias': multimedias},  'pageable': {
#             'number': result.page - 1, 'totalPages': ceil(result.total/result.per_page)}}

#         return json_temp

#     except Exception as error:
#         return {'Error': f"{error}"}, 500  # Internal Error

# @multimedia_controller.route("/page/<int:page>")
# def get_all_pagination(page=1):
#     try:
#         result = MultimediaService.get_all_pagination(page)
#         # multimedia = multimedia_schema.dump(result, many=True)
#         multimedia = multimedia_without_cliente.dump(result, many=True)
#         return jsonify(multimedia)

#     except Exception as error:
#         return {'Error': f"{error}"}, 500  # Internal Error
