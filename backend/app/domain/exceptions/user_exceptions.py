class AliasYaExiste(Exception):
    pass

class InvalidUsernameError(Exception):
    """Se lanza cuando el alias del usuario no existe."""
    pass


class InvalidPasswordError(Exception):
    """Se lanza cuando la contraseña no coincide."""
    pass


