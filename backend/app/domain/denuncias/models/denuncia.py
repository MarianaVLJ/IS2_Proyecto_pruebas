from datetime import datetime, timezone


class Denuncia:
    def __init__(
            self,
            usuario,
            categoria,
            descripcion,
            lugar,
            fecha_hecho=None,
            involucrados=None,
            evidencia=None):
        self.usuario = usuario
        self.categoria = categoria
        self.descripcion = descripcion
        self.lugar = lugar
        self.fecha_hecho = fecha_hecho or datetime.now(timezone.utc)
        self.involucrados = involucrados
        self.evidencia = evidencia
        self.fecha_creacion = datetime.now(timezone.utc)
