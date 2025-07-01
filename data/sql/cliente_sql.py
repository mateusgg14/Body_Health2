CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS cliente (
    id INTEGER PRIMARY KEY,
    tipo_conta TEXT NOT NULL,
    FOREIGN KEY (id) REFERENCES usuario(id));
"""

INSERIR = """
INSERT INTO cliente (tipo_conta) 
VALUES (?)
"""

ALTERAR = """
UPDATE cliente (tipo_conta)
WHERE id=?
"""

EXCLUIR = """
DELETE FROM cliente
WHERE id=?
"""

OBTER_POR_ID = """
SELECT 
c.id, c.tipo_conta, u.nome, u.email, u.hashed_password, u.data_nascimento, u.sexo
FROM cliente c
INNER JOIN usuario u ON c.id = u.id
WHERE c.id=?
"""

OBTER_TODOS = """
SELECT 
c.id, c.tipo_conta), u.nome, u.email, u.hashed_password, u.data_nascimento, u.sexo
FROM cliente c
INNER JOIN usuario u ON c.id = u.id
ORDER BY u.nome
""" 