from mongoengine import Document, StringField, ReferenceField, DateTimeField
from datetime import datetime
from app.infrastructure.database.user_document import UserDocument
from app.infrastructure.database.publicacion_document import Publicacion


class Reaccion(Document):
    usuario = ReferenceField(UserDocument, required=True)
    publicacion = ReferenceField(Publicacion, required=True)
    tipo = StringField(required=True, choices=["me_gusta", "abrazo", "fuerza"])
    fecha = DateTimeField(default=datetime.now)

    meta = {
        "collection": "reacciones",
        "indexes": [
            {
                "fields": ["usuario", "publicacion"],
                "unique": True
            }
        ]
    }
