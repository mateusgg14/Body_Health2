CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS profissional (
id INTEGER PRIMARY KEY,
tipo_profissional TEXT NOT NULL CHECK (tipo_profissional IN ('nutricionista', 'educador_fisico')),
status TEXT NOT NULL CHECK (status IN ('ativo', 'inativo')),
master INTEGER DEFAULT 0,
FOREIGN KEY (id) REFERENCES usuario(id)
"""

from dataclasses import dataclass

from data.models.usuario_model import Usuario


@dataclass
class Profissional(Usuario):
    tipo_profissional: str
    status: str
    master: bool

INSERIR = """
INSERT INTO profissional (tipo_profissional, status, master) 
VALUES (?, ?, ?)
"""

ALTERAR = """
UPDATE profissional
SET tipo_profissional=?, status=?, master=?
WHERE id=?
"""

EXCLUIR = """
DELETE FROM profissional
WHERE id=?
"""

OBTER_POR_ID = """
SELECT
p.id, p.tipo_profissional, p.status, p.master, u.nome, u.email, u.senha
FROM profissional p
INNER JOIN usuario u ON a.id = u.id
WHERE p.id=?
"""

OBTER_TODOS = """
SELECT 
p.id, p.tipo_profissional, p.status, p.master, u.nome, u.email, u.senha
FROM profissional p
INNER JOIN usuario u ON p.id = u.id
ORDER BY u.nome
"""