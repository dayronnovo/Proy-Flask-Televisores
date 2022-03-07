from marshmallow import Schema, fields, missing
from schemas.cliente_schemas import ClienteSchema
from datetime import datetime


class HistorialProgramacionSchema(Schema):
    id = fields.Int()
    hora_de_inicio = fields.Time()
    time_id = fields.Int()
    fecha = fields.Date(missing=datetime.today().strftime('%Y-%m-%d'))

    # Relacion con Televisor
    televisores = fields.List(fields.Nested(
        "TelevisorSchema", only=("id", "ubicacion")))
    # Relacion con Multimedia
    multimedias = fields.List(fields.Nested(
        "MultimediaSchema", only=("id", "archivo", "tipo_archivo")))
    # Relacion con Televisor
    cliente = fields.Nested("ClienteSchema", only=("id", "nombre"))
