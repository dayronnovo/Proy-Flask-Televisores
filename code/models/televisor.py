from conexion_bd_mysql import db
from typing import Dict

association_table = db.Table('televisor_multimedia', db.metadata,
                             db.Column('televisor_id', db.ForeignKey('televisores.id'), primary_key=True),
                             db.Column('multimedia_id', db.ForeignKey('multimedias.id'), primary_key=True)
                             )


class Televisor(db.Model):
    __tablename__ = 'televisores'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ubicacion = db.Column(db.String(80), nullable=False)

    # relacion con cliente
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    cliente = db.relationship('Cliente', back_populates="televisores")

    # relacion con multimedia
    multimedias = db.relationship("Multimedia", secondary=association_table, back_populates="televisores")

    def __init__(self, id, ubicacion) -> None:
        self.id = id
        self.ubicacion = ubicacion

    @classmethod
    def constructor(cls, data: Dict):
        return cls(data.get('id'), data['ubicacion'])

    def __repr__(self) -> str:
        return f"Televisor => [id: {self.id}, ubicacion: {self.ubicacion}]"
