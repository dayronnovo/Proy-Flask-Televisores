from conexion_bd_mysql import db


class Cliente(db.Model):

    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(80), nullable=False)

    # Relacion con Televisor
    televisores = db.relationship('Televisor', back_populates='cliente', lazy=True)
    # Relacion con Multimedia
    multimedias = db.relationship('Multimedia', back_populates='cliente', lazy=True)

    def __init__(self, id, nombre) -> None:
        self.id = id
        self.nombre = nombre

    @classmethod
    def constructor(cls, data):
        return cls(data.get('id'), data['nombre'])

    def __repr__(self) -> str:
        return f"Cliente => [id: {self.id}, nombre: {self.nombre}]"
