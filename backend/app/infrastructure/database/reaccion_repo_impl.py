from app.domain.models.reaccion import Reaccion as ReaccionModel
from app.domain.repositories.reaccion_repo import ReaccionRepository
from app.infrastructure.database.reaccion_document import (
    Reaccion as ReaccionDocument
)
from app.infrastructure.database.user_document import UserDocument
from app.infrastructure.database.publicacion_document import Publicacion
from datetime import datetime
from bson import ObjectId


class MongoReaccionRepository(ReaccionRepository):
    def crear(self, reaccion: ReaccionModel) -> ReaccionModel:
        documento = ReaccionDocument(
            usuario=UserDocument.objects.get(id=reaccion.usuario_id),
            publicacion=Publicacion.objects.get(id=reaccion.publicacion_id),
            tipo=reaccion.tipo,
            fecha=reaccion.fecha or datetime.now()
        )
        documento.save()
        reaccion.id = str(documento.id)
        return reaccion

    def existe(self, usuario_id: str, publicacion_id: str) -> bool:
        return ReaccionDocument.objects(
            usuario=usuario_id,
            publicacion=publicacion_id
        ).first() is not None

    def contar_por_tipo(self, publicacion_id: str) -> dict:
        pipeline = [
            {"$match": {"publicacion": ObjectId(publicacion_id)}},
            {"$group": {"_id": "$tipo", "total": {"$sum": 1}}}
        ]
        resultados = ReaccionDocument.objects.aggregate(*pipeline)
        conteo = {res["_id"]: res["total"] for res in resultados}
        return {
            "me_gusta": conteo.get("me_gusta", 0),
            "abrazo": conteo.get("abrazo", 0),
            "fuerza": conteo.get("fuerza", 0)
        }

    def eliminar(
        self, usuario_id: str, publicacion_id: str, tipo: str
    ) -> bool:
        result = ReaccionDocument.objects(
            usuario=ObjectId(usuario_id),
            publicacion=ObjectId(publicacion_id),
            tipo=tipo
        ).first()

        if result:
            result.delete()
            return True
        return False
