from marshmallow import Schema, fields, validates, ValidationError, validate


class MultimediaSchema(Schema):
    id = fields.Int()
    nombre = fields.Str(required=True, validate=validate.Length(min=2))
    time_to_start = fields.DateTime(required=True)
    cliente_id = fields.Int(load_only=True, required=True)

    # Relacion
    cliente = fields.Nested("ClienteSchema", exclude=("multimedias",))

    @validates('nombre')
    def string_vacio(self, cadena: str):
        if len(cadena.strip()) == 0:
            raise ValidationError("El texto no puede ser vacio.")
