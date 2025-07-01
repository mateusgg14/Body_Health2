# data/sql/profissional_sql.py

CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS profissional (
    id INTEGER PRIMARY KEY,
    tipo_profissional TEXT NOT NULL CHECK (tipo_profissional IN ('nutricionista', 'educador_fisico')),
    status TEXT NOT NULL CHECK (status IN ('ativo', 'inativo')),
    FOREIGN KEY (id) REFERENCES usuario(id) ON DELETE CASCADE
);
"""

# CORREÇÃO: Adicionamos a coluna 'id' ao INSERT
INSERIR = """
INSERT INTO profissional (tipo_profissional, status) 
VALUES (?, ?)
"""

ALTERAR = """
UPDATE profissional
SET tipo_profissional = ?, status = ?
WHERE id = ?
"""

EXCLUIR = """
DELETE FROM profissional
WHERE id=?
"""

# CORREÇÃO: Alias 'p.id' e 'u.hashed_password'
OBTER_POR_ID = """
SELECT
    p.id, p.tipo_profissional, p.status, u.nome, u.email, u.hashed_password as senha
FROM
    profissional p
INNER JOIN
    usuario u ON p.id = u.id
WHERE
    p.id=?
"""

OBTER_TODOS = """
SELECT
    p.id, p.tipo_profissional, p.status, u.nome, u.email, u.hashed_password as senha
FROM
    profissional p
INNER JOIN
    usuario u ON p.id = u.id
ORDER BY
    u.nome
"""