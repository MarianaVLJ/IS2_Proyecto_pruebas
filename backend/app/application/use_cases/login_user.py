from app.domain.repositories.user_repo import UserRepository
from app.domain.services.password_service import PasswordService
from app.domain.exceptions.user_exceptions import InvalidUsernameError, InvalidPasswordError


class LoginUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, alias: str, password: str) -> str:
        # 🔹 Validación de alias vacío
        if not alias or alias.strip() == "":
            raise InvalidUsernameError("El alias no puede estar vacío.")

        user = self.user_repo.find_by_alias(alias)
        if not user:
            raise InvalidUsernameError("Usuario no encontrado")

        hashed_password = PasswordService.hash_password(password)
        if user.password_hash != hashed_password:
            raise InvalidPasswordError("Contraseña incorrecta")

        return "Inicio de sesión exitoso"
