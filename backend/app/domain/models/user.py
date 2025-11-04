from dataclasses import dataclass


@dataclass
class User:
    alias: str
    password_hash: str

    @staticmethod
    def create(alias: str, password_hash: str) -> 'User':
        return User(alias=alias, password_hash=password_hash)
