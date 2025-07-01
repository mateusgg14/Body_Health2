CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS admin (
id INTEGER PRIMARY KEY ,
master BOOLEAN NOT NULL DEFAULT 0,
FOREIGN KEY (id) REFERENCES usuario(id) ON DELETE CASCADE
);
"""

INSERIR = """
INSERT INTO admin (id, master) 
VALUES (?, ?)
"""

ALTERAR = """
UPDATE admin
SET master=?
WHERE id=?
"""

EXCLUIR = """
DELETE FROM admin
WHERE id=?
"""

OBTER_POR_ID = """
SELECT 
    a.id, 
    a.master, 
    u.nome, 
    u.email, 
    u.hashed_password, 
    u.data_nascimento, 
    u.sexo, 
    u.user_type
FROM admin a
INNER JOIN usuario u ON a.id = u.id
WHERE a.id=?
"""
OBTER_TODOS = """
SELECT 
a.id, a.master, u.nome, u.email, u.senha
FROM admin a
INNER JOIN usuario u ON a.id = u.id
ORDER BY u.nome
""" 