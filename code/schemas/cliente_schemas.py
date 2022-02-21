from marshmallow import Schema, fields, validate, ValidationError, validates


class ClienteSchema(Schema):
    id = fields.Int(required=True)
    nombre = fields.Str(required=True, validate=validate.Length(min=2))

    # Relacion
    televisores = fields.List(fields.Nested("TelevisorSchema",), only=('id', 'ubicacion'))
    multimedias = fields.List(fields.Nested("MultimediaSchema",), only=('id', 'archivo', 'tipo_archivo'))

    @validates('nombre')
    def string_vacio(self, cadena: str):
        if len(cadena.strip()) == 0:
            raise ValidationError("El texto no puede ser vacio.")
