from app.domain.repositories.user_repo import UserRepository
from app.domain.services.password_service import PasswordService
from app.domain.models.user import User


class RegisterUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, alias: str, password: str) -> bool:
        if self.user_repo.find_by_alias(alias):
            return False

        password_hash = PasswordService.hash_password(password)
        user = User.create(alias, password_hash)
        self.user_repo.save(user)
        return True
