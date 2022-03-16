from marshmallow import Schema, fields, validates, ValidationError, validate


class UsuarioSchema(Schema):
    id = fields.Int(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)

    # Relacion
    roles = fields.List(fields.Nested(
        "RoleSchema", only=('id', "name")))
