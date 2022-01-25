from marshmallow import Schema, fields, validate


class MultimediaSchema(Schema):
    id = fields.Int()
    nombre = fields.Str(required=True)
    time_to_start = fields.DateTime(required=True)
    cliente_id = fields.Int(load_only=True)

    # Relacion
    cliente = fields.Nested("ClienteSchema", exclude=("multimedias",))
