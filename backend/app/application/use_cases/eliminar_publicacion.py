from app.domain.repositories.publicacion_repo import PublicacionRepository


class EliminarPublicacionUseCase:
    def __init__(self, repositorio: PublicacionRepository):
        self.repositorio = repositorio

    def execute(self, publicacion_id: str, autor_alias: str) -> bool:
        return self.repositorio.eliminar(publicacion_id, autor_alias)
