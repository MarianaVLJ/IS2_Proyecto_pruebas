import unittest
import hashlib
import importlib
import app.domain.services.password_service as ps

# 🔁 Forzamos la recarga del módulo para evitar conflictos con Flask o imports previos
importlib.reload(ps)
from app.domain.services.password_service import PasswordService


class TestPasswordService(unittest.TestCase):
    """Pruebas unitarias para el módulo del dominio: PasswordService"""

    def setUp(self):
        """Se ejecuta antes de cada test."""
        self.password = "admin123"
        self.hashed = PasswordService.hash_password(self.password)

    def tearDown(self):
        """Se ejecuta después de cada test."""
        pass

    def test_hash_password_returns_string(self):
        """Verifica que el resultado sea un string."""
        self.assertIsInstance(self.hashed, str)

    def test_hash_password_not_plain(self):
        """Verifica que el hash no sea igual a la contraseña original."""
        self.assertNotEqual(self.password, self.hashed)

    def test_hash_password_reproducible(self):
        """Verifica que el hash sea determinista: misma entrada → mismo resultado."""
        again = PasswordService.hash_password(self.password)
        self.assertEqual(self.hashed, again)

    def test_hash_password_is_sha256(self):
        """Verifica que el hash tiene la longitud esperada de SHA-256 (64 caracteres hex)."""
        self.assertEqual(len(self.hashed), 64)

    def test_hash_password_manual_comparison(self):
        """Compara contra el resultado esperado calculado manualmente."""
        expected = hashlib.sha256(self.password.encode()).hexdigest()
        self.assertEqual(self.hashed, expected)


if __name__ == "__main__":
    unittest.main()
