from app.domain.repositories.publicacion_repo import PublicacionRepository


class EditarPublicacionUseCase:
    def __init__(self, repositorio: PublicacionRepository):
        self.repositorio = repositorio

    def execute(
        self,
        publicacion_id: str,
        nuevo_contenido: str,
        autor_alias: str
    ) -> bool:
        return self.repositorio.editar(
            publicacion_id,
            nuevo_contenido,
            autor_alias
        )
