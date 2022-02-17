from marshmallow import Schema, fields


class MultimediaSchema(Schema):
    id = fields.Int()
    archivo = fields.String()
    tipo_archivo = fields.String()

    # Relacion
    televisores = fields.List(fields.Nested("TelevisorSchema", exclude=("multimedias",)))
