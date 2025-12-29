from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Publicacion:
    contenido: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    usuario: str
    anonimo: bool
    id: Optional[str] = field(default=None)
