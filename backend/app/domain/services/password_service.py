import hashlib

class PasswordService:
    @staticmethod
    def hash_password(password: str) -> str:
        # Aplica SHA-256 y devuelve el hash hexadecimal
        return hashlib.sha256(password.encode()).hexdigest()
