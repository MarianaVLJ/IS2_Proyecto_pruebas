from app.domain.models.publicacion import Publicacion
from app.infrastructure.database.publicacion_document import (
    Publicacion as PublicacionDocument
)
from app.domain.repositories.publicacion_repo import PublicacionRepository
from mongoengine.errors import DoesNotExist
from datetime import datetime


class MongoPublicacionRepository(PublicacionRepository):
    def crear(self, publicacion: Publicacion) -> Publicacion:
        publicacion_document = PublicacionDocument(
            contenido=publicacion.contenido,
            fecha_creacion=publicacion.fecha_creacion,
            fecha_actualizacion=publicacion.fecha_actualizacion,
            usuario=publicacion.usuario,
            anonimo=publicacion.anonimo
        )
        publicacion_document.save()
        publicacion.id = str(publicacion_document.id)
        return publicacion

    def obtener(self) -> list[Publicacion]:
        publicacion_document = PublicacionDocument.objects.order_by(
            "-fecha_creacion"
        )
        publicaciones = []

        for doc in publicacion_document:
            if doc.anonimo:
                usuario_nombre = "Anonimo"
            else:
                usuario_nombre = doc.usuario.alias
            publicaciones.append(Publicacion(
                contenido=doc.contenido,
                fecha_creacion=doc.fecha_creacion,
                fecha_actualizacion=doc.fecha_actualizacion,
                usuario=str(usuario_nombre),
                anonimo=doc.anonimo,
                id=str(doc.id)
            ))

        return publicaciones

    def editar(
        self,
        publicacion_id: str,
        nuevo_contenido: str,
        autor_alias: str
    ) -> bool:
        try:
            publicacion = PublicacionDocument.objects.get(id=publicacion_id)
            if publicacion.usuario.alias != autor_alias:
                return False

            publicacion.contenido = nuevo_contenido
            publicacion.fecha_actualizacion = datetime.now()
            publicacion.save()
            return True
        except DoesNotExist:
            return False

    def eliminar(self, publicacion_id: str, autor_alias: str) -> bool:
        try:
            publicacion = PublicacionDocument.objects.get(id=publicacion_id)
            if publicacion.usuario.alias != autor_alias:
                return False

            publicacion.delete()
            return True
        except DoesNotExist:
            return False
