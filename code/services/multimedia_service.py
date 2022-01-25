from models.multimedia import Multimedia
from conexion_bd_mysql import db


class MultimediaService:

    @staticmethod
    def get_by_id(id: int):
        autor = Multimedia.query.filter_by(id=id).first()
        return autor

    @staticmethod
    def create(data):
        cliente = Multimedia.constructor(data)
        db.session.add(cliente)
        db.session.commit()

    @staticmethod
    def get_all():
        autores = Multimedia.query.all()
        return autores
