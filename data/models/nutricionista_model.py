from dataclasses import dataclass

from data.models.profissional_model import Profissional


@dataclass
class Nutricionista(Profissional):
    master: bool
    crfa: str
