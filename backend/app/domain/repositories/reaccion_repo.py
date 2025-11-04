from abc import ABC, abstractmethod
from app.domain.models.reaccion import Reaccion


class ReaccionRepository(ABC):
    @abstractmethod
    def crear(self, reaccion: Reaccion) -> Reaccion:
        pass

    @abstractmethod
    def existe(self, usuario_id: str, publicacion_id: str) -> bool:
        pass

    @abstractmethod
    def contar_por_tipo(self, publicacion_id: str) -> dict:
        pass

    @abstractmethod
    def eliminar(
        self, usuario_id: str, publicacion_id: str, tipo: str
    ) -> bool:
        pass
