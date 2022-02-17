from conexion_bd_mysql import db
from typing import Dict
from models.televisor import association_table


class Multimedia(db.Model):
    __tablename__ = 'multimedias'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    archivo = db.Column(db.String(80), nullable=False)
    tipo_archivo = db.Column(db.String(80), nullable=False)

    # relacion
    televisores = db.relationship("Televisor", secondary=association_table, back_populates="multimedias")

    def __init__(self, id,  archivo, tipo_archivo) -> None:
        self.id = id
        self.archivo = archivo
        self.tipo_archivo = tipo_archivo

    @classmethod
    def constructor(cls, data: Dict):
        return cls(data.get('id'), data['archivo'], data['tipo_archivo'])

    def __repr__(self) -> str:
        return f"Multimedia => [id: {self.id}, archivo: {self.archivo}, tipo_archivo: {self.tipo_archivo}]"

    def __eq__(self, otro_mult):
        # Aquí puedes comparar cualquier cosa de los dos objetos. Debes regresar un Booleano
        return otro_mult.id == self.id
