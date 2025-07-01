CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS educador_fisico (
id INTEGER PRIMARY KEY,
cref TEXT NOT NULL UNIQUE,
master INTEGER DEFAULT 0,
FOREIGN KEY (id) REFERENCES profissional(id)
"""

INSERIR = """
INSERT INTO educador_fisico (cref, master) 
VALUES (?, ?)
"""

ALTERAR = """
UPDATE educador_fisico
SET cref=?, master=?
WHERE id=?
"""

EXCLUIR = """
DELETE FROM educador_fisico
WHERE id=?
"""

OBTER_POR_ID = """
SELECT
c.id, c.cref, c.master, u.nome, u.email, u.senha
FROM educador_fisico c
INNER JOIN usuario u ON c.id = u.id
WHERE c.id=?
"""

OBTER_TODOS = """
SELECT 
c.id, c.cref, c.master, u.nome, u.email, u.senha
FROM educador_fisico c
INNER JOIN usuario u ON c.id = u.id
ORDER BY u.nome
"""