from conexion_bd_mysql import db

association_table_usuario_role = db.Table('usuarios_roles', db.metadata, db.Column('usuario_id', db.ForeignKey(
    'usuarios.id'), primary_key=True), db.Column('role_id', db.ForeignKey('roles.id'), primary_key=True))


class Role(db.Model):

    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)

    # relacion con Televisor
    usuarios = db.relationship(
        "Usuario", secondary=association_table_usuario_role, back_populates="roles")

    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name

    @classmethod
    def constructor(cls, data):
        return cls(data.get('id'), data['name'])

    def __repr__(self) -> str:
        return f"Role => [id: {self.id}, name: {self.name}]"
