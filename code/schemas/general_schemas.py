# Aqui voy a poner todos los schemas para que no ocurra la importacion circular

# inicializando el ClienteSchema
from schemas.cliente_schemas import ClienteSchema
from schemas.televisor_schemas import TelevisorSchema
from schemas.multimedia_schema import MultimediaSchema
from schemas.archivos_schema import ArchivoSchema

cliente_schema = ClienteSchema()
cliente_without_televisores = ClienteSchema(exclude=("televisores",))

# inicializando el TelevisorSchema
televisor_schema = TelevisorSchema()
televisor_without_multimedias = TelevisorSchema(exclude=("multimedias",))
televisor_without_multimedias_and_cliente = TelevisorSchema(exclude=("multimedias", "cliente"))

# inicializando el MultimediaSchema
multimedia_schema = MultimediaSchema()
multimedia_without_televisores = MultimediaSchema(exclude=("televisores",))
# inicializando el ArchivoSchema
archivo_schema = ArchivoSchema()
