from models.cliente import Cliente
from conexion_bd_mysql import db


class ClienteService:

    @staticmethod
    def get_by_id(id: int):
        autor = Cliente.query.filter_by(id=id).first()
        return autor

    @staticmethod
    def create(data):
        cliente = Cliente.constructor(data)
        db.session.add(cliente)
        db.session.commit()

    @staticmethod
    def get_all():
        autores = Cliente.query.all()
        return autores
