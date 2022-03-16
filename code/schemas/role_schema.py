from marshmallow import Schema, fields, validates, ValidationError, validate


class RoleSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)

    # Relacion
    usuarios = fields.List(fields.Nested(
        "UsuarioSchema", only=('id', "email", "password")))
