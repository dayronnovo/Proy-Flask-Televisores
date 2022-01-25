from marshmallow import Schema, fields, validate


class ClienteSchema(Schema):
    id = fields.Int()
    nombre = fields.Str(required=True)

    # Relacion
    multimedias = fields.List(fields.Nested("MultimediaSchema", exclude=("cliente",)))
