CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS cliente (
id INTEGER PRIMARY KEY,
master INTEGER DEFAULT 0,
FOREIGN KEY (id) REFERENCES usuario(id)
"""

INSERIR = """
INSERT INTO cliente (master) 
VALUES (?)
"""

ALTERAR = """
UPDATE cliente
SET master=?
WHERE id=?
"""

EXCLUIR = """
DELETE FROM cliente
WHERE id=?
"""

OBTER_POR_ID = """
SELECT 
c.id, c.master, u.nome, u.email, u.senha, u.data_nascimento, u.sexo
FROM cliente c
INNER JOIN usuario u ON c.id = u.id
WHERE c.id=?
"""

OBTER_TODOS = """
SELECT 
c.id, c.master, u.nome, u.email, u.senha, u.data_nascimento, u.sexo
FROM cliente c
INNER JOIN usuario u ON c.id = u.id
ORDER BY u.nome
""" 