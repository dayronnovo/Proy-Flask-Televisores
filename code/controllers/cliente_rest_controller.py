from flask import Blueprint, request
from services.cliente_service import ClienteService, Cliente
from marshmallow import ValidationError
from messages.es_ES import messages
from typing import Dict
from schemas.general_schemas import cliente_schema, cliente_without_televisores, cliente_without_multimedias_and_televisores, archivo_schema

from flask import Blueprint, request, send_from_directory, jsonify
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os
import uuid
import json
from excepciones_personalizadas.excepciones import NotFound

# Creando controlador
cliente_controller = Blueprint('cliente_controller', __name__)

CARPETA = os.path.abspath("./code/uploads/")

# Metodos


@cliente_controller.route("/<int:id>")
def get_by_id(id: int):
    try:
        cliente: Cliente = ClienteService.get_by_id(id)
        if cliente:
            return cliente_without_multimedias_and_televisores.dump(cliente)  # Aqui estoy usando Marshmallow
        else:
            return {'Error': messages['not_found'].format(id)}, 404  # Not Found
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


# Asignar Multimedias a un Cliente
@cliente_controller.route("/multimedias", methods=['POST'], strict_slashes=False)
def agregar_multimedias_a_un_cliente():
    try:
        #  De esta Forma probe como recibir files lo dejo como comentario
        #         # prueba: FileStorage = request.files['televisor']
        #         # televisor_json = json.load(request.files['televisor'])
        #         # print(televisor_json)
        #         # print(request.files['archivo'])
        # print(f"Desde el ClienteController: {request.files}")
        # print(f"Desde el ClienteController: {request.form.get('cliente_id')}")
        request_temp = {'archivo': request.files['archivo']}
        # validar el archivo con Marshmallow y luego obtengo el FileStoraged del dict
        archivo: FileStorage = archivo_schema.load(request_temp)['archivo']

        # # print(f"Imagen: {archivo.content_type.startswith('image')}")
        # # print(f"Video: {archivo.content_type.startswith('video')}")

        extension: str = os.path.splitext(archivo.filename)[1]

        nombre_archivo: str = secure_filename(f"{uuid.uuid4().hex}{extension}")
        # # Debo guardar la imagen o el video despues de haber guardado en la BBDD.
        archivo.save(os.path.join(CARPETA, nombre_archivo))

        ClienteService.agregar_multimedias_a_un_cliente({'archivo': nombre_archivo, 'tipo_archivo': archivo.content_type},
                                                        request.form.get('cliente_id'))

        return {"Message": messages['entity_created'].format("Multimedia")}, 201  # Created
    except NotFound as error:
        return {'Error': f"{error}"}, 404  # Not Found
    except (RequestEntityTooLarge, ValidationError) as error:
        return {'Error': f"{error}"}, 400  # Bad Request
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
        cliente = cliente_without_televisores.dump(result.items, many=True)
        # Formando el JSON
        json_temp = {'content': cliente,  'pageable': {
            'number': result.page - 1, 'totalPages': result.pages, 'totalEntities': result.total}}
        #  ceil(result.total/result.per_page)
        return json_temp

    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error
