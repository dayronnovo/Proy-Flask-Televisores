from flask import Blueprint, request
from services.cliente_service import ClienteService, Cliente
from marshmallow import ValidationError
from messages.es_ES import messages
from typing import Dict
from schemas.general_schemas import cliente_schema, cliente_without_televisores, cliente_without_multimedias_and_televisores, archivo_schema
from flask import Blueprint, request
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os
import uuid
from excepciones_personalizadas.excepciones import NotFound

from flask_jwt_extended import jwt_required
from configs.jwt_config import admin_required
# from app import admin_required


# Creando controlador
cliente_controller = Blueprint('cliente_controller', __name__)

CARPETA = os.path.abspath("./code/uploads/")


@cliente_controller.route("/<int:id>")
# @jwt_required(locations=["headers"])
@jwt_required()
def get_by_id(id):
    try:

        # print(f"prueba: {request.args.get('id')}")
        # print(f"prueba: {request.view_args}")
        # id = request.view_args['id']

        cliente: Cliente = ClienteService.get_by_id(id)
        if cliente:

            return cliente_without_multimedias_and_televisores.dump(cliente)
        else:

            return {'Error': messages['not_found'].format(id)}, 404
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@cliente_controller.route("/multimedias", methods=['POST'], strict_slashes=False)
def agregar_multimedias_a_un_cliente():
    try:

        request_temp = {'archivo': request.files['archivo']}
        archivo: FileStorage = archivo_schema.load(request_temp)['archivo']

        extension: str = os.path.splitext(archivo.filename)[1]

        nombre_archivo: str = secure_filename(f"{uuid.uuid4().hex}{extension}")

        archivo.save(os.path.join(CARPETA, nombre_archivo))

        ClienteService.agregar_multimedias_a_un_cliente({'archivo': nombre_archivo, 'tipo_archivo': archivo.content_type},
                                                        request.form.get('cliente_id'))

        # Created
        return {"Message": messages['entity_created'].format("Multimedia")}, 201
    except NotFound as error:
        return {'Error': f"{error}"}, 404  # Not Found
    except (RequestEntityTooLarge, ValidationError) as error:
        return {'Error': f"{error}"}, 400  # Bad Request
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@cliente_controller.route("/", methods=['POST'], strict_slashes=False)
def create():
    try:

        print(request.get_json())
        data: Dict = cliente_without_multimedias_and_televisores.load(
            request.get_json(), partial=("id",))
        ClienteService.save(data)

        return {"Message": messages['entity_created'].format("Cliente")}, 201
    except ValidationError as error:
        return {'Error': f"{error}"}, 400  # Bad Request
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@cliente_controller.route("/", methods=['PUT'], strict_slashes=False)
def update():
    try:

        data: Dict = cliente_schema.load(request.get_json())
        cliente: Cliente = ClienteService.get_by_id(data['id'])
        if not cliente:
            return {'Error': messages['not_found'].format(id)}, 404

        cliente.nombre = data['nombre']
        ClienteService.update(data)

        # Created
        return {"Message": messages['entity_updated'].format("Cliente")}, 201
    except ValidationError as error:
        return {'Error': f"{error}"}, 400  # Bad Request
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@cliente_controller.route("/page/<int:page>")
@admin_required()
def get_all_pagination(page=1):
    try:

        result = ClienteService.get_all_pagination(page)

        cliente = cliente_without_televisores.dump(result.items, many=True)

        json_temp = {'content': cliente,  'pageable': {
            'number': result.page - 1, 'totalPages': result.pages, 'totalEntities': result.total}}

        return json_temp

    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error
