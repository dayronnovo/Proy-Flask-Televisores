from marshmallow import Schema, fields, validates, ValidationError, validate
from schemas.archivos_schema import FileStorageField


class MultimediaSchema(Schema):
    id = fields.Int()
    archivo = fields.String()

    # Relacion
    televisores = fields.List(fields.Nested("TelevisorSchema", exclude=("multimedias",)))
