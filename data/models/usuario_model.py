from dataclasses import dataclass


@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    hashed_password: str
    data_nascimento:  str
    sexo: str
    user_type: str
