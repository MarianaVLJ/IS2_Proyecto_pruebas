from abc import ABC, abstractmethod
from typing import List
from app.domain.models.publicacion import Publicacion


class PublicacionRepository(ABC):
    @abstractmethod
    def crear(self, publicacion: Publicacion) -> Publicacion:
        pass

    @abstractmethod
    def obtener(self) -> List[Publicacion]:
        pass

    @abstractmethod
    def editar(
        self,
        publicacion_id: str,
        nuevo_contenido: str,
        autor_alias: str
    ) -> bool:
        pass

    @abstractmethod
    def eliminar(self, publicacion_id: str, autor_alias: str) -> bool:
        pass
