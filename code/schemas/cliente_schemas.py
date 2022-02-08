from marshmallow import Schema, fields, validate, ValidationError, validates


class ClienteSchema(Schema):
    id = fields.Int(required=True)
    nombre = fields.Str(required=True, validate=validate.Length(min=2))

    # Relacion
    televisores = fields.List(fields.Nested("TelevisorSchema"), exclude=("cliente",))

    @validates('nombre')
    def string_vacio(self, cadena: str):
        if len(cadena.strip()) == 0:
            raise ValidationError("El texto no puede ser vacio.")
