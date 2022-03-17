from marshmallow import Schema, fields, validates, ValidationError, validate
import re


class UsuarioSchema(Schema):
    id = fields.Int(required=True)
    user_name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    active = fields.Bool(load_default=True)

    # Relacion
    roles = fields.List(fields.Nested(
        "RoleSchema", only=('id', "name")))

    @validates("email")
    def validate_quantity(self, value):
        if not re.search("[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$", value):
            raise ValidationError("El formato del email no es correcto.")
