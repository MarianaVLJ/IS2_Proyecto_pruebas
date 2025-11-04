from datetime import datetime
from mongoengine import (
    Document, StringField, DateTimeField, ReferenceField,
    BooleanField
)
from app.infrastructure.database.user_document import UserDocument


class Publicacion(Document):
    contenido = StringField(required=True, max_length=1000)
    fecha_creacion = DateTimeField(default=datetime.now)
    fecha_actualizacion = DateTimeField(default=datetime.now)
    usuario = ReferenceField(UserDocument, required=True)
    anonimo = BooleanField(default=False)

    meta = {
        "collection": "publicaciones",
        "indexes": ["-fecha_creacion"]
    }
