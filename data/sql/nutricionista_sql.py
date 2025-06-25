CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS nutricionista (
id INTEGER PRIMARY KEY,
crfa TEXT NOT NULL UNIQUE,
master INTEGER DEFAULT 0,
FOREIGN KEY (id) REFERENCES profissional(id)
"""

INSERIR = """
INSERT INTO nutricionista (crfa, master) 
VALUES (?, ?)
"""

from dataclasses import dataclass

from data.models.profissional_model import Profissional


@dataclass
class Nutricionista(Profissional):
    master: bool
    crfa: str



ALTERAR = """
UPDATE nutricionista
SET crfa=?, master=?
WHERE id=?
"""

EXCLUIR = """
DELETE FROM nutricionista
WHERE id=?
"""

OBTER_POR_ID = """
SELECT
n.id, n.crfa, n.master, u.nome, u.email, u.senha
FROM nutricionista n
INNER JOIN usuario u ON n.id = u.id
WHERE n.id=?
"""

OBTER_TODOS = """
SELECT 
n.id, n.crfa, n.master, u.nome, u.email, u.senha
FROM nutricionista n
INNER JOIN usuario u ON n.id = u.id
ORDER BY u.nome
"""