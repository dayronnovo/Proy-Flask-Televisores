# Aqui voy a poner todos los schemas para que no ocurra la importacion circular

from schemas.role_schema import RoleSchema
from schemas.usuario_schema import UsuarioSchema
from schemas.cliente_schemas import ClienteSchema
from schemas.televisor_schemas import TelevisorSchema
from schemas.multimedia_schema import MultimediaSchema
from schemas.archivos_schema import ArchivoSchema
from schemas.historial_de_programacion_schema import HistorialProgramacionSchema

# inicializando el ClienteSchema
cliente_schema = ClienteSchema()
cliente_without_televisores = ClienteSchema(exclude=("televisores",))
cliente_without_multimedias = ClienteSchema(exclude=("multimedias",))
cliente_without_multimedias_and_televisores = ClienteSchema(
    exclude=("multimedias", "televisores"))

# inicializando el TelevisorSchema
televisor_schema = TelevisorSchema()
televisor_without_multimedias = TelevisorSchema(exclude=("multimedias",))
televisor_without_cliente = TelevisorSchema(exclude=("cliente",))
televisor_without_multimedias_and_cliente = TelevisorSchema(
    exclude=("multimedias", "cliente", ))
televisor_without_multimedias_cliente_historiales = TelevisorSchema(
    exclude=("multimedias", "cliente", "historiales"))

# inicializando el MultimediaSchema
multimedia_schema = MultimediaSchema()
multimedia_without_televisores = MultimediaSchema(exclude=("televisores",))
multimedia_without_cliente = MultimediaSchema(exclude=("cliente",))
multimedia_without_televisores_and_cliente = MultimediaSchema(
    exclude=("televisores", "cliente"))
multimedia_without_televisores_and_cliente_historial = MultimediaSchema(
    exclude=("televisores", "cliente", "historiales"))
# inicializando el ArchivoSchema
archivo_schema = ArchivoSchema()

# inicializando el ArchivoSchema
historial_programacion_without_cliente_multimedia_televisor = HistorialProgramacionSchema(
    exclude=("cliente", "multimedias", "televisores"))
historial_programacion_without_cliente_televisor = HistorialProgramacionSchema(
    exclude=("cliente", "televisores"))
historial_programacion_without_cliente = HistorialProgramacionSchema(
    exclude=("cliente",))
historial_programacion = HistorialProgramacionSchema()

# inicializando el UsuarioSchema
usuario_schema = UsuarioSchema()
usuario_schema_without_roles = UsuarioSchema(exclude=("roles",))
# inicializando el RoleSchema
role_schema = RoleSchema()
role_schema_without_usuarios = RoleSchema(exclude=("usuarios", "id"))
