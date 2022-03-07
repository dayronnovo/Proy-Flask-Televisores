from marshmallow import Schema, fields
from schemas.cliente_schemas import ClienteSchema


class MultimediaSchema(Schema):
    id = fields.Int()
    archivo = fields.String()
    tipo_archivo = fields.String()

    # Relacion
    televisores = fields.List(fields.Nested(
        "TelevisorSchema", only=("id", "ubicacion")))

    # Relacion
    historiales = fields.List(fields.Nested("HistorialProgramacionSchema", only=(
        "id", "hora_de_inicio", "time_id", "fecha")))

    cliente = fields.Nested(lambda: ClienteSchema(only=('id', 'nombre')))
