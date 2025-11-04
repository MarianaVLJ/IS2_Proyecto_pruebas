from app.domain.repositories.denuncia_repo import DenunciaRepository
from app.domain.models.denuncia import Denuncia
from app.infrastructure.database.denuncia_document import DenunciaDocument


class MongoDenunciaRepository(DenunciaRepository):
    def save(self, denuncia: Denuncia) -> str:
        doc = DenunciaDocument(
            categoria=denuncia.categoria,
            descripcion=denuncia.descripcion,
            lugar=denuncia.lugar,
            fecha_hecho=denuncia.fecha_hecho,
            involucrados=denuncia.involucrados,
            evidencia=denuncia.evidencia,
            usuario=denuncia.usuario
        )
        doc.save()
        return str(doc.id)

    def find_by_id(self, denuncia_id: str) -> Denuncia | None:
        doc = DenunciaDocument.objects(id=denuncia_id).first()
        if not doc:
            return None
        return self._to_domain(doc)

    def find_by_user(self, user) -> list[Denuncia]:
        docs = DenunciaDocument.objects(
            usuario=user).order_by('-fecha_creacion')
        return [self._to_dict(doc) for doc in docs]

    """
    método privado: convierte un documento de Mongo
    en un objeto Denuncia de el dominio.
    """
    def _to_domain(self, doc: DenunciaDocument) -> Denuncia:
        return Denuncia(
            categoria=doc.categoria,
            descripcion=doc.descripcion,
            lugar=doc.lugar,
            fecha_hecho=doc.fecha_hecho,
            involucrados=doc.involucrados,
            evidencia=doc.evidencia,
            usuario=doc.usuario
        )

    """
    método auxiliar para convertir un documento/denuncia a diccionario
    """
    def _to_dict(self, doc: DenunciaDocument) -> dict:
        return {
            "id": str(doc.id),
            "categoria": doc.categoria,
            "descripcion": doc.descripcion,
            "lugar": doc.lugar,
            "fecha_hecho":
                doc.fecha_hecho.isoformat() if doc.fecha_hecho else None,
            "involucrados": doc.involucrados,
            "evidencia": doc.evidencia,
            "fecha_creacion":
                doc.fecha_creacion.isoformat() if doc.fecha_creacion else None,
        }
