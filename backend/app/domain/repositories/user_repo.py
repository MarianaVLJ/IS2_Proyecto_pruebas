from abc import ABC, abstractmethod
from app.domain.models.user import User


class UserRepository(ABC):
    @abstractmethod
    def find_by_alias(self, alias: str) -> User | None: pass

    @abstractmethod
    def save(self, user: User) -> None: pass
