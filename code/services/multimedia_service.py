from models.multimedia import Multimedia
from models.cliente import Cliente
from conexion_bd_mysql import db
from excepciones_personalizadas.excepciones import NotFound
from messages.es_ES import messages


class MultimediaService:

    @staticmethod
    def get_by_id(id: int):
        autor = Multimedia.query.filter_by(id=id).first()
        return autor

    @staticmethod
    def create(data):
        multimedia = Multimedia.constructor(data)

        cliente = Cliente.query.filter_by(id=data['cliente_id']).first()
        if not cliente:
            raise NotFound(messages['not_found'].format(data['cliente_id']))
        multimedia.cliente = cliente

        db.session.add(multimedia)
        db.session.commit()

    @staticmethod
    def get_all():
        autores = Multimedia.query.all()
        return autores
