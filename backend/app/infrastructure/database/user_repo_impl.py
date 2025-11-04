from app.domain.repositories.user_repo import UserRepository
from app.domain.models.user import User
from app.infrastructure.database.user_document import UserDocument


class MongoUserRepository(UserRepository):
    def find_by_alias(self, alias: str) -> User | None:
        doc = UserDocument.objects(alias=alias).first()
        if doc:
            return User(alias=doc.alias, password_hash=doc.password_hash)
        return None

    def save(self, user: User) -> None:
        doc = UserDocument(
            alias=user.alias,
            password_hash=user.password_hash
        )
        doc.save()
