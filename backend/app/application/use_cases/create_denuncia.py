from app.domain.repositories.denuncia_repo import DenunciaRepository
from app.domain.models.denuncia import Denuncia


class CreateDenunciaUseCase:
    def __init__(self, denuncia_repo: DenunciaRepository):
        self.denuncia_repo = denuncia_repo

    def execute(
            self,
            categoria,
            descripcion,
            lugar,
            fecha_hecho,
            involucrados,
            evidencia,
            usuario):
        denuncia = Denuncia(
            categoria=categoria,
            descripcion=descripcion,
            lugar=lugar,
            fecha_hecho=fecha_hecho,
            involucrados=involucrados,
            evidencia=evidencia,
            usuario=usuario
        )
        saved_doc = self.denuncia_repo.save(denuncia)
        return saved_doc, True
