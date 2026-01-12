# Imports corregidos según la estructura DDD
from app.domain.users.user_repository import UserRepository
from app.domain.users.models.user import User
from app.infrastructure.database.user_document import UserDocument

class MongoUserRepository(UserRepository):
    """
    Implementación concreta para MongoDB. 
    Esta clase vive en Infraestructura y el Dominio no la conoce[cite: 271].
    """
    def find_by_alias(self, alias: str) -> User | None:
        # Busca en la base de datos usando el Documento de MongoEngine [cite: 264]
        doc = UserDocument.objects(alias=alias).first()
        if doc:
            # Mapeo de Documento (infra) a Entidad (dominio) [cite: 304]
            return User(id=str(doc.id), alias=doc.alias, password_hash=doc.password_hash)
        return None

    def save(self, user: User) -> None:
        # Convierte la entidad de dominio a un documento persistente [cite: 326]
        doc = UserDocument(
            alias=user.alias,
            password_hash=user.password_hash
        )
        doc.save()