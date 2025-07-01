from dataclasses import dataclass

from data.models.usuario_model import Usuario


@dataclass
class Administrador(Usuario):
     master: bool 