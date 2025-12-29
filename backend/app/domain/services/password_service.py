import hashlib

class PasswordService:
    @staticmethod
    def hash_password(plain_text_password: str) -> str:
        """Genera un hash SHA-256 para la contraseña proporcionada."""
        # 1. Convertir la cadena a bytes con un nombre que indique el formato
        password_in_bytes = plain_text_password.encode('utf-8')
        
        # 2. Generar el hash usando un nombre que identifique el algoritmo
        sha256_hash_engine = hashlib.sha256(password_in_bytes)
        
        # 3. Obtener el resultado hexadecimal descriptivo
        hashed_password_hex = sha256_hash_engine.hexdigest()
        
        return hashed_password_hex