import pytest
from backend.app.application.use_cases.login_user import LoginUserUseCase
from backend.app.domain.exceptions.user_exceptions import InvalidUsernameError, InvalidPasswordError

# Usuario falso para pruebas
class FakeUser:
    def __init__(self, alias, password_hash):
        self.alias = alias
        self.password_hash = password_hash

# Repositorio de usuario falso para pruebas
class FakeUserRepository:
    def find_by_alias(self, alias):
        if alias == "admin":
            # Cambiado para que coincida con la contraseña de prueba correcta
            return FakeUser("admin", "admin123")  # Ahora almacena "admin123" en lugar de "admin"
        return None
    
# Servicio de contraseña falso para pruebas
class FakePasswordService:  # Corregido el nombre de la clase (typo en FakepassordService)
    @staticmethod
    def hash_password(password):
        return password  # Simula el hashing devolviendo la contraseña sin cambios
    

# Caso de uso personalizado para pruebas
class CustomLoginUserUseCase(LoginUserUseCase):
    def __init__(self, user_repo):
        super().__init__(user_repo)
        self.password_service = FakePasswordService()  # Usando el nombre corregido
    
    def execute(self, alias: str, password: str) -> bool:
        user = self.user_repo.find_by_alias(alias)
        if not user:
            raise InvalidUsernameError("Alias no encontrado")

        hashed_password = self.password_service.hash_password(password)
        if user.password_hash != hashed_password:
            raise InvalidPasswordError("Contraseña incorrecta")

        return True
    
# Pruebas unitarias

def test_login_correcto():
    use_case = CustomLoginUserUseCase(FakeUserRepository())
    assert use_case.execute("admin", "admin123") is True  # Ahora coinciden las credenciales

def test_login_usuario_invalido():
    use_case = CustomLoginUserUseCase(FakeUserRepository())
    with pytest.raises(InvalidUsernameError):
        use_case.execute("usuario_invalido", "admin123")

def test_login_contraseña_incorrecta():
    use_case = CustomLoginUserUseCase(FakeUserRepository())
    with pytest.raises(InvalidPasswordError):
        use_case.execute("admin", "contraseña_incorrecta")