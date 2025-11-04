from app.domain.repositories.publicacion_repo import PublicacionRepository
from app.domain.models.publicacion import Publicacion


class ObtenerPublicacionesUseCase:
    def __init__(self, repositorio: PublicacionRepository):
        self.repositorio = repositorio

    def execute(self) -> list[Publicacion]:
        return self.repositorio.obtener()
