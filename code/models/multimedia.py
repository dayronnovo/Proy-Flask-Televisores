from conexion_bd_mysql import db
from typing import Dict


class Multimedia(db.Model):
    __tablename__ = 'multimedias'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(80), nullable=False)
    time_to_start = db.Column(db.DateTime, nullable=False)

    # relacion
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    cliente = db.relationship('Cliente', back_populates="multimedias")

    def __init__(self, id, nombre, time_to_start) -> None:
        self.id = id
        self.nombre = nombre
        self.time_to_start = time_to_start

    @classmethod
    def constructor(cls, data: Dict):
        return cls(data.get('id'), data['nombre'], data['time_to_start'])

    def __repr__(self) -> str:
        return f"Autor => [id: {self.id}, nombre: {self.nombre}, time_to_start: {self.time_to_start}]"
