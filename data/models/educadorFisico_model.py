from dataclasses import dataclass

from data.models.profissional_model import Profissional


@dataclass
class EducadorFisico(Profissional):
    cref: str
