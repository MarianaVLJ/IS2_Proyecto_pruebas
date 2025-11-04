from app.domain.repositories.user_repo import UserRepository
from app.domain.services.password_service import PasswordService


class LoginUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, alias: str, password: str) -> str:
        user = self.user_repo.find_by_alias(alias)
        if not user:
            return "Usuario no encontrado"

        hashed_password = PasswordService.hash_password(password)
        if user.password_hash != hashed_password:
            return "Contraseña incorrecta"
        return "Inicio de sesión exitoso"
