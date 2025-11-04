from app.domain.models.reaccion import Reaccion
from app.domain.repositories.reaccion_repo import ReaccionRepository
from datetime import datetime


class ReaccionarPublicacionUseCase:
    def __init__(self, repositorio: ReaccionRepository):
        self.repositorio = repositorio

    def execute(self, usuario_id: str, publicacion_id: str, tipo: str) -> bool:
        if self.repositorio.existe(usuario_id, publicacion_id):
            return False

        nueva_reaccion = Reaccion(
            usuario_id=usuario_id,
            publicacion_id=publicacion_id,
            tipo=tipo,
            fecha=datetime.now()
        )
        self.repositorio.crear(nueva_reaccion)
        return True
