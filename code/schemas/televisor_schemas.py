from marshmallow import Schema, fields, validates, ValidationError, validate


class TelevisorSchema(Schema):
    id = fields.Int(required=True)
    ubicacion = fields.Str(required=True, validate=validate.Length(min=2))
    cliente_id = fields.Int(load_only=True, required=True)

    # Relacion
    cliente = fields.Nested("ClienteSchema", exclude=("televisores",))
    multimedias = fields.List(fields.Nested("MultimediaSchema", exclude=("televisores",)))

    @validates('ubicacion')
    def string_vacio(self, cadena: str):
        if len(cadena.strip()) == 0:
            raise ValidationError("El texto no puede ser vacio.")
