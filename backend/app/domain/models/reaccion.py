from dataclasses import dataclass
from datetime import datetime


@dataclass
class Reaccion:
    usuario_id: str
    publicacion_id: str
    tipo: str
    fecha: datetime
    id: str = None
