from flask import Blueprint, request, send_from_directory, jsonify
from services.multimedia_service import MultimediaService, Multimedia
from messages.es_ES import messages
import os
from schemas.general_schemas import multimedia_without_televisores_and_cliente, multimedia_without_televisores, cliente_without_televisores, televisor_without_multimedias_and_cliente


# Creando controlador
multimedia_controller = Blueprint('multimedia_controller', __name__)


CARPETA = os.path.abspath("./code/uploads/")


@multimedia_controller.route("/reproducir/<int:id>", methods=['PUT'], strict_slashes=False)
def get_multimedias_by_ids(id):

    try:

        multimedias = MultimediaService.get_by_ids(
            request.get_json()['ids'], id)
        if multimedias:
            multimedias = multimedia_without_televisores.dump(
                multimedias, many=True)
            return jsonify(multimedias)
        else:
            return {'Error': "No se encontraron multimedias"}, 404  # Not Found

    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


# Obtengo las multimedias (los archivos)
@multimedia_controller.route("/file/<int:id>")
def get_file(id: int):
    try:
        multimedia: Multimedia = MultimediaService.getById(id)
        if multimedia:
            return send_from_directory("uploads", multimedia.archivo, as_attachment=True)
        else:
            # Not Found
            return {'Error': messages['not_found'].format(id)}, 404
    except FileNotFoundError as error:
        return {'Error': "La imagen no existe."}, 404  # Not Found
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@multimedia_controller.route("/imagenes/<int:id>")
def get_imagenes_by_cliente_id(id: int):
    try:
        result = MultimediaService.getImagenesByClienteId(id)
        if result:

            multimedias = multimedia_without_televisores_and_cliente.dump(
                result, many=True)

            return jsonify(multimedias)
        else:
            # Not Found
            return {'Error': f"El cliente con el id: {id} no tiene imagenes"}, 404
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@multimedia_controller.route("/videos/<int:id>")
def get_videos_by_cliente_id(id: int):
    try:
        result = MultimediaService.getVideosByClienteId(id)
        if result:

            multimedias = multimedia_without_televisores_and_cliente.dump(
                result, many=True)

            return jsonify(multimedias)
        else:
            # Not Found
            return {'Error': f"El cliente con el id: {id} no tiene videos"}, 404
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@multimedia_controller.route("/televisor/videos/<int:id>")
def get_videos_by_televisor_id(id: int):
    try:
        result_dict = MultimediaService.getVideosByTelevisorId(id)
        if result_dict:
            cliente = cliente_without_televisores.dump(result_dict['cliente'])
            televisor = televisor_without_multimedias_and_cliente.dump(
                result_dict['televisor'])
            multimedias = multimedia_without_televisores.dump(
                result_dict['multimedias'], many=True)

            return {'cliente': cliente, 'televisor': televisor, 'multimedias': multimedias}
        else:
            # Not Found
            return {'Error': f"El televisor con el id: {id} no tiene multimedias"}, 404
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@multimedia_controller.route("/televisor/<int:id>")
def get_multimedias_by_televisor_id(id: int):
    try:
        multimedias_dict = MultimediaService.getMultimediasByTelevisorId(id)
        if multimedias_dict:

            multimedias_dict = multimedia_without_televisores_and_cliente.dump(
                multimedias_dict, many=True)

            return jsonify(multimedias_dict)

        else:
            # Not Found
            return {'Error': f"El televisor con el id: {id} no tiene multimedias"}, 404
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@multimedia_controller.route("/cliente/<int:id>/<int:page>")
def getMultimediasByClienteIdWithPagination(id: int, page: int):
    try:
        print(page)
        result = MultimediaService.getMultimediasByClienteIdWithPagination(
            id, page)

        return result
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error


@multimedia_controller.route("/delete", methods=['PUT'], strict_slashes=False)
def delete():
    try:

        print(request.get_json())

        multimedias = MultimediaService.get_by_ids(
            request.get_json()['multimedias'])

        if multimedias:
            for multimedia in multimedias:
                multimedia.televisores.clear()
                multimedia.historiales.clear()

                MultimediaService.update()

            MultimediaService.delete(multimedias)

            return {"Message": "Multimedias eliminadas con exito."}, 200
        else:
            # Not Found
            return {'Error': "No se encontraron multimedias."}, 404
    except Exception as error:
        return {'Error': f"{error}"}, 500  # Internal Error
