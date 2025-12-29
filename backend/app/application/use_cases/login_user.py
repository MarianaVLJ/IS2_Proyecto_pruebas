from app.domain.repositories.user_repo import UserRepository
from app.domain.services.password_service import PasswordService
from app.domain.exceptions.user_exceptions import InvalidUsernameError, InvalidPasswordError

class LoginUserUseCase:
    """
    Caso de uso para el inicio de sesión de usuarios.
    Se aplicó Refactoring: Extract Method para separar validaciones de la lógica de negocio.
    """
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, alias: str, password: str) -> str:
        # 1. Validar entrada (Extract Method)
        self._validate_input_not_empty(alias)

        # 2. Buscar usuario
        user = self.user_repo.find_by_alias(alias)
        if not user:
            raise InvalidUsernameError("Usuario no encontrado")

        # 3. Verificar credenciales (Extract Method)
        self._verify_password_match(user, password)

        return "Inicio de sesión exitoso"

    def _validate_input_not_empty(self, alias: str):
        """Valida que el alias no sea nulo o vacío (Clean Code)."""
        if not alias or alias.strip() == "":
            raise InvalidUsernameError("El alias no puede estar vacío.")

    def _verify_password_match(self, user, password: str):
        """Encapsula la lógica de verificación de hashes (Encapsulamiento)."""
        hashed_password = PasswordService.hash_password(password)
        if user.password_hash != hashed_password:
            raise InvalidPasswordError("Contraseña incorrecta")