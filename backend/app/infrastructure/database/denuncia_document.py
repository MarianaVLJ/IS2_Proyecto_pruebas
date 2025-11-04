from mongoengine import (
    ReferenceField, Document, StringField, DateTimeField, ListField
)
from app.infrastructure.database.user_document import UserDocument


class DenunciaDocument(Document):
    usuario = ReferenceField(UserDocument, required=True)
    categoria = StringField(required=True)
    descripcion = StringField(required=True, max_length=1000)
    lugar = StringField(required=True)
    fecha_hecho = DateTimeField()
    involucrados = ListField(StringField())
    evidencia = ListField(StringField())
    fecha_creacion = DateTimeField()

    meta = {
        'collection': 'denuncias',
        'ordering': ['-fecha_creacion'],
        'indexes': ['categoria', 'lugar']
    }
