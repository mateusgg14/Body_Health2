from dataclasses import dataclass

from data.models.usuario_model import Usuario


@dataclass
class Cliente(Usuario):
    master: bool
