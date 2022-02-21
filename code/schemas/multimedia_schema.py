from marshmallow import Schema, fields
from schemas.cliente_schemas import ClienteSchema


class MultimediaSchema(Schema):
    id = fields.Int()
    archivo = fields.String()
    tipo_archivo = fields.String()

    # Relacion
    televisores = fields.List(fields.Nested("TelevisorSchema", only=("id", "ubicacion")))

    cliente = fields.Nested(lambda: ClienteSchema(only=('id', 'nombre')))
