from dataclasses import dataclass

from data.models.usuario_model import Usuario


@dataclass
class Profissional(Usuario):
    tipo_profissional: str
    status: str
    master: bool

