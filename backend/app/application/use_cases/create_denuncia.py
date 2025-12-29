from backend.app.domain.denuncias.models.denuncia import Denuncia

class CreateDenunciaUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, categoria, descripcion, lugar, fecha_hecho, involucrados, evidencia, usuario):
        denuncia = Denuncia(
            categoria=categoria,
            descripcion=descripcion,
            lugar=lugar,
            fecha_hecho=fecha_hecho,
            involucrados=involucrados,
            evidencia=evidencia,
            usuario=usuario
        )
        result = self.repo.save(denuncia)
        return result, True
