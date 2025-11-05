import unittest
import hashlib
from unittest.mock import Mock
from app.application.use_cases.login_user import LoginUserUseCase
from app.domain.exceptions.user_exceptions import InvalidUsernameError, InvalidPasswordError
from app.domain.services.password_service import PasswordService
from unittest.mock import patch

class TestLoginUserUseCase(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        # 🔁 Restaurar el método original de forma global al finalizar todos los tests
        PasswordService.hash_password = staticmethod(
            lambda password: hashlib.sha256(password.encode()).hexdigest()
        )

    def setUp(self):
        # Simula el repositorio de usuarios
        self.mock_repo = Mock()
        self.mock_repo.find_by_alias = Mock()
        self.use_case = LoginUserUseCase(self.mock_repo)

    # Caso 1: Login correcto
    def test_login_correcto(self):
        user = Mock()
        user.password_hash = "admin123"
        self.mock_repo.find_by_alias.return_value = user

        with patch.object(PasswordService, "hash_password", return_value="admin123"):
            result = self.use_case.execute("admin", "admin1clear23")
            self.assertEqual(result, "Inicio de sesión exitoso")

    # Caso 2: Usuario no encontrado → debe lanzar InvalidUsernameError
    def test_usuario_invalido(self):
        self.mock_repo.find_by_alias.return_value = None
        with self.assertRaises(InvalidUsernameError):
            self.use_case.execute("usuario_invalido", "1234")

    # Caso 3: Contraseña incorrecta → debe lanzar InvalidPasswordError
    def test_contrasena_incorrecta(self):
        user = Mock()
        user.password_hash = "hash_correcto"
        self.mock_repo.find_by_alias.return_value = user

        with patch.object(PasswordService, "hash_password", return_value="hash_incorrecto"):
            with self.assertRaises(InvalidPasswordError):
                self.use_case.execute("admin", "mala_contra")

    # Caso 4: Alias vacío → debe lanzar InvalidUsernameError
    def test_alias_vacio(self):
        with self.assertRaises(InvalidUsernameError):
            self.use_case.execute("", "1234")

    # Caso 5: Error interno en el repositorio → debe lanzar Exception
    def test_error_interno_en_repo(self):
        self.mock_repo.find_by_alias.side_effect = Exception("Fallo en la base de datos")
        with self.assertRaises(Exception):
            self.use_case.execute("admin", "admin123")


if __name__ == "__main__":
    unittest.main()
