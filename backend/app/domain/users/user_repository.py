from abc import ABC, abstractmethod
from app.domain.users.models.user import User

class UserRepository(ABC):
    @abstractmethod
    def find_by_alias(self, alias: str) -> User:
        pass