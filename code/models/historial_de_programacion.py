from conexion_bd_mysql import db
from models.televisor import association_table_historial_televisores
from models.multimedia import association_table_historial_multimedias


class HistorialProgramacion(db.Model):

    __tablename__ = 'historial_de_programacion'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hora_de_inicio = db.Column(db.Time, nullable=False)
    time_id = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.Date, nullable=False)

    # relacion con cliente (ManyToOne Unidireccional)
    cliente_id = db.Column(db.Integer, db.ForeignKey(
        'clientes.id'), nullable=False)
    cliente = db.relationship('Cliente')

    # relacion con multimedia (ManyToMany Bidireccional)
    multimedias = db.relationship(
        "Multimedia", secondary=association_table_historial_multimedias, back_populates="historiales")

    # relacion con Televisor (ManyToMany Bidireccional)
    televisores = db.relationship(
        "Televisor", secondary=association_table_historial_televisores, back_populates="historiales")

    def __init__(self, id, hora_de_inicio, time_id, fecha) -> None:
        self.id = id
        self.hora_de_inicio = hora_de_inicio
        self.time_id = time_id
        self.fecha = fecha

    @classmethod
    def constructor(cls, data):
        return cls(data.get('id'), data['hora_de_inicio'], data['time_id'], data['fecha'])

    def __repr__(self) -> str:
        return f"Historial_Programacion => [id: {self.id}, hora_de_inicio: {self.hora_de_inicio}, time_id: {self.time_id}, fecha: {self.fecha}]"
