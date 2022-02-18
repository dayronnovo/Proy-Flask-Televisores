from flask import Blueprint, request, send_from_directory, jsonify
from services.multimedia_service import MultimediaService, NotFound, Multimedia
from services.televisor_service import TelevisorService
from marshmallow import ValidationError
from messages.es_ES import messages
import os
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import uuid
import json
from schemas.general_schemas import multimedia_schema, multimedia_without_televisores, archivo_schema, cliente_without_televisores, televisor_without_multimedias_and_cliente


# Creando controlador
multimedia_controller = Blueprint('multimedia_controller', __name__)


CARPETA = os.path.abspath("./code/uploads/")


# Creo las multimedias
@multimedia_controller.route("/", methods=['POST'], strict_slashes=False)
def create():
    try:
        #  De esta Forma probe como recibir files lo dejo como comentario
        # prueba: FileStorage = request.files['televisor']
        # televisor_json = json.load(request.files['televisor'])
        # print(televisor_json)
        # print(request.files['archivo'])

        # Tengo que crearlo asi porque Marchmallow siempre recibe un JSON
        request_temp = {'archivo': request.files['archivo']}
        # validar el archivo con Marshmallow y luego obtengo el FileStoraged del dict
        archivo: FileStorage = archivo_schema.load(request_temp)['archivo']

        # print(f"Imagen: {archivo.content_type.startswith('image')}")
        # print(f"Video: {archivo.content_type.startswith('video')}")

        extension: str = os.path.splitext(archivo.filename)[1]

        nombre_archivo: str = secure_filename(f"{uuid.uuid4().hex}{extension}")
        # Debo guardar la imagen o el video despues de haber guardado en la BBDD.
        archivo.save(os.path.join(CARPETA, nombre_archivo))

        MultimediaService.create({'archivo': nombre_archivo, 'tipo_archivo': archivo.content_type},
                                 json.load(request.files['televisor']))
        return {"Message": messages['entity_created'].format("Multimedia")}, 201  # Created
    except NotFound as error:
        return {'Error': f"{error}"}, 404  # Not Found
    except (RequestEntityTooLarge, ValidationError) as error:
        return {'Error': f"{error}"}, 400  # Bad Request
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@multimedia_controller.route("/reproducir/<int:id>", methods=['PUT'], strict_slashes=False)
def get_multimedias_by_ids(id):

    # print(request.get_json()['ids'])

    try:

        multimedias = MultimediaService.get_by_ids(request.get_json()['ids'], id)
        if multimedias:
            multimedias = multimedia_without_televisores.dump(multimedias, many=True)
            return jsonify(multimedias)
        else:
            return {'Error': "No se encontraron multimedias"}, 404  # Not Found
    except NotFound as error:
        return {'Error': f"{error}"}, 404  # NotFound
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


# Obtengo las multimedias (los archivos)
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


# Obtengo las imagenes por el id del televisor.
@multimedia_controller.route("/televisor/imagenes/<int:id>")
def get_imagenes_by_televisor_id(id: int):
    try:
        result_dict = MultimediaService.getImagenesByTelevisorId(id)
        if result_dict:
            cliente = cliente_without_televisores.dump(result_dict['cliente'])
            televisor = televisor_without_multimedias_and_cliente.dump(result_dict['televisor'])
            multimedias = multimedia_without_televisores.dump(result_dict['multimedias'], many=True)

            return {'cliente': cliente, 'televisor': televisor, 'multimedias': multimedias}
        else:
            return {'Error': f"El televisor con el id: {id} no tiene multimedias"}, 404  # Not Found
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@multimedia_controller.route("/televisor/videos/<int:id>")
def get_videos_by_televisor_id(id: int):
    try:
        result_dict = MultimediaService.getVideosByTelevisorId(id)
        if result_dict:
            cliente = cliente_without_televisores.dump(result_dict['cliente'])
            televisor = televisor_without_multimedias_and_cliente.dump(result_dict['televisor'])
            multimedias = multimedia_without_televisores.dump(result_dict['multimedias'], many=True)

            return {'cliente': cliente, 'televisor': televisor, 'multimedias': multimedias}
        else:
            return {'Error': f"El televisor con el id: {id} no tiene multimedias"}, 404  # Not Found
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@multimedia_controller.route("/televisor/<int:id>")
def get_multimedias_by_televisor_id(id: int):
    try:
        result_dict = MultimediaService.getMultimediasByTelevisorId(id)
        if result_dict:
            cliente = cliente_without_televisores.dump(result_dict['cliente'])
            televisor = televisor_without_multimedias_and_cliente.dump(result_dict['televisor'])
            multimedias_del_televisor = multimedia_without_televisores.dump(result_dict['multimedias'], many=True)

            multimedias_del_cliente = multimedia_without_televisores.dump(
                MultimediaService.getMultimediasByClienteId(cliente['id']), many=True)

            return {'cliente': cliente, 'televisor': televisor, 'multimedias_televisor': multimedias_del_televisor, 'multimedias_cliente': multimedias_del_cliente}
        else:
            return {'Error': f"El televisor con el id: {id} no tiene multimedias"}, 404  # Not Found
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error

# @multimedia_controller.route("/multimedias/<int:id>")
# def get_multimedias_by_televisor_id(id: int):
    # try:
    #     televisor = TelevisorService.get_by_id(id)

    #     if televisor:
    #         multimedias_televisor_dict = multimedia_without_televisores.dump(televisor.multimedias, many=True)

    #         televisor_dict = televisor_without_multimedias_and_cliente.dump(televisor)

    #         cliente_dict = cliente_without_televisores.dump(televisor.cliente)
    #         # Obtengo las multimedias del televisor.
    #         multimedias_del_cliente = TelevisorService.getMultimediasByClienteId(cliente_dict['id'])

    #         multimedias_del_cliente = multimedia_without_televisores.dump(
    #             multimedias_del_cliente, many=True)

    #         resp_personalizada = {'cliente': cliente_dict, 'multimedias_televisor': multimedias_televisor_dict,
    #                               'multimedias_cliente': multimedias_del_cliente, 'televisor': televisor_dict}

    #         # return jsonify(multimedias_dict)
    #         return resp_personalizada
    #     else:
    #         return {'Error': messages['empty_bd']}, 400  # Bad Request
    # except Exception as error:
    #     return {'Error': f"{error}"}, 500  # Internal Error

# Con este metodo estaba obteniendo las Multimedias del Cliente por el Id de este.
# @multimedia_controller.route("/cliente/<int:id>")
# def get_multimedias_by_cliente_id(id: int):
#     try:
#         multimedias = MultimediaService.getMultimediasByClienteId(id)

#         if multimedias:
#             multimedias_dict = multimedia_without_televisores.dump(
#                 multimedias, many=True)  # Aqui estoy usando Marshmallow
#             return jsonify(multimedias_dict)
#         else:
#             return {'Error': messages['not_found'].format(id)}, 404  # Not Found
#     except Exception as error:
#         return {'Error': f"{error}"}, 500  # Internal Error

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
