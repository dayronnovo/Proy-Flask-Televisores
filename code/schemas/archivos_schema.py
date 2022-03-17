from marshmallow import Schema, fields, validate
from werkzeug.datastructures import FileStorage
import os

TEXT = ('.txt',)
DOCUMENTS = tuple(
    '.rtf .odf .ods .gnumeric .abw .doc .docx .xls .xlsx'.split())
IMAGES = tuple('.jpg .jpe .jpeg .png .gif .svg .bmp'.split())
AUDIO = tuple('.wav .mp3 .aac .ogg .oga .flac'.split())
VIDEO = tuple('.mp4 .mov .wmv .avi .avchd .flv .f4v .swf .mkv'.split())
DATA = tuple('.csv .ini .json .plist .xml .yaml .yml'.split())
SCRIPTS = tuple('.js .php .pl .py .rb .sh'.split())
ARCHIVES = tuple('.gz .bz2 .zip .tar .tgz .txz .7z'.split())
EXECUTABLES = tuple('.so .exe .dll'.split())


class FileStorageField(fields.Field):
    default_error_messages = {
        "invalid": "El archivo no es valido."
    }

    def _deserialize(self, value: FileStorage, attr, data, **kwargs):
        extension = os.path.splitext(value.filename)[1].lower()
        if extension not in IMAGES + VIDEO:
            self.fail("Invalid Format")
        return value


class ArchivoSchema(Schema):
    archivo = FileStorageField(required=True)
