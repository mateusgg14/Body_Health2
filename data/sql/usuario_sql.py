CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS usuario (
id INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL,
email TEXT NOT NULL,
hashed_password TEXT NOT NULL,
data_nascimento TEXT NOT NULL,
sexo TEXT NOT NULL,
user_type TEXT NOT NULL CHECK (user_type IN ('cliente', 'profissional', 'administrador'))
);
"""

INSERIR = """
INSERT INTO usuario (nome, email, hashed_password, data_nascimento, sexo, user_type)
VALUES (?, ?, ?, ?, ?, ?)
"""

ALTERAR = """
UPDATE usuario
SET nome=?, email=?, data_nascimento=?, sexo=?, user_type=?
WHERE id=?
"""

ALTERAR_SENHA = """
UPDATE usuario
SET hashed_password=?
WHERE id=?
"""

EXCLUIR = """
DELETE FROM usuario
WHERE id=?
"""

OBTER_POR_ID = """
SELECT 
id, nome, email, hashed_password, data_nascimento, sexo, user_type
FROM usuario
WHERE id=?
"""

OBTER_TODOS = """
SELECT 
id, nome, email, hashed_password, data_nascimento, sexo, user_type
FROM usuario
ORDER BY nome
"""