from app.domain.repositories.reaccion_repo import ReaccionRepository


class EliminarReaccionUseCase:
    def __init__(self, repositorio: ReaccionRepository):
        self.repositorio = repositorio

    def execute(
        self, usuario_id: str, publicacion_id: str, tipo: str
    ) -> bool:
        return self.repositorio.eliminar(usuario_id, publicacion_id, tipo)
