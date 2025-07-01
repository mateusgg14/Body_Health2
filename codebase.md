# .coveragerc

```
[run]
source = .
omit = 
    */.venv/*
    */tests/*
    */test_*
    setup.py
    main.py
    */migrations/*
    */venv/*
    */env/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstract

[html]
directory = htmlcov
```

# .vscode\launch.json

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "FastAPI",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "main:app",
                "--reload",
                "--port",
                "8000"
            ],
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```

# .vscode\settings.json

```json
{
    "python.testing.pytestArgs": [
        "Body_Health2-main"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true
}
```

# dados.db

```db

```

# data\models\administrador_model.py

```py
from dataclasses import dataclass

from data.models.usuario_model import Usuario


@dataclass
class Administrador(Usuario):
     master: bool 
```

# data\models\cliente_model.py

```py
from dataclasses import dataclass

from data.models.usuario_model import Usuario


@dataclass
class Cliente(Usuario):
    pass
```

# data\models\educadorFisico_model.py

```py
from dataclasses import dataclass

from data.models.profissional_model import Profissional


@dataclass
class EducadorFisico(Profissional):
    cref: str

```

# data\models\nutricionista_model.py

```py
from dataclasses import dataclass

from data.models.profissional_model import Profissional


@dataclass
class Nutricionista(Profissional):
    crfa: str

```

# data\models\profissional_model.py

```py
from dataclasses import dataclass
from data.models.usuario_model import Usuario

@dataclass
class Profissional(Usuario):
    tipo_profissional: str
    status: str

```

# data\models\usuario_model.py

```py
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

```

# data\repo\administrador_repo.py

```py
from typing import Optional
from data.models.usuario_model import *
from data.models.administrador_model import Administrador
from data.sql.administrador_sql import *
from data.models.usuario_model import Usuario
from data.repo import usuario_repo
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0

def inserir(administrador: Administrador) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(0, 
            administrador.nome, 
            administrador.email, 
            administrador.hashed_password,
            administrador.data_nascimento,
            administrador.sexo,
            administrador.user_type)
        id_usuario = usuario_repo.inserir(usuario, cursor)
        cursor.execute(INSERIR, (
            id_usuario,
            administrador.master))
        return id_usuario

def alterar(administrador: Administrador) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(administrador.id, 
            administrador.nome, 
            administrador.email, 
            administrador.hashed_password,
            administrador.data_nascimento,
            administrador.sexo,
            administrador.user_type)
        usuario_repo.alterar(usuario, cursor)
        cursor.execute(ALTERAR, (
            administrador.master,
            administrador.id))
        return (cursor.rowcount > 0)
    
def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        usuario_repo.excluir(id, cursor)
        return (cursor.rowcount > 0)

def obter_por_id(id: int) -> Optional[Administrador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        admin = Administrador(
            id=row["id"],
            nome=row["nome"],
            email=row["email"],
            senha=row["senha"],
            master=row["master"])
        return admin
    
def obter_todos() -> list[Administrador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        admins = [
            Administrador(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                master=row["master"])
                for row in rows]
        return admins
```

# data\repo\cliente_repo.py

```py
from typing import Optional
from data.repo import usuario_repo
from data.models.cliente_model import Cliente
from data.sql.cliente_sql import *
from data.models.usuario_model import Usuario
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount >= 0

def inserir(cliente: Cliente) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(
            id=None,
            nome=cliente.nome,
            email=cliente.email,
            hashed_password=cliente.hashed_password,
            data_nascimento=cliente.data_nascimento,
            sexo=cliente.sexo,
            user_type="cliente"
        )
        id_usuario = usuario_repo.inserir(usuario, cursor)
        if id_usuario:
            cursor.execute(INSERIR, (cliente.master,))
            conn.commit()
            return id_usuario
        return None

def alterar(cliente: Cliente) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(
            id=cliente.id,
            nome=cliente.nome,
            email=cliente.email,
            hashed_password=cliente.hashed_password,
            data_nascimento=cliente.data_nascimento,
            sexo=cliente.sexo,
            user_type="cliente"
        )
        usuario_repo.alterar(usuario, cursor)
        cursor.execute(ALTERAR, (cliente.master, cliente.id))
        conn.commit()
        return cursor.rowcount > 0

def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        usuario_repo.excluir(id, cursor)
        conn.commit()
        return cursor.rowcount > 0

def obter_por_id(id: int) -> Optional[Cliente]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return Cliente(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                hashed_password=row["senha"],
                data_nascimento=["data_nascimento"],  
                sexo=["sexo"],             
                master=bool(row["master"])
            )
        return None

def obter_todos() -> list[Cliente]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        return [
            Cliente(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                hashed_password=row["senha"],
                data_nascimento=["data_nascimento"], 
                sexo=["sexo"],             
                master=bool(row["master"])
            ) for row in rows
        ]

```

# data\repo\educadorFisico_repo.py

```py
from typing import Optional
from data.models.educadorFisico_model import EducadorFisico
from data.repo import profissional_repo
from data.sql.educadorFisico_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0

def inserir(educador: EducadorFisico) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        id_profissional = profissional_repo.inserir(educador)
        if id_profissional is None:
            return None
        cursor.execute(INSERIR, (
            educador.cref,
            int(educador.master)
        ))
        conn.commit()
        return id_profissional

def alterar(educador: EducadorFisico) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        ok_profissional = profissional_repo.alterar(educador)
        cursor.execute(ALTERAR, (
            educador.cref,
            int(educador.master),
            educador.id
        ))
        conn.commit()
        return ok_profissional and cursor.rowcount > 0

def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        ok_especializacao = cursor.rowcount > 0
        ok_profissional = profissional_repo.excluir(id)
        conn.commit()
        return ok_especializacao and ok_profissional

def obter_por_id(id: int) -> Optional[EducadorFisico]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if not row:
            return None
        return EducadorFisico(
            id=row["id"],
            nome=row["nome"],
            email=row["email"],
            senha=row["senha"],
            data_nascimento="",
            sexo="",
            user_type="profissional",
            tipo_profissional="educador_fisico",
            status="ativo",  # valor padrão
            master=bool(row["master"]),
            cref=row["cref"]
        )

def obter_todos() -> list[EducadorFisico]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        return [
            EducadorFisico(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                data_nascimento="",
                sexo="",
                user_type="profissional",
                tipo_profissional="educador_fisico",
                status="ativo",  # valor padrão
                master=bool(row["master"]),
                cref=row["cref"]
            ) for row in rows
        ]

```

# data\repo\nutricionista_repo.py

```py
from typing import Optional
from data.models.nutricionista_model import Nutricionista
from data.repo import profissional_repo
from data.sql.nutricionista_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return cursor.rowcount > 0

def inserir(nutricionista: Nutricionista) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        id_profissional = profissional_repo.inserir(nutricionista)
        if id_profissional is None:
            return None
        cursor.execute(INSERIR, (
            nutricionista.crfa,
            int(nutricionista.master)
        ))
        conn.commit()
        return id_profissional

def alterar(nutricionista: Nutricionista) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        ok_profissional = profissional_repo.alterar(nutricionista)
        cursor.execute(ALTERAR, (
            nutricionista.crfa,
            int(nutricionista.master),
            nutricionista.id
        ))
        conn.commit()
        return ok_profissional and cursor.rowcount > 0

def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        ok_nutricionista = cursor.rowcount > 0
        ok_profissional = profissional_repo.excluir(id)
        conn.commit()
        return ok_nutricionista and ok_profissional

def obter_por_id(id: int) -> Optional[Nutricionista]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if not row:
            return None
        return Nutricionista(
            id=row["id"],
            nome=row["nome"],
            email=row["email"],
            senha=row["senha"],
            data_nascimento="",
            sexo="",
            user_type="profissional",
            tipo_profissional="nutricionista",
            status="ativo",  # valor padrão
            master=bool(row["master"]),
            crfa=row["crfa"]
        )

def obter_todos() -> list[Nutricionista]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        return [
            Nutricionista(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                data_nascimento="",
                sexo="",
                user_type="profissional",
                tipo_profissional="nutricionista",
                status="ativo",  # valor padrão
                master=bool(row["master"]),
                crfa=row["crfa"]
            ) for row in rows
        ]

```

# data\repo\profissional_repo.py

```py
from typing import Optional
from data.models.profissional_model import Profissional
from data.sql.profissional_sql import *
from data.repo import usuario_repo
from data.util import get_connection

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
        return False

def inserir(profissional: Profissional) -> Optional[int]:
     with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            profissional.nome,
            profissional.email,
            profissional.hashed_password,
            profissional.data_nascimento,
            profissional.sexo,
            profissional.user_type,
            profissional.tipo_profissional,
            profissional.status))
        return cursor.lastrowid

def alterar(profissional: Profissional) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            usuario = usuario_repo.alterar(profissional, cursor)
            cursor.execute(
                ALTERAR,
                (profissional.tipo_profissional, profissional.status)
            )
            profissional = cursor.rowcount > 0
            conn.commit()
            return usuario and profissional
        except Exception as e:
            conn.rollback()
            print(f"Erro ao alterar profissional: {e}")
            return False

def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            usuario = usuario_repo.excluir(id, cursor)
            conn.commit()
            return usuario
        except Exception as e:
            conn.rollback()
            print(f"Erro ao excluir profissional: {e}")
            return False

def obter_por_id(id: int) -> Optional[Profissional]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Profissional(
            id=row["id"],
            nome=row["nome"],
            email=row["email"],
            hashed_password=row["senha"],
            data_nascimento="",
            sexo="",
            user_type="profissional",
            tipo_profissional=row["tipo_profissional"],
            status=row["status"])        

def obter_todos() -> list[Profissional]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        return [
            Profissional(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                hashed_password=row["senha"],
                data_nascimento="",
                sexo="",
                user_type="profissional",
                tipo_profissional=row["tipo_profissional"],
                status=row["status"]
            )
            for row in rows
        ]

```

# data\repo\usuario_repo.py

```py
from typing import Any, Optional
from data.models.usuario_model import Usuario
from data.sql.usuario_sql import *
from data.util import *

def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
        return False


def inserir(usuario: Usuario) -> Optional[int]:
     with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            usuario.nome,
            usuario.email,
            usuario.hashed_password,
            usuario.data_nascimento,
            usuario.sexo,
            usuario.user_type))
        return cursor.lastrowid
    
def alterar(usuario: Usuario) -> bool:
     with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (
            usuario.nome,
            usuario.email,
            usuario.data_nascimento,
            usuario.sexo,
            usuario.user_type,
            usuario.id))
        return (cursor.rowcount > 0)
    
def atualizar_senha(id: int, hashed_password: str) -> bool:
     with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR_SENHA, (hashed_password, id))
        return (cursor.rowcount > 0)
    
# data/repo/usuario_repo.py

# Em data/repo/usuario_repo.py

def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        
        # ESSA LINHA É ESSENCIAL para salvar a exclusão no banco de dados.
        conn.commit()
        
        return (cursor.rowcount > 0)
    
def obter_por_id(id: int) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()

        # ESTA VERIFICAÇÃO É A CORREÇÃO NECESSÁRIA
        if row is None:
            return None

        # O código abaixo só será executado se um usuário for encontrado
        usuario = Usuario(
            id=row["id"],
            nome=row["nome"],
            email=row["email"],
            hashed_password=row["hashed_password"],
            data_nascimento=row["data_nascimento"],
            sexo=row["sexo"],
            user_type=row["user_type"]
        )
        return usuario

def obter_todos() -> list[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        usuarios = [
            Usuario(
                id=row["id"], 
                nome=row["nome"],
                email=row["email"],
                senha=row["hashed_password"],
                data_nascimento=row["data_nascimento"],
                sexo=row["sexo"],
                user_type=row["user_type"]) 
                for row in rows]
        return usuarios
```

# data\sql\administrador_sql.py

```py
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS admin (
id INTEGER PRIMARY KEY,
master INTEGER DEFAULT 0,
FOREIGN KEY (id) REFERENCES usuario(id)
"""

INSERIR = """
INSERT INTO admin (master) 
VALUES (?)
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
a.id, a.master, u.nome, u.email, u.senha
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
```

# data\sql\cliente_sql.py

```py
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
```

# data\sql\educadorFisico_sql.py

```py
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
```

# data\sql\nutricionista_sql.py

```py
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
```

# data\sql\profissional_sql.py

```py
# data/sql/profissional_sql.py

CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS profissional (
    id INTEGER PRIMARY KEY,
    tipo_profissional TEXT NOT NULL CHECK (tipo_profissional IN ('nutricionista', 'educador_fisico')),
    status TEXT NOT NULL CHECK (status IN ('ativo', 'inativo')),
    master INTEGER DEFAULT 0,
    FOREIGN KEY (id) REFERENCES usuario(id) ON DELETE CASCADE
);
"""

# CORREÇÃO: Adicionamos a coluna 'id' ao INSERT
INSERIR = """
INSERT INTO profissional (id, tipo_profissional, status, master) 
VALUES (?, ?, ?, ?)
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

# CORREÇÃO: Alias 'p.id' e 'u.hashed_password'
OBTER_POR_ID = """
SELECT
    p.id, p.tipo_profissional, p.status, p.master, u.nome, u.email, u.hashed_password as senha
FROM
    profissional p
INNER JOIN
    usuario u ON p.id = u.id
WHERE
    p.id=?
"""

OBTER_TODOS = """
SELECT
    p.id, p.tipo_profissional, p.status, p.master, u.nome, u.email, u.hashed_password as senha
FROM
    profissional p
INNER JOIN
    usuario u ON p.id = u.id
ORDER BY
    u.nome
"""
```

# data\sql\usuario_sql.py

```py
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
```

# data\util.py

```py
import sqlite3
import os

def get_connection():
    database_path = os.environ.get('TEST_DATABASE_PATH', 'dados.db')
    conexao = sqlite3.connect(database_path)
    conexao.row_factory = sqlite3.Row
    return conexao
```

# main.py

```py
print("Repositório com testes.")
```

# pytest.ini

```ini
[tool:pytest]
# Diretórios onde o pytest deve procurar por testes
testpaths = tests

# Padrões de arquivos de teste
python_files = test_*.py *_test.py

# Padrões de classes de teste
python_classes = Test*

# Padrões de funções de teste
python_functions = test_*

# Marcadores personalizados
markers =
    slow: marca testes que demoram para executar
    integration: marca testes de integração
    unit: marca testes unitários

# Opções padrão do pytest COM coverage
addopts = 
    -v
    --strict-markers
    --disable-warnings
    --color=yes
    --tb=short
    --maxfail=1
    --strict-config
    --cov=.
    --cov-report=html
    --cov-report=term-missing:skip-covered
    --cov-config=.coveragerc

# Filtros de warnings
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning

# Configuração de log
log_cli = false
log_cli_level = INFO

# Formato de saída mais limpo
console_output_style = progress
```

# README.md

```md

```

# requirements.txt

```txt
fastapi[standard]
uvicorn[standard]
jinja2
Babel
python-multipart
itsdangerous

# Dependências de teste
pytest
pytest-asyncio
pytest-cov
```

# templates\1.DashboardInicial.html

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Body Health</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
    <link rel="" href="">
    <style>
        :root {
            /* Cores para o tema escuro - Consistente com as outras páginas */
            --dark-bg: #1a1a1a; /* Fundo principal muito escuro */
            --dark-card-bg: #2b2b2b; /* Fundo dos cards */
            --dark-text-color: #e0e0e0; /* Cor de texto padrão clara (quase branca) */
            --dark-muted-text: #b0b0b0; /* Texto muted mais claro */
            --dark-border-color: #444444; /* Bordas mais escuras */
            --dark-shadow-color: rgba(0,0,0,0.5); /* Sombra mais intensa */
            --highlight-yellow: #ffc107; /* Amarelo de destaque */
            --highlight-green: #28a745; /* Verde para checks */
            --highlight-red: #dc3545; /* Vermelho para X */

            /* Cores para o banner claro (se quiser manter um elemento claro) */
            --light-banner-bg-start: #ffffff;
            --light-banner-bg-end: #eaeaea;
            --light-banner-text: #000000;
        }

        body {
            background-color: var(--dark-bg);
            color: var(--dark-text-color);
            font-family: Arial, sans-serif;
            padding-top: 70px; /* Espaço para a navbar fixa */
        }
        .navbar {
            background-color: #212529 !important; /* Cor da navbar consistente */
            box-shadow: 0 2px 4px var(--dark-shadow-color);
        }
        .navbar-brand, .navbar-nav .nav-link {
            color: var(--dark-text-color) !important;
        }
        .navbar-nav .nav-link.active {
             color: var(--highlight-yellow) !important;
        }
        .btn-outline-light {
            color: var(--dark-text-color);
            border-color: var(--dark-text-color);
        }
        .btn-outline-light:hover {
            background-color: var(--dark-text-color);
            color: var(--dark-bg);
        }

        .headline {
            text-align: center;
            font-size: 2.5rem; /* Ajustado para um pouco maior */
            font-weight: bold;
            margin-top: 3rem;
            margin-bottom: 3rem; /* Adicionado margem inferior */
        }
        .headline span {
            color: var(--highlight-yellow); /* Usa a variável para o amarelo */
        }

        .banner {
            display: flex;
            flex-wrap: wrap;
            background: linear-gradient(to right, var(--light-banner-bg-start), var(--light-banner-bg-end));
            border-radius: 12px;
            box-shadow: 0 4px 20px var(--dark-shadow-color);
            margin: 2rem auto;
            max-width: 1200px;
            padding: 2rem;
            color: var(--light-banner-text); /* Texto do banner em preto */
            align-items: center; /* Alinha verticalmente no centro */
        }
        .banner-text {
            flex: 1 1 400px;
            padding: 1rem;
        }
        .banner-image {
            flex: 1 1 400px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1rem;
        }
        .banner-image img {
            max-width: 100%;
            border-radius: 10px;
        }

        .carousel img {
            height: 400px;
            object-fit: cover;
            border-radius: 12px; /* Adiciona borda arredondada ao carrossel */
        }

        .plans-section { /* Renomeado de .planos para evitar conflito e clareza */
            background-color: var(--dark-card-bg); /* Fundo escuro para a seção de planos */
            color: var(--dark-text-color);
            padding: 2rem;
            border-radius: 20px;
            margin: 3rem auto;
            max-width: 1200px;
            box-shadow: 0 0 15px var(--dark-shadow-color);
        }
        .plans-section h2 { /* Título da seção de planos */
            color: white; /* Cor do título principal da seção de planos */
            margin-bottom: 2rem;
            text-align: center;
        }

        .plan-card { /* Renomeado de .plano para .plan-card para clareza */
            background-color: #3b3b3b; /* Fundo dos cards de plano */
            color: var(--dark-text-color);
            border-radius: 15px;
            padding: 25px;
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between; /* Empurra o botão para baixo */
            min-width: 280px; /* Garante que não fiquem muito estreitos */
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            border: 1px solid var(--dark-border-color); /* Borda sutil */
        }
        .plan-card h3 {
            color: white;
            margin-bottom: 1rem;
        }
        .plan-card p {
            margin-bottom: 1rem;
        }
        .plan-card s {
            color: var(--dark-muted-text);
        }
        .plan-card strong {
            color: var(--highlight-yellow);
            font-size: 1.2rem;
        }

        .plan-card-highlight { /* Renomeado de .plano-destaque */
            background-color: #4f4f4f; /* Um pouco mais escuro para destaque */
            border-color: var(--highlight-yellow); /* Borda amarela */
            position: relative;
            box-shadow: 0 0 20px rgba(255,193,7,0.4); /* Sombra mais forte */
        }
        .plan-card-highlight::before {
            content: "💡 O mais vantajoso";
            position: absolute;
            top: -15px; /* Ajustado um pouco para cima */
            left: 50%; /* Centraliza */
            transform: translateX(-50%); /* Centraliza */
            background-color: var(--highlight-yellow);
            color: #212529; /* Texto escuro no badge */
            padding: 5px 15px; /* Ajustado padding */
            border-radius: 20px; /* Mais arredondado */
            font-weight: bold;
            font-size: 0.9rem;
            white-space: nowrap; /* Evita quebra de linha */
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }
        .plan-card button {
            background-color: var(--highlight-yellow);
            color: #212529; /* Texto preto no botão */
            padding: 12px 25px; /* Ajustado padding */
            border: none;
            border-radius: 8px; /* Menos arredondado */
            font-weight: bold;
            margin-top: auto; /* Empurra o botão para o final do card */
            transition: background-color 0.3s ease;
            width: 100%;
        }
        .plan-card button:hover {
            background-color: #e6b000;
        }
        .plan-card ul {
            margin-top: 15px;
            padding-left: 0; /* Remove padding padrão da lista */
            list-style: none; /* Remove bullet points */
        }
        .plan-card ul li {
            margin-bottom: 8px;
            font-size: 0.95rem;
            display: flex;
            align-items: center;
            color: var(--dark-text-color);
        }
        .plan-card ul li i { /* Para os ícones de check/x */
            margin-right: 8px;
            font-size: 1.1rem;
        }
        /* Cores dos checks e X's */
        .plan-card ul li .bi-check-circle-fill {
            color: var(--highlight-green);
        }
        .plan-card ul li .bi-x-circle-fill {
            color: var(--highlight-red);
        }
        .plan-card ul li.disabled-feature { /* Para os itens desabilitados no plano gratuito */
            color: var(--dark-muted-text);
            text-decoration: line-through;
        }
        .plan-card ul li.disabled-feature .bi-x-circle-fill {
            color: var(--highlight-red); /* Garante que o X continue vermelho */
        }
        .plan-card .price-info { /* Classe para o preço principal */
            margin-top: 1rem;
        }
    </style>
</head>
<body>

    <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
        <div class="container-fluid">
            <a class="navbar-brand" href="inicial.html">
                <img src="img/login.png" height="50px" alt="Body Health Logo"> Body Health
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="inicial.html">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="6.Suporte.html">Suporte</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="4.Planos.html">Planos</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="5.SobreNos.html">Sobre Nós</a>
                    </li>
                    <li class="nav-item ms-lg-3"> <a href="2.Login.html" class="btn btn-outline-light">Login</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-5">
        <div id="carouselExampleAutoplaying" class="carousel slide" data-bs-ride="carousel">
            <div class="carousel-inner">
                <div class="carousel-item active">
                    <img src="img/qiZtFsNEjacT.png" class="d-block w-100" alt="Imagem 1">
                </div>
                <div class="carousel-item">
                    <img src="img/wgGO3n56mJld.png" class="d-block w-100" alt="Imagem 2">
                </div>
                <div class="carousel-item">
                    <img src="img/RfMh6PMcZtcv.png" class="d-block w-100" alt="Imagem 3">
                </div>
            </div>
            <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="prev">
                <span class="carousel-control-prev-icon"></span>
                <span class="visually-hidden">Anterior</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="next">
                <span class="carousel-control-next-icon"></span>
                <span class="visually-hidden">Próximo</span>
            </button>
        </div>
    </div>

    <div class="headline">O Corpo dos seus sonhos em <span>suas mãos</span></div>

    <section class="banner">
        <div class="banner-text">
            <h4 class="mt-4">Body Health: Seu parceiro na jornada fitness!</h4>
            <ul>
                <li><i class="bi bi-play-circle-fill"></i> Vídeos demonstrativos para cada exercício</li>
                <li><i class="bi bi-graph-up"></i> Acompanhe sua evolução e cargas em tempo real</li>
                <li><i class="bi bi-clipboard-check"></i> Tenha acesso a dezenas de treinos, mesmo sem assinatura</li>
                <li><i class="bi bi-arrow-repeat"></i> Contrate planos ou faça upgrade com facilidade</li>
                <li><i class="bi bi-globe"></i> Tudo isso online, no seu tempo – e com opções gratuitas!</li>
            </ul>
            <p class="fw-bold mt-3">Tudo isso de graça!</p>
            <a href="#"><img src="https://upload.wikimedia.org/wikipedia/commons/7/78/Google_Play_Store_badge_EN.svg" alt="Google Play" height="40"></a>
            </div>
        <div class="banner-image">
            <img src="img/smart_fit_app-BR.png" alt="App Body Health">
        </div>
    </section>

    <div class="plans-section">
        <h2 class="text-center">Escolha o plano ideal para você</h2>
        <div class="d-flex flex-wrap justify-content-center gap-4 mt-4">
            <div class="plan-card plan-card-highlight">
                <div>
                    <h3>Plano Anual</h3>
                    <p class="price-info"><s>R$ 239,88</s><br><strong>por R$179,90 / ano</strong></p>
                </div>
                <ul>
                    <li><i class="bi bi-check-circle-fill"></i> Criar Conta</li>
                    <li><i class="bi bi-check-circle-fill"></i> Calcular IMC</li>
                    <li><i class="bi bi-check-circle-fill"></i> Planilha de Treino Básica</li>
                    <li><i class="bi bi-check-circle-fill"></i> Salvar Dados</li>
                    <li><i class="bi bi-check-circle-fill"></i> Ler Artigos</li>
                    <li><i class="bi bi-x-circle-fill"></i> Sem Anúncios</li> <li><i class="bi bi-check-circle-fill"></i> Treinos Personalizados Ilimitados</li>
                    <li><i class="bi bi-check-circle-fill"></i> Acompanhamento Nutricional</li>
                    <li><i class="bi bi-check-circle-fill"></i> Avaliar Profissionais</li>
                    <li><i class="bi bi-check-circle-fill"></i> Salvar Medidas e Peso</li>
                </ul>
                <a href="4.Planos.html" class="d-block mt-3 text-center text-decoration-none">
                    <button>Assinar Agora</button>
                </a>
            </div>

            <div class="plan-card">
                <div>
                    <h3>Plano Mensal</h3>
                    <p class="price-info"><strong>A partir de R$ 19,90/mês</strong></p>
                </div>
                <ul>
                    <li><i class="bi bi-check-circle-fill"></i> Criar Conta</li>
                    <li><i class="bi bi-check-circle-fill"></i> Calcular IMC</li>
                    <li><i class="bi bi-check-circle-fill"></i> Planilha de Treino Básica</li>
                    <li><i class="bi bi-check-circle-fill"></i> Salvar Dados</li>
                    <li><i class="bi bi-check-circle-fill"></i> Ler Artigos</li>
                    <li><i class="bi bi-x-circle-fill"></i> Sem Anúncios</li> <li><i class="bi bi-check-circle-fill"></i> Treinos Personalizados Limitados</li>
                    <li><i class="bi bi-check-circle-fill"></i> Acompanhamento Nutricional Básico</li>
                    <li><i class="bi bi-check-circle-fill"></i> Avaliar Profissionais</li>
                    <li><i class="bi bi-check-circle-fill"></i> Salvar Medidas e Peso</li>
                </ul>
                <a href="4.Planos.html" class="d-block mt-3 text-center text-decoration-none">
                     <button>Assinar Agora</button>
                </a>
            </div>

            <div class="plan-card">
                <div>
                    <h3>Plano Gratuito</h3>
                    <p class="price-info"><strong>R$ 0,00</strong></p>
                </div>
                <ul>
                    <li><i class="bi bi-check-circle-fill"></i> Criar Conta</li>
                    <li><i class="bi bi-check-circle-fill"></i> Calcular IMC</li>
                    <li><i class="bi bi-check-circle-fill"></i> Planilha de Treino Básica</li>
                    <li><i class="bi bi-check-circle-fill"></i> Salvar Dados Limitado</li>
                    <li><i class="bi bi-check-circle-fill"></i> Ler Artigos Selecionados</li>
                    <li class="disabled-feature"><i class="bi bi-x-circle-fill"></i> Com Anúncios</li> <li class="disabled-feature"><i class="bi bi-x-circle-fill"></i> Treinos Personalizados</li>
                    <li class="disabled-feature"><i class="bi bi-x-circle-fill"></i> Acompanhamento Nutricional</li>
                    <li class="disabled-feature"><i class="bi bi-x-circle-fill"></i> Avaliar Profissionais</li>
                    <li class="disabled-feature"><i class="bi bi-x-circle-fill"></i> Salvar Medidas e Peso</li>
                </ul>
                <a href="4.Planos.html" class="d-block mt-3 text-center text-decoration-none">
                    <button>Começar Agora</button>
                </a>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

# templates\2.Login.html

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Login - Body Health</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    /* VARIAVEIS */
    :root {
        --dark-shadow-color: rgba(0, 0, 0, 0.5);
    }

    body {
      margin: 0;
      padding: 0;
      background-image: url("sua-imagem.jpg"); /* Substitua pelo caminho correto da sua imagem de fundo */
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
      font-family: Arial, sans-serif;
      background-color: #000; /* Cor de fallback caso a imagem não carregue */
      color: white; /* Cor do texto padrão para o body */
    }

    .navbar {
      background-color: #212529 !important; /* Cor da navbar consistente */
      box-shadow: 0 2px 4px var(--dark-shadow-color); /* Usando a variável */
    }

    .navbar-nav .nav-link {
      color: white !important;
      margin-left: 20px;
      font-weight: 500;
    }

    .login-box {
      /* Ajustes de largura e posicionamento */
      max-width: 600px; /* Aumentado para consistência com o cadastro */
      margin: 100px auto; /* Centraliza vertical e horizontalmente */
      background-color: rgba(255, 255, 255, 0.1); /* Fundo branco transparente */
      backdrop-filter: blur(10px); /* Efeito de blur no fundo */
      padding: 30px;
      border-radius: 12px; /* Raio da borda consistente */
      color: white;
      text-align: center; /* Centraliza o título e o botão */
    }

    .login-box h4 {
      color: white; /* Título branco */
      margin-bottom: 25px;
    }

    .form-control {
      background-color: rgba(255, 255, 255, 0.05); /* Fundo branco bem transparente para os campos */
      color: white;
      border: 1px solid #ccc; /* Borda cinza clara */
      padding: 10px 15px; /* Padding padrão para inputs */
      height: auto; /* Garante que a altura seja flexível */
    }

    .form-control::placeholder {
      color: rgba(255, 255, 255, 0.5); /* Placeholder mais claro */
    }

    .form-label {
        color: white; /* Garante que os labels sejam brancos */
        text-align: left; /* Alinha labels à esquerda */
        display: block; /* Garante que labels ocupem a largura total para espaçamento */
        margin-bottom: 5px;
    }

    /* ESTILO DO BOTÃO DE LOGIN - AJUSTADO PARA O MESMO TAMANHO DOS INPUTS */
    .btn-login-custom { /* Nova classe para o botão de login */
      background-color: #ffc107; /* Cor de fundo amarela */
      color: #000; /* Cor do texto preta */
      border: none;
      width: 100%; /* Ocupa 100% da largura do pai */
      padding: 10px 15px; /* Mesma altura e padding dos inputs para alinhar */
      border-radius: 5px;
      font-size: 1rem; /* Tamanho da fonte padrão para combinar com os inputs */
      font-weight: bold;
      margin-top: 20px; /* Espaçamento superior */
      display: block; /* Garante que o botão seja um bloco para ocupar 100% */
      line-height: 1.5; /* Ajuste para o texto dentro do botão */
    }

    .btn-login-custom:hover {
      background-color: #e0a800; /* Um pouco mais escuro no hover */
      color: #000;
    }

    /* ESTILO DOS LINKS DENTRO DO CARD DE LOGIN */
    .login-box a {
      color: white; /* Links brancos */
      text-decoration: none;
    }

    .login-box a:hover {
      text-decoration: underline;
    }

    .logo {
      height: 40px;
    }

    /* Se você tiver um ícone de WhatsApp, mantenha aqui */
    .whatsapp-icon {
      position: fixed;
      bottom: 20px;
      right: 20px;
      font-size: 28px;
      color: #25D366;
      background-color: white;
      border-radius: 50%;
      padding: 10px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
    }
  </style>
</head>
<body>

  <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
    <div class="container-fluid">
      <a class="navbar-brand" href="inicial.html">
        <img src="img/login.png" height="50px" alt="Body Health Logo"> Body Health
      </a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="1.DashboardInicial.html">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="6.Suporte.html">Suporte</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="4.Planos.html">Planos</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="5.SobreNos.html">Sobre Nós</a>
        </ul>
      </div>
    </div>
  </nav>

  <div class="login-box">
    <h4 class="text-center mb-4">Entrar</h4>
    <form>
      <div class="mb-3">
        <label for="email" class="form-label">E-mail</label>
        <input type="email" class="form-control" id="email" placeholder="Digite seu e-mail">
      </div>
      <div class="mb-3">
        <label for="senha" class="form-label">Senha</label>
        <input type="password" class="form-control" id="senha" placeholder="Digite sua senha">
      </div>
      <button type="submit" class="btn-login-custom mt-4">Entrar</button>
    </form>
    <p class="text-center mt-4">Não tem uma conta? <a href="3.Cadastro.html">Cadastre-se</a></p>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

# templates\3.Cadastro.html

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Cadastro - Body Health</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    /* VARIAVEIS */
    :root {
        --dark-shadow-color: rgba(0, 0, 0, 0.5);
    }

    body {
      margin: 0;
      padding: 0;
      background-image: url("sua-imagem.jpg"); /* Substitua pelo caminho correto da sua imagem de fundo */
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
      font-family: Arial, sans-serif;
      background-color: #000;
      color: white;
    }

    .navbar {
      background-color: #212529 !important;
      box-shadow: 0 2px 4px var(--dark-shadow-color);
    }

    .navbar-nav .nav-link {
      color: white !important;
      margin-left: 20px;
      font-weight: 500;
    }

    .register-card {
      max-width: 600px; /* Largura do card de cadastro */
      margin: 100px auto;
      background-color: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(10px);
      padding: 30px;
      border-radius: 12px;
      color: white;
      text-align: center;
    }

    .register-card h2 {
      color: white;
      margin-bottom: 25px;
    }

    .form-control, .form-select {
      background-color: rgba(255, 255, 255, 0.05);
      color: white;
      border: 1px solid #ccc;
      padding: 10px 15px; /* Padding padrão para inputs */
      height: auto; /* Garante que a altura seja flexível */
    }

    .form-control::placeholder {
      color: rgba(255, 255, 255, 0.5);
    }

    .form-label {
        color: white;
        text-align: left;
        display: block;
        margin-bottom: 5px;
    }

    /* ESTILO DO BOTÃO CADASTRAR - AJUSTADO PARA O MESMO TAMANHO DOS INPUTS */
    .btn-register-custom { /* Nova classe para o botão */
      background-color: #ffc107; /* Cor de fundo amarela */
      color: #000; /* Cor do texto preta */
      border: none;
      width: 100%; /* Ocupa 100% da largura do pai */
      padding: 10px 15px; /* Mesma altura e padding dos inputs para alinhar */
      border-radius: 5px;
      font-size: 1rem; /* Tamanho da fonte padrão para combinar com os inputs */
      font-weight: bold;
      margin-top: 20px;
      display: block; /* Garante que o botão seja um bloco para ocupar 100% */
      line-height: 1.5; /* Ajuste para o texto dentro do botão */
    }

    .btn-register-custom:hover {
      background-color: #e0a800; /* Um pouco mais escuro no hover */
      color: #000;
    }


    /* ESTILO DOS LINKS DENTRO DO CARD */
    .register-card a {
      color: white;
      text-decoration: none;
    }

    .register-card a:hover {
      text-decoration: underline;
    }

    .logo {
      height: 40px;
    }

    .whatsapp-icon {
      position: fixed;
      bottom: 20px;
      right: 20px;
      font-size: 28px;
      color: #25D366;
      background-color: white;
      border-radius: 50%;
      padding: 10px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
    }
  </style>
</head>
<body>

  <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
    <div class="container-fluid">
      <a class="navbar-brand" href="inicial.html">
        <img src="img/login.png" height="50px" alt="Body Health Logo"> Body Health
      </a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item"><a class="nav-link active" href="1.DashboardInicial.html">Home</a></li>
          <li class="nav-item"><a class="nav-link" href="6.Suporte.html">Suporte</a></li>
          <li class="nav-item"><a class="nav-link" href="4.Planos.html">Planos</a></li>
          <li class="nav-item"><a class="nav-link" href="5.SobreNos.html">Sobre Nós</a></li>
        </ul>
      </div>
    </div>
  </nav>

  <div class="register-card">
    <h2>Criar sua Conta</h2>
    <form id="cadastroForm">
      <div class="mb-4">
        <label for="tipoConta" class="form-label">Você é:</label>
        <select class="form-select" id="tipoConta" required>
          <option value="" selected disabled>Selecione o tipo de conta</option>
          <option class="text-black" value="cliente">Cliente</option>
          <option class="text-black" value="profissional">Profissional (Personal Trainer ou Nutricionista)</option>
        </select>
      </div>

      <div class="mb-3">
        <label for="email" class="form-label">E-mail</label>
        <input type="email" class="form-control" id="email" name="email" placeholder="Digite seu e-mail" required>
      </div>

      <div class="mb-3">
        <label for="senha" class="form-label">Senha</label>
        <input type="password" class="form-control" id="senha" name="senha" placeholder="Digite sua senha" required>
      </div>

      <div class="mb-3">
        <label for="confirmarSenha" class="form-label">Confirmar Senha</label>
        <input type="password" class="form-control" id="confirmarSenha" name="confirmarSenha" placeholder="Confirme sua senha" required>
      </div>

      <div id="camposCliente" style="display: none;">
        <div class="mb-3">
          <label for="nomeCliente" class="form-label">Nome Completo</label>
          <input type="text" class="form-control" id="nomeCliente" name="nomeCliente" placeholder="Seu nome completo">
        </div>
        <div class="mb-3">
          <label for="cpfCliente" class="form-label">CPF</label>
          <input type="text" class="form-control" id="cpfCliente" name="cpfCliente" placeholder="000.000.000-00">
        </div>
      </div>

      <div id="camposProfissional" style="display: none;">
        <div class="mb-3">
          <label for="nomeProfissional" class="form-label">Nome Completo</label>
          <input type="text" class="form-control" id="nomeProfissional" name="nomeProfissional" placeholder="Seu nome completo">
        </div>
        <div class="mb-3">
          <label for="cpfProfissional" class="form-label">CPF</label>
          <input type="text" class="form-control" id="cpfProfissional" name="cpfProfissional" placeholder="000.000.000-00">
        </div>
        <div class="mb-3">
          <label for="dataNascimentoProfissional" class="form-label">Data de Nascimento</label>
          <input type="date" class="form-control" id="dataNascimentoProfissional" name="dataNascimentoProfissional">
        </div>
        <div class="mb-3">
          <label for="tipoProfissionalSelect" class="form-label">Tipo de Profissional</label>
          <select class="form-select" id="tipoProfissionalSelect" name="tipoProfissional">
            <option value="" selected disabled>Selecione (Personal ou Nutricionista)</option>
            <option value="personal_trainer">Personal Trainer</option>
            <option value="nutricionista">Nutricionista</option>
          </select>
        </div>
        <div class="mb-3">
          <label for="numeroRegistro" class="form-label">Número de Registro (CREF/CRN)</label>
          <input type="text" class="form-control" id="numeroRegistro" name="numeroRegistro" placeholder="Ex: CREF 000000-G/RJ ou CRN 00000">
          <div class="form-text text-muted">Seu registro será verificado para aprovação da conta.</div>
        </div>
        <div class="mb-3">
          <label for="diplomaFoto" class="form-label">Foto do Diploma / Certificado</label>
          <input class="form-control" type="file" id="diplomaFoto" name="diplomaFoto" accept="image/*">
          <div class="form-text text-muted">Envie uma foto clara do seu diploma para validação.</div>
        </div>
      </div>

      <div class="mb-3 form-check" style="text-align: left;">
        <input type="checkbox" class="form-check-input" id="termos" required>
        <label class="form-check-label" for="termos">
          Concordo com os <a href="#">Termos de Serviço</a> e a <a href="#">Política de Privacidade</a>.
        </label>
      </div>

      <button type="submit" class="btn-register-custom mt-3">Cadastrar</button>
    </form>
    <p class="text-center mt-4">Já tem uma conta? <a href="2.Login.html">Faça Login</a></p>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

  <script>
    document.getElementById("tipoConta").addEventListener("change", function () {
      const tipo = this.value;
      document.getElementById("camposCliente").style.display = tipo === "cliente" ? "block" : "none";
      document.getElementById("camposProfissional").style.display = tipo === "profissional" ? "block" : "none";
    });

    // Esconde os campos inicialmente
    document.getElementById("camposCliente").style.display = "none";
    document.getElementById("camposProfissional").style.display = "none";
  </script>
</body>
</html>
```

# templates\4.Planos.html

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Planos - Body Health</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        :root {
            /* Cores para o tema escuro */
            --dark-bg: #1a1a1a;
            --dark-card-bg: #2b2b2b;
            --dark-text-color: #e0e0e0;
            --dark-muted-text: #b0b0b0;
            --dark-border-color: #444444;
            --dark-shadow-color: rgba(0,0,0,0.5);
            --highlight-yellow: #ffc107;
            --highlight-green: #28a745;
            --highlight-red: #dc3545;
        }

        body {
            background-color: var(--dark-bg);
            color: var(--dark-text-color);
            padding-top: 70px;
        }
        .navbar {
            background-color: #212529 !important;
            box-shadow: 0 2px 4px var(--dark-shadow-color);
        }
        .navbar-brand, .navbar-nav .nav-link {
            color: var(--dark-text-color) !important;
        }
        .navbar-nav .nav-link.active {
            color: var(--highlight-yellow) !important;
        }

        h1, h3, h5 {
            color: var(--dark-text-color);
        }
        .text-primary {
            color: white !important;
        }

        /* Estilos para as abas */
        .plan-tabs {
            display: flex;
            justify-content: center;
            margin-bottom: 30px;
            gap: 10px;
        }
        /* Esconde os radio buttons */
        .plan-tab-control {
            display: none;
        }
        /* Estilo das labels que atuam como abas */
        .plan-tab-label {
            border: 1px solid var(--dark-border-color);
            border-radius: 0.25rem;
            padding: 12px 35px;
            font-weight: bold;
            background-color: var(--dark-card-bg);
            color: var(--dark-text-color);
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
            user-select: none;
        }
        .plan-tab-label:hover {
            background-color: #3b3b3b;
            color: #ffffff;
        }
        /* Estilo da aba ativa quando o rádio correspondente está checado */
        .plan-tab-control:checked + .plan-tab-label {
            background-color: var(--highlight-yellow);
            color: #212529;
            border-color: var(--highlight-yellow);
            box-shadow: 0 0 10px rgba(255,193,7,0.3);
        }

        /* Conteúdo das abas - inicialmente todos escondidos */
        .tab-content-section {
            display: none;
            width: 100%;
        }

        .features i {
            font-size: 1.1rem;
            margin-right: 10px;
            color: var(--highlight-green);
        }
        .features .col-12, .features .col-md-6 {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        .text-danger {
            color: var(--highlight-red) !important;
        }

        .sidebar, .plan-details-card {
            background-color: var(--dark-card-bg);
            border-radius: 8px;
            padding: 25px;
            box-shadow: 0 0 15px var(--dark-shadow-color);
            margin-bottom: 20px;
        }
        .plan-details-card h3 {
            color: white;
        }
        .plan-details-card p {
            color: var(--dark-text-color);
            font-size: 1.05rem;
            line-height: 1.6;
        }
        .form-check-label {
            color: var(--dark-text-color);
        }
        .form-check-label strong {
            color: #ffffff;
        }
        .text-success {
            color: var(--highlight-green) !important;
        }
        .badge.bg-success {
            background-color: var(--highlight-green) !important;
        }

        .price-display {
            font-size: 2.2rem;
            font-weight: bold;
            color: white;
            margin-top: 15px;
            margin-bottom: 20px;
            text-align: center;
        }
        .btn-primary {
            background-color: #007bff;
            border-color: #007bff;
            color: #ffffff;
        }
        .btn-primary:hover {
            background-color: #0056b3;
            border-color: #0056b3;
        }
        .text-muted {
            color: var(--dark-muted-text) !important;
        }
        .text-decoration-none {
            color: white !important;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
        <div class="container-fluid">
            <a class="navbar-brand" href="inicial.html" > <img src="img/login.png" alt="" height="50px">Body Health</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link text-white" href="1.DashboardInicial.html">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link text-white" href="6.Suporte.html">Suporte</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link text-white active" aria-current="page" href="4.Planos.html">Planos</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link text-white" href="5.SobreNos.html">Sobre Nós</a>
                    </li>
                    <li>
                        <li class="nav-item ms-lg-3"> <a href="2.Login.html" class="btn btn-outline-light">Login</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-5">
        <h1 class="text-center mb-5 fw-bold text-primary">Escolha o plano ideal para você</h1>

        <div class="plan-tabs" role="tablist">
            <input type="radio" name="plan-tab-control" id="premium-tab" checked class="plan-tab-control">
            <label for="premium-tab" class="plan-tab-label" onclick="showTab('premium-content-section')">Plano Premium</label>

            <input type="radio" name="plan-tab-control" id="free-tab" class="plan-tab-control">
            <label for="free-tab" class="plan-tab-label" onclick="showTab('free-content-section')">Plano Gratuito</label>
        </div>

        <div class="tab-content-wrapper">

            <div id="premium-content-section" class="tab-content-section row">
                <div class="col-md-7">
                    <div class="plan-details-card">
                        <h3 class="fw-bold">Leve sua saúde ao próximo nível com o Plano Premium!</h3>
                        <p>Desbloqueie todo o potencial da Body Health com acesso ilimitado a recursos exclusivos e personalizados, criados para otimizar seus resultados e te manter motivado.</p>
                        <div class="row features mt-4">
                            <div class="col-12 col-md-6"><i class="bi bi-check-circle-fill"></i> Treinos personalizados e ilimitados</div>
                            <div class="col-12 col-md-6"><i class="bi bi-check-circle-fill"></i> Acompanhamento nutricional completo</div>
                            <div class="col-12 col-md-6"><i class="bi bi-check-circle-fill"></i> Análise de progresso avançada</div>
                            <div class="col-12 col-md-6"><i class="bi bi-check-circle-fill"></i> Suporte prioritário 24/7</div>
                            <div class="col-12 col-md-6"><i class="bi bi-check-circle-fill"></i> Biblioteca premium de artigos e receitas</div>
                            <div class="col-12 col-md-6"><i class="bi bi-check-circle-fill"></i> Sem anúncios, foco total no seu bem-estar</div>
                            <div class="col-12 col-md-6"><i class="bi bi-check-circle-fill"></i> Desafios e comunidades exclusivas</div>
                            <div class="col-12 col-md-6"><i class="bi bi-check-circle-fill"></i> Integração com dispositivos inteligentes</div>
                        </div>
                    </div>
                </div>

                <div class="col-md-5">
                    <div class="sidebar">
                        <h5>Assine o Plano Premium e transforme sua saúde!</h5>
                        <div class="form-check mt-4">
                            <input class="form-check-input" type="radio" name="assinatura" id="plano1" value="19.90" checked>
                            <label class="form-check-label" for="plano1">
                                <strong>Assinatura Mensal</strong><br>
                                Pague mês a mês. Cancele quando quiser.<br>
                                <strong class="text-success">R$19,90 / mês</strong>
                            </label>
                        </div>
                        <div class="form-check mt-3">
                            <input class="form-check-input" type="radio" name="assinatura" id="plano2" value="179.90">
                            <label class="form-check-label" for="plano2">
                                <strong>Assinatura Anual</strong><br>
                                Pague um ano e economize! (Economia de 25%)<br>
                                <strong class="text-success">R$179,90 / ano</strong> <span class="badge bg-success">Melhor Custo-Benefício!</span>
                            </label>
                        </div>
                        <div class="price-display">R$19,90</div>
                        <a href= 7.Pagamento.html><button class="btn btn-primary btn-lg w-100 mt-3">Assinar Agora</button></a>
                        <p class="mt-3 text-muted text-center" style="font-size: 0.85rem;">
                            Consulte os termos de uso para saber detalhes sobre alterações de preços e sobre como cancelar.
                        </p>
                    </div>
                </div>
            </div>

            <div id="free-content-section" class="tab-content-section row">
                <div class="col-md-7">
                    <div class="plan-details-card">
                        <h3 class="fw-bold">Comece sua jornada fitness com o Plano Gratuito!</h3>
                        <p>Ideal para quem está começando, a versão gratuita da Body Health oferece funcionalidades essenciais para você dar os primeiros passos em direção a uma vida mais saudável.</p>
                        <div class="row features mt-4">
                            <div class="col-12 col-md-6"><i class="bi bi-check-circle-fill"></i> Criar e gerenciar sua conta</div>
                            <div class="col-12 col-md-6"><i class="bi bi-check-circle-fill"></i> Calcular IMC e outras métricas básicas</div>
                            <div class="col-12 col-md-6"><i class="bi bi-check-circle-fill"></i> Acesso à planilha de treino básica</div>
                            <div class="col-12 col-md-6"><i class="bi bi-check-circle-fill"></i> Salvar dados de progresso limitado</div>
                            <div class="col-12 col-md-6"><i class="bi bi-check-circle-fill"></i> Leitura de artigos selecionados</div>
                            <div class="col-12 col-md-6 text-danger"><i class="bi bi-x-circle-fill"></i> Exibição de anúncios</div>
                        </div>
                    </div>
                </div>
                <div class="col-md-5">
                    <div class="sidebar">
                        <h5>Aproveite o Plano Gratuito!</h5>
                        <p class="text-center mt-4">Com o plano gratuito, você tem acesso às funcionalidades essenciais para começar sua jornada fitness.</p>
                        <div class="price-display">Grátis</div>
                        <a href="2.Login.html"><button class="btn btn-primary btn-lg w-100 mt-3">Assinar Agora</button></a>
                        <p class="mt-3 text-muted text-center" style="font-size: 0.85rem;">
                            Sem custos, sem compromisso. Explore e descubra o que a Body Health pode fazer por você.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Function to show the correct tab content on page load
            function initializeTabs() {
                const premiumTab = document.getElementById('premium-tab');
                const freeTab = document.getElementById('free-tab');

                if (premiumTab.checked) {
                    showTab('premium-content-section');
                } else if (freeTab.checked) {
                    showTab('free-content-section');
                }
            }

            // Function to handle tab content display
            window.showTab = function(tabId) {
                // Hide all tab content sections
                document.querySelectorAll('.tab-content-section').forEach(section => {
                    section.style.display = 'none';
                });

                // Show the selected tab content section
                document.getElementById(tabId).style.display = 'flex';
            };

            // Update price display based on radio button selection
            const subscriptionRadios = document.querySelectorAll('input[name="assinatura"]');
            const priceDisplay = document.querySelector('.price-display');

            subscriptionRadios.forEach(radio => {
                radio.addEventListener('change', function() {
                    if (this.checked) {
                        const price = this.value;
                        if (price === "19.90") {
                            priceDisplay.textContent = 'R$19,90';
                        } else if (price === "179.90") {
                            priceDisplay.textContent = 'R$179,90';
                        }
                    }
                });
            });

            // Initialize tabs when the DOM is fully loaded
            initializeTabs();
        });
    </script>
</body>
</html>
```

# templates\5.SobreNos.html

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sobre Nós - Body Health</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        :root {
            /* Cores para o tema escuro */
            --dark-bg: #1a1a1a; /* Fundo principal muito escuro */
            --dark-card-bg: #2b2b2b; /* Fundo dos cards e sidebar */
            --dark-text-color: #e0e0e0; /* Cor de texto padrão clara (quase branca) */
            --dark-muted-text: #b0b0b0; /* Texto muted mais claro */
            --dark-border-color: #444444; /* Bordas mais escuras */
            --dark-shadow-color: rgba(0,0,0,0.5); /* Sombra mais intensa */
            --highlight-yellow: #ffc107; /* Amarelo de destaque (pode ser ajustado) */
            --highlight-green: #28a745; /* Verde para checks */
            --highlight-red: #dc3545; /* Vermelho para X */
        }

        body {
            background-color: var(--dark-bg);
            color: var(--dark-text-color); /* Texto padrão claro */
            padding-top: 70px; /* Espaço para a navbar fixa */
        }
        .navbar {
            background-color: #212529 !important; /* Bootstrap bg-dark é escuro, mas vamos garantir */
            box-shadow: 0 2px 4px var(--dark-shadow-color);
        }
        .navbar-brand, .navbar-nav .nav-link {
            color: var(--dark-text-color) !important;
        }
        .navbar-nav .nav-link.active {
             color: var(--highlight-yellow) !important; /* Destaque para o link ativo */
        }

        h1, h2, h3, h5 {
            color: var(--dark-text-color); /* Títulos claros */
        }
        .text-primary { /* Para o título principal */
            color: white !important; /* Alterado para branco puro */
        }

        .about-card {
            background-color: var(--dark-card-bg);
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 0 15px var(--dark-shadow-color);
            margin-bottom: 30px;
        }
        .about-card p {
            font-size: 1.05rem;
            line-height: 1.7;
            margin-bottom: 20px;
        }
        .about-card ul {
            list-style: none;
            padding: 0;
        }
        .about-card ul li {
            margin-bottom: 10px;
            font-size: 1.0rem;
        }
        .about-card ul li i {
            margin-right: 10px;
            color: var(--highlight-yellow); /* Ícones de destaque */
        }
        .img-team {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin-top: 20px;
            box-shadow: 0 0 10px var(--dark-shadow-color);
        }
        .icon-large {
            font-size: 2.5rem;
            color: var(--highlight-yellow);
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
        <div class="container-fluid">
            <a class="navbar-brand" href="inicial.html"> <img src="img/login.png" alt="" height="50px">Body Health</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link text-white" href="1.DashboardInicial.html">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link text-white" href="6.Suporte.html">Suporte</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link text-white" href="4.Planos.html">Planos</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link text-white active" aria-current="page" href="5.SobreNos.html">Sobre Nós</a>

                    </li>
                    <li>
                        <li class="nav-item ms-lg-3"> <a href="2.Login.html" class="btn btn-outline-light">Login</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-5">
        <h1 class="text-center mb-5 fw-bold text-primary">Sobre a Body Health</h1>

        <div class="row justify-content-center">
            <div class="col-lg-10">
                <div class="about-card">
                    <h2 class="text-center mb-4">Nossa Missão</h2>
                    <p class="text-center">Na Body Health, nossa missão é capacitar indivíduos a alcançar seus objetivos de saúde e bem-estar através de ferramentas intuitivas, conhecimento especializado e uma comunidade de apoio. Acreditamos que todos merecem uma vida plena e saudável, e estamos aqui para guiá-lo a cada passo do caminho.</p>
                </div>
            </div>
        </div>

        <div class="row justify-content-center">
            <div class="col-md-6 col-lg-5 mb-4">
                <div class="about-card text-center h-100">
                    <i class="bi bi-heart-pulse icon-large"></i>
                    <h3 class="mb-3">Nossa Visão</h3>
                    <p>Ser a plataforma líder em saúde e fitness, reconhecida pela inovação, personalização e pelo impacto positivo na vida de milhões de pessoas em todo o mundo.</p>
                </div>
            </div>
            <div class="col-md-6 col-lg-5 mb-4">
                <div class="about-card text-center h-100">
                    <i class="bi bi-lightbulb icon-large"></i>
                    <h3 class="mb-3">Nossos Valores</h3>
                    <ul style="text-align: left; list-style: none; padding-left: 0;">
                        <li><i class="bi bi-check-circle-fill"></i> <span><strong>Inovação:</strong> Constantemente buscando as melhores soluções.</span></li>
                        <li><i class="bi bi-check-circle-fill"></i> <span><strong>Paixão:</strong> Amamos o que fazemos e acreditamos no poder da saúde.</span></li>
                        <li><i class="bi bi-check-circle-fill"></i> <span><strong>Integridade:</strong> Transparência e honestidade em todas as ações.</span></li>
                        <li><i class="bi bi-check-circle-fill"></i> <span><strong>Resultados:</strong> Focados em entregar valor real aos nossos usuários.</span></li>
                        <li><i class="bi bi-check-circle-fill"></i> <span><strong>Comunidade:</strong> Fortalecendo conexões e apoio mútuo.</span></li>
                    </ul>

                </div>
            </div>
        </div>

        <div class="row justify-content-center">
            <div class="col-lg-10">
                <div class="about-card">
                    <h2 class="text-center mb-4">O Que Fazemos</h2>
                    <p>A Body Health oferece uma gama completa de recursos para sua jornada fitness:</p>
                    <div class="row features mt-4">
                        <div class="col-12 col-md-6"><i class="bi bi-activity"></i> Planos de Treino Personalizados</div>
                        <div class="col-12 col-md-6"><i class="bi bi-book"></i> Guias Nutricionais e Receitas Saudáveis</div>
                        <div class="col-12 col-md-6"><i class="bi bi-graph-up"></i> Monitoramento de Progresso Detalhado</div>
                        <div class="col-12 col-md-6"><i class="bi bi-chat-dots"></i> Suporte Especializado e Comunidade Ativa</div>
                    </div>
                    <p class="mt-4">Seja você um iniciante ou um atleta experiente, a Body Health tem as ferramentas e o suporte que você precisa para superar seus limites e viver sua melhor versão.</p>
                </div>
            </div>
        </div>

        <div class="row justify-content-center">
            <div class="col-lg-10">
                <div class="about-card text-center">
                    <h2 class="mb-4">Nossa Equipe</h2>
                    <p>Somos um grupo dedicado de profissionais apaixonados por saúde e tecnologia, comprometidos em criar a melhor experiência para você.</p>
                    <p class="mt-3 text-muted">Juntos, construímos o futuro do bem-estar digital.</p>
                </div>
            </div>
        </div>

    </div>

    </body>
</html>
```

# templates\6.Suporte.html

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Suporte - Body Health</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        :root {
            /* Cores para o tema escuro */
            --dark-bg: #1a1a1a; /* Fundo principal muito escuro */
            --dark-card-bg: #2b2b2b; /* Fundo dos cards e formulários */
            --dark-text-color: #e0e0e0; /* Cor de texto padrão clara (quase branca) */
            --dark-muted-text: #b0b0b0; /* Texto muted mais claro */
            --dark-border-color: #444444; /* Bordas mais escuras */
            --dark-shadow-color: rgba(0,0,0,0.5); /* Sombra mais intensa */
            --highlight-yellow: #ffc107; /* Amarelo de destaque */
            --highlight-green: #28a745; /* Verde para checks */
        }

        body {
            background-color: var(--dark-bg);
            color: var(--dark-text-color);
            padding-top: 70px; /* Espaço para a navbar fixa */
        }
        .navbar {
            background-color: #212529 !important;
            box-shadow: 0 2px 4px var(--dark-shadow-color);
        }
        .navbar-brand, .navbar-nav .nav-link {
            color: var(--dark-text-color) !important;
        }
        .navbar-nav .nav-link.active {
             color: var(--highlight-yellow) !important;
        }

        h1, h2, h3, h5 {
            color: var(--dark-text-color);
        }
        .text-primary {
            color: white !important;
        }

        .support-card {
            background-color: var(--dark-card-bg);
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 0 15px var(--dark-shadow-color);
            margin-bottom: 30px;
        }
        .support-card p, .support-card ul li {
            font-size: 1.05rem;
            line-height: 1.7;
        }
        .support-card ul {
            list-style: none;
            padding: 0;
        }
        .support-card ul li {
            margin-bottom: 10px;
        }
        .support-card ul li i {
            margin-right: 10px;
            color: var(--highlight-yellow);
        }

        /* Estilo para o formulário de contato */
        .form-label {
            color: var(--dark-text-color);
            font-weight: bold;
        }
        .form-control, .form-control:focus {
            background-color: #3b3b3b;
            color: var(--dark-text-color);
            border: 1px solid var(--dark-border-color);
        }
        .form-control::placeholder {
            color: var(--dark-muted-text);
        }
        .form-control:focus {
            box-shadow: 0 0 0 0.25rem rgba(255,193,7,0.25); /* Sombra amarela no foco */
            border-color: var(--highlight-yellow);
        }
        .btn-primary {
            background-color: #007bff;
            border-color: #007bff;
            color: #ffffff;
        }
        .btn-primary:hover {
            background-color: #0056b3;
            border-color: #0056b3;
        }

        /* Estilo para a seção de FAQ (Acordeão básico sem JS) */
        .faq-item {
            margin-bottom: 15px;
            border: 1px solid var(--dark-border-color);
            border-radius: 8px;
            overflow: hidden; /* Garante que o overflow seja tratado */
        }
        .faq-question {
            background-color: var(--dark-card-bg);
            padding: 15px 20px;
            cursor: pointer;
            font-weight: bold;
            color: var(--dark-text-color);
            display: block; /* Para o ícone de seta funcionar com :before */
            position: relative;
            user-select: none;
        }
        .faq-question:hover {
            background-color: #3b3b3b;
        }
        .faq-answer {
            background-color: #323232; /* Um pouco mais claro que o card */
            padding: 0 20px;
            max-height: 0; /* Escondido por padrão */
            overflow: hidden;
            transition: max-height 0.4s ease-out, padding 0.4s ease-out; /* Animação suave */
            color: var(--dark-muted-text);
        }
        /* Para mostrar a resposta quando o checkbox invisível é marcado */
        .faq-checkbox {
            display: none; /* Esconde o checkbox */
        }
        .faq-checkbox:checked + .faq-question + .faq-answer {
            max-height: 200px; /* Altura máxima para mostrar o conteúdo (ajuste conforme necessário) */
            padding: 15px 20px;
        }
        /* Estilo para a seta indicadora */
        .faq-question::before {
            content: '\f282'; /* Código do ícone chevron-down do Bootstrap Icons */
            font-family: 'bootstrap-icons';
            float: right;
            transition: transform 0.3s ease;
        }
        .faq-checkbox:checked + .faq-question::before {
            content: '\f286'; /* Código do ícone chevron-up */
            transform: rotate(180deg);
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
        <div class="container-fluid">
            <a class="navbar-brand" href="inicial.html"><img src="img/login.png" alt="" height="50px"> Body Health</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link text-white" aria-current="page" href="1.DashboardInicial.html">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link text-white active" aria-current="page" href="6.Suporte.html">Suporte</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link text-white" href="4.Planos.html">Planos</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link text-white" href="5.SobreNos.html">Sobre Nós</a>
                    </li>
                    <li>
                        <li class="nav-item ms-lg-3"> <a href="2.Login.html" class="btn btn-outline-light">Login</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-5">
        <h1 class="text-center mb-5 fw-bold text-primary">Central de Ajuda e Suporte</h1>

        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="support-card text-center">
                    <h2 class="mb-4">Como Podemos Ajudar?</h2>
                    <p>Nossa equipe de suporte está pronta para auxiliá-lo. Escolha a melhor forma de entrar em contato conosco ou consulte nossa seção de Perguntas Frequentes.</p>

                    <div class="row mt-4">
                        <div class="col-md-6 mb-3">
                            <i class="bi bi-envelope-fill icon-large"></i>
                            <h5 class="mt-2">E-mail</h5>
                            <p><a href="mailto:suporte@bodyhealth.com" class="text-decoration-none text-white">suporte@bodyhealth.com</a></p>
                        </div>
                        <div class="col-md-6 mb-3">
                            <i class="bi bi-whatsapp icon-large"></i>
                            <h5 class="mt-2">WhatsApp</h5>
                            <p><a href="https://wa.me/5528992566961" class="text-decoration-none text-white" target="_blank">(28) 99256-6961</a></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="support-card">
                    <h2 class="text-center mb-4">Envie sua Mensagem</h2>
                    <form>
                        <div class="mb-3">
                            <label for="nome" class="form-label">Seu Nome</label>
                            <input type="text" class="form-control" id="nome" placeholder="Seu nome completo" required>
                        </div>
                        <div class="mb-3">
                            <label for="email" class="form-label">Seu E-mail</label>
                            <input type="email" class="form-control" id="email" placeholder="nome@exemplo.com" required>
                        </div>
                        <div class="mb-3">
                            <label for="assunto" class="form-label">Assunto</label>
                            <input type="text" class="form-control" id="assunto" placeholder="Dúvida sobre plano, problema técnico, etc." required>
                        </div>
                        <div class="mb-3">
                            <label for="mensagem" class="form-label">Sua Mensagem</label>
                            <textarea class="form-control" id="mensagem" rows="5" placeholder="Descreva sua questão ou problema" required></textarea>
                        </div>
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary btn-lg">Enviar Mensagem</button>
                        </div>
                    </form>
                    <p class="mt-3 text-muted text-center" style="font-size: 0.9rem;">
                        * Este formulário é apenas para demonstração. Não envia dados reais.
                    </p>
                </div>
            </div>
        </div>

        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="support-card">
                    <h2 class="text-center mb-4">Perguntas Frequentes (FAQ)</h2>

                    <div class="faq-item">
                        <input type="checkbox" id="faq1" class="faq-checkbox">
                        <label for="faq1" class="faq-question">Como faço para me cadastrar na Body Health?</label>
                        <div class="faq-answer">
                            <p>Você pode se cadastrar diretamente pelo nosso aplicativo ou site. Clique em "Registrar" e siga os passos para criar sua conta gratuita. Após o cadastro, você terá a opção de assinar um de nossos planos premium para ter acesso a recursos adicionais.</p>
                        </div>
                    </div>

                    <div class="faq-item">
                        <input type="checkbox" id="faq2" class="faq-checkbox">
                        <label for="faq2" class="faq-question">Quais são os benefícios do Plano Premium?</label>
                        <div class="faq-answer">
                            <p>O Plano Premium oferece treinos personalizados ilimitados, acompanhamento nutricional completo, análise de progresso avançada, suporte prioritário, biblioteca exclusiva de artigos e receitas, e muito mais. Ele é projetado para maximizar seus resultados e sua experiência.</p>
                        </div>
                    </div>

                    <div class="faq-item">
                        <input type="checkbox" id="faq3" class="faq-checkbox">
                        <label for="faq3" class="faq-question">Posso cancelar minha assinatura a qualquer momento?</label>
                        <div class="faq-answer">
                            <p>Sim, assinaturas mensais podem ser canceladas a qualquer momento diretamente nas configurações da sua conta. Assinaturas anuais são faturadas uma vez por ano, e a renovação automática pode ser desativada a qualquer momento.</p>
                        </div>
                    </div>

                    <div class="faq-item">
                        <input type="checkbox" id="faq4" class="faq-checkbox">
                        <label for="faq4" class="faq-question">A Body Health se integra com outros dispositivos?</label>
                        <div class="faq-answer">
                            <p>Sim, o Plano Premium permite a integração com os principais smartwatches e dispositivos de monitoramento de fitness para que você possa sincronizar seus dados de treino e saúde automaticamente.</p>
                        </div>
                    </div>

                </div>
            </div>
        </div>

    </div>

    </body>
</html>
```

# templates\7.Pagamento.html

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Finalizar Pagamento - Body Health</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        :root {
            /* Cores para o tema escuro */
            --dark-bg: #1a1a1a;
            --dark-card-bg: #2b2b2b;
            --dark-text-color: #e0e0e0;
            --dark-muted-text: #b0b0b0;
            --dark-border-color: #444444;
            --dark-shadow-color: rgba(0,0,0,0.5);
            --highlight-yellow: #ffc107;
            --highlight-green: #28a745;
            --highlight-red: #dc3545;
        }

        body {
            background-color: var(--dark-bg);
            color: var(--dark-text-color);
            padding-top: 70px;
        }
        .navbar {
            background-color: #212529 !important;
            box-shadow: 0 2px 4px var(--dark-shadow-color);
        }
        .navbar-brand, .navbar-nav .nav-link {
            color: var(--dark-text-color) !important;
        }
        .navbar-nav .nav-link.active {
            color: var(--highlight-yellow) !important;
        }

        h1, h3, h5, h4 {
            color: var(--dark-text-color);
        }
        .text-primary {
            color: white !important;
        }

        .card-custom {
            background-color: var(--dark-card-bg);
            border-radius: 8px;
            padding: 25px;
            box-shadow: 0 0 15px var(--dark-shadow-color);
            margin-bottom: 20px;
        }

        .form-label {
            color: var(--dark-text-color);
        }
        .form-control, .form-select {
            background-color: #3b3b3b;
            border: 1px solid var(--dark-border-color);
            color: var(--dark-text-color);
        }
        .form-control:focus, .form-select:focus {
            background-color: #4b4b4b;
            border-color: var(--highlight-yellow);
            box-shadow: 0 0 0 0.25rem rgba(255,193,7,0.25);
            color: var(--dark-text-color);
        }
        .form-control::placeholder {
            color: var(--dark-muted-text);
        }

        .btn-primary {
            background-color: #007bff;
            border-color: #007bff;
            color: #ffffff;
        }
        .btn-primary:hover {
            background-color: #0056b3;
            border-color: #0056b3;
        }
        .text-muted {
            color: var(--dark-muted-text) !important;
        }
        .list-group-item {
            background-color: transparent;
            border-color: var(--dark-border-color);
            color: var(--dark-text-color);
        }
        .list-group-item strong {
            color: white;
        }
        .text-success {
            color: var(--highlight-green) !important;
        }

        /* Estilos para abas de pagamento (Cartão/PIX) */
        .payment-tabs {
            display: flex;
            margin-bottom: 20px;
            border-bottom: 1px solid var(--dark-border-color);
        }
        .payment-tab-button {
            flex-grow: 1;
            padding: 10px 15px;
            cursor: pointer;
            text-align: center;
            color: var(--dark-muted-text);
            font-weight: bold;
            border: none;
            background: transparent;
            border-bottom: 3px solid transparent;
            transition: all 0.3s ease;
        }
        .payment-tab-button.active {
            color: var(--highlight-yellow);
            border-bottom: 3px solid var(--highlight-yellow);
        }
        .payment-tab-button:hover:not(.active) {
            color: var(--dark-text-color);
        }
        .payment-content {
            display: none;
        }
        .payment-content.active {
            display: block;
        }

        #pix-qr-code {
            width: 100%;
            max-width: 250px;
            height: auto;
            display: block;
            margin: 20px auto;
            border-radius: 8px;
        }
        #pix-copy-button {
            background-color: var(--highlight-green);
            border-color: var(--highlight-green);
        }
        #pix-copy-button:hover {
            background-color: #218838;
            border-color: #1e7e34;
        }
        .pix-code-container {
            position: relative;
        }
        .pix-code-container input {
            padding-right: 50px; /* Space for the copy button */
        }
        .pix-copy-btn-absolute {
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            color: var(--dark-muted-text);
            font-size: 1.2rem;
        }
        .pix-copy-btn-absolute:hover {
            color: var(--highlight-yellow);
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
        <div class="container-fluid">
            <a class="navbar-brand" href="inicial.html">
                <img src="img/login.png" height="50px" alt="Body Health Logo"> Body Health
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" aria-current="page" href="1.DashboardInicial.html">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="6.Suporte.html">Suporte</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="4.Planos.html">Planos</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="5.SobreNos.html">Sobre Nós</a>
                    </li>
                    <li class="nav-item ms-lg-3"> <a href="2.Login.html" class="btn btn-outline-light">Login</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-5">
        <h1 class="text-center mb-5 fw-bold text-primary">Finalizar Pagamento</h1>

        <div class="row g-4">
            <div class="col-md-7 order-md-1">
                <div class="card-custom">
                    <h4 class="mb-3">Escolha seu Plano</h4>
                    <div class="mb-4">
                        <div class="form-check">
                            <input class="form-check-input" type="radio" name="planType" id="planMensal" value="mensal" checked>
                            <label class="form-check-label" for="planMensal">
                                <strong>Plano Premium Mensal</strong> - R$19,90 / mês
                            </label>
                        </div>
                        <div class="form-check mt-2">
                            <input class="form-check-input" type="radio" name="planType" id="planAnual" value="anual">
                            <label class="form-check-label" for="planAnual">
                                <strong>Plano Premium Anual</strong> - R$179,90 / ano <span class="badge bg-success">Economize 25%!</span>
                            </label>
                        </div>
                    </div>

                    <h4 class="mb-3">Método de Pagamento</h4>
                    <div class="payment-tabs">
                        <button class="payment-tab-button active" data-tab-target="#credit-card-content">Cartão de Crédito</button>
                        <button class="payment-tab-button" data-tab-target="#pix-content">PIX</button>
                    </div>

                    <div id="credit-card-content" class="payment-content active">
                        <form class="needs-validation" novalidate id="card-payment-form">
                            <div class="mb-3">
                                <label for="nomeCartao" class="form-label">Nome no Cartão</label>
                                <input type="text" class="form-control" id="nomeCartao" placeholder="Nome Completo (como no cartão)" required>
                                <div class="invalid-feedback">
                                    O nome no cartão é obrigatório.
                                </div>
                            </div>

                            <div class="mb-3">
                                <label for="numeroCartao" class="form-label">Número do Cartão</label>
                                <input type="text" class="form-control" id="numeroCartao" placeholder="XXXX XXXX XXXX XXXX" required pattern="[0-9]{16}">
                                <div class="invalid-feedback">
                                    Um número de cartão válido é obrigatório (16 dígitos).
                                </div>
                            </div>

                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label for="validade" class="form-label">Validade (MM/AA)</label>
                                    <input type="text" class="form-control" id="validade" placeholder="MM/AA" required pattern="(0[1-9]|1[0-2])\/[0-9]{2}">
                                    <div class="invalid-feedback">
                                        A validade é obrigatória (MM/AA).
                                    </div>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label for="cvv" class="form-label">CVV</label>
                                    <input type="text" class="form-control" id="cvv" placeholder="XXX" required pattern="[0-9]{3,4}">
                                    <div class="invalid-feedback">
                                        O CVV é obrigatório (3 ou 4 dígitos).
                                    </div>
                                </div>
                            </div>

                            <hr class="my-4" style="border-color: var(--dark-border-color);">

                            <h4 class="mb-3">Endereço de Cobrança</h4>

                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label for="primeiroNome" class="form-label">Primeiro Nome</label>
                                    <input type="text" class="form-control" id="primeiroNome" placeholder="" value="" required>
                                    <div class="invalid-feedback">
                                        Seu primeiro nome é obrigatório.
                                    </div>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label for="sobrenome" class="form-label">Sobrenome</label>
                                    <input type="text" class="form-control" id="sobrenome" placeholder="" value="" required>
                                    <div class="invalid-feedback">
                                        Seu sobrenome é obrigatório.
                                    </div>
                                </div>
                            </div>

                            <div class="mb-3">
                                <label for="endereco" class="form-label">Endereço</label>
                                <input type="text" class="form-control" id="endereco" placeholder="Rua, número" required>
                                <div class="invalid-feedback">
                                    Por favor, insira seu endereço de cobrança.
                                </div>
                            </div>

                            <div class="mb-3">
                                <label for="endereco2" class="form-label">Endereço 2 <span class="text-muted">(Opcional)</span></label>
                                <input type="text" class="form-control" id="endereco2" placeholder="Apartamento, condomínio, etc.">
                            </div>

                            <div class="row">
                                <div class="col-md-5 mb-3">
                                    <label for="pais" class="form-label">País</label>
                                    <select class="form-select" id="pais" required>
                                        <option value="">Escolha...</option>
                                        <option>Brasil</option>
                                        <option>Estados Unidos</option>
                                        <option>Canadá</option>
                                        </select>
                                    <div class="invalid-feedback">
                                        Por favor, selecione um país válido.
                                    </div>
                                </div>
                                <div class="col-md-4 mb-3">
                                    <label for="estado" class="form-label">Estado</label>
                                    <select class="form-select" id="estado" required>
                                        <option value="">Escolha...</option>
                                        <option>SP</option>
                                        <option>RJ</option>
                                        <option>MG</option>
                                        </select>
                                    <div class="invalid-feedback">
                                        Por favor, forneça um estado válido.
                                    </div>
                                </div>
                                <div class="col-md-3 mb-3">
                                    <label for="cep" class="form-label">CEP</label>
                                    <input type="text" class="form-control" id="cep" placeholder="00000-000" required pattern="[0-9]{5}-[0-9]{3}">
                                    <div class="invalid-feedback">
                                        CEP é obrigatório.
                                    </div>
                                </div>
                            </div>

                            <hr class="my-4" style="border-color: var(--dark-border-color);">

                            <button class="w-100 btn btn-primary btn-lg" type="submit">Pagar com Cartão</button>
                        </form>
                    </div>

                    <div id="pix-content" class="payment-content">
                        <p class="text-center lead">Escaneie o QR Code ou copie o código PIX para finalizar o pagamento.</p>
                        <img src="https://via.placeholder.com/250?text=QR+Code+PIX" alt="QR Code PIX" id="pix-qr-code">
                        <div class="mb-3 pix-code-container">
                            <label for="pix-code" class="form-label">Código PIX Copia e Cola</label>
                            <input type="text" class="form-control" id="pix-code" value="00020126580014BR.GOV.BCB.PIX0136a53266e-2ba4-41d4-8395-502842e22c06520400005303986540519.905802BR5913Nome Empresa6008BRASILIA62070503***6304CA27" readonly>
                            <button class="pix-copy-btn-absolute" onclick="copyPixCode()"><i class="bi bi-clipboard"></i></button>
                            <div class="form-text text-muted">Este QR Code e código são apenas para demonstração.</div>
                        </div>
                        <button class="w-100 btn btn-success btn-lg mt-3" type="button" id="confirm-pix-payment">Já Paguei com PIX</button>
                    </div>

                </div>
            </div>

            <div class="col-md-5 order-md-2">
                <div class="card-custom">
                    <h4 class="d-flex justify-content-between align-items-center mb-3">
                        <span class="text-primary">Resumo do Pedido</span>
                    </h4>
                    <ul class="list-group mb-3">
                        <li class="list-group-item d-flex justify-content-between lh-sm">
                            <div>
                                <h6 class="my-0">Plano <span id="plano-nome">Premium Mensal</span></h6>
                                <small class="text-muted">Acesso ilimitado à Body Health</small>
                            </div>
                            <span class="text-success" id="plano-preco">R$19,90</span>
                        </li>
                        <li class="list-group-item d-flex justify-content-between">
                            <span>Total (BRL)</span>
                            <strong id="total-preco">R$19,90</strong>
                        </li>
                    </ul>
                    <p class="text-muted" style="font-size: 0.85rem;">Ao finalizar a assinatura, você concorda com nossos Termos de Uso e Política de Privacidade.</p>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const planoNomeElement = document.getElementById('plano-nome');
            const planoPrecoElement = document.getElementById('plano-preco');
            const totalPrecoElement = document.getElementById('total-preco');
            const planTypeRadios = document.querySelectorAll('input[name="planType"]');
            const paymentTabButtons = document.querySelectorAll('.payment-tab-button');
            const paymentContents = document.querySelectorAll('.payment-content');

            const precoMensal = 19.90;
            const precoAnual = 179.90;

            // --- Lógica de seleção de plano ---
            function updatePlanDetails() {
                let selectedPlanType = document.querySelector('input[name="planType"]:checked').value;
                let currentPrice = 0;

                if (selectedPlanType === 'anual') {
                    planoNomeElement.textContent = 'Premium Anual';
                    currentPrice = precoAnual;
                } else {
                    planoNomeElement.textContent = 'Premium Mensal';
                    currentPrice = precoMensal;
                }
                planoPrecoElement.textContent = `R$${currentPrice.toFixed(2).replace('.', ',')}`;
                totalPrecoElement.textContent = `R$${currentPrice.toFixed(2).replace('.', ',')}`;

                // Update PIX QR code and code (in a real scenario, this would be generated by your backend)
                const pixCodeInput = document.getElementById('pix-code');
                const pixQrCodeImg = document.getElementById('pix-qr-code');
                if (selectedPlanType === 'anual') {
                    // Example: a dummy PIX code for annual plan (replace with real logic)
                    pixCodeInput.value = '00020126580014BR.GOV.BCB.PIX0136a53266e-2ba4-41d4-8395-502842e22c065204000053039865405' + precoAnual.toFixed(2).replace('.', '') + '5802BR5913Nome Empresa6008BRASILIA62070503***6304CA27';
                    pixQrCodeImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=${encodeURIComponent(pixCodeInput.value)}`;
                } else {
                    // Example: a dummy PIX code for monthly plan (replace with real logic)
                    pixCodeInput.value = '00020126580014BR.GOV.BCB.PIX0136a53266e-2ba4-41d4-8395-502842e22c065204000053039865405' + precoMensal.toFixed(2).replace('.', '') + '5802BR5913Nome Empresa6008BRASILIA62070503***6304CA27';
                    pixQrCodeImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=${encodeURIComponent(pixCodeInput.value)}`;
                }
            }

            planTypeRadios.forEach(radio => {
                radio.addEventListener('change', updatePlanDetails);
            });

            // Set initial plan details on load
            updatePlanDetails();

            // --- Lógica de abas de pagamento (Cartão/PIX) ---
            paymentTabButtons.forEach(button => {
                button.addEventListener('click', () => {
                    const targetId = button.dataset.tabTarget;

                    paymentTabButtons.forEach(btn => btn.classList.remove('active'));
                    paymentContents.forEach(content => content.classList.remove('active'));

                    button.classList.add('active');
                    document.querySelector(targetId).classList.add('active');
                });
            });

            // --- Validação de Formulário Bootstrap ---
            const cardPaymentForm = document.getElementById('card-payment-form');
            cardPaymentForm.addEventListener('submit', function (event) {
                if (!cardPaymentForm.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                } else {
                    event.preventDefault(); // Impede o envio real do formulário para simulação
                    alert('Pagamento com Cartão simulado com sucesso! Sua assinatura foi ativada.');
                    // Em uma aplicação real, aqui você enviaria os dados para um servidor seguro.
                    // window.location.href = 'pagina-de-confirmacao.html';
                }
                cardPaymentForm.classList.add('was-validated');
            }, false);

            // --- Lógica do PIX ---
            window.copyPixCode = function() {
                const pixCodeInput = document.getElementById('pix-code');
                pixCodeInput.select();
                pixCodeInput.setSelectionRange(0, 99999); // Para mobile
                document.execCommand('copy');
                alert('Código PIX copiado!');
            };

            document.getElementById('confirm-pix-payment').addEventListener('click', function() {
                alert('Confirmação de pagamento PIX simulada. Sua assinatura será ativada após a compensação.');
                // Em um cenário real, você faria uma requisição ao backend para verificar o status do pagamento PIX.
                // Isso geralmente envolve o backend consultando a API do banco/PSP.
                // window.location.href = 'pagina-de-aguardando-pagamento.html';
            });

            // --- Máscaras para inputs ---
            document.getElementById('numeroCartao').addEventListener('input', function (e) {
                let value = e.target.value.replace(/\D/g, ''); // Remove non-digits
                let formattedValue = '';
                for (let i = 0; i < value.length; i++) {
                    if (i > 0 && i % 4 === 0) {
                        formattedValue += ' ';
                    }
                    formattedValue += value[i];
                }
                e.target.value = formattedValue;
            });

            document.getElementById('validade').addEventListener('input', function (e) {
                let value = e.target.value.replace(/\D/g, ''); // Remove non-digits
                if (value.length > 2) {
                    value = value.substring(0, 2) + '/' + value.substring(2, 4);
                }
                e.target.value = value;
            });

            document.getElementById('cep').addEventListener('input', function (e) {
                let value = e.target.value.replace(/\D/g, ''); // Remove non-digits
                if (value.length > 5) {
                    value = value.substring(0, 5) + '-' + value.substring(5, 8);
                }
                e.target.value = value;
            });
        });
    </script>
</body>
</html>
```

# templates\img\login.png

This is a binary file of the type: Image

# templates\img\qiZtFsNEjacT.png

This is a binary file of the type: Image

# templates\img\RfMh6PMcZtcv.png

This is a binary file of the type: Image

# templates\img\smart_fit_app-BR.png

This is a binary file of the type: Image

# templates\img\wgGO3n56mJld.png

This is a binary file of the type: Image

# tests\__init__.py

```py

```

# tests\conftest.py

```py
from datetime import datetime
import pytest
import os
import sys
import tempfile

# Adiciona o diretório raiz do projeto ao PYTHONPATH
# Isso permite importar módulos do projeto nos testes
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Fixture para criar um banco de dados temporário para testes
@pytest.fixture
def test_db():
    # Cria um arquivo temporário para o banco de dados
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    # Configura a variável de ambiente para usar o banco de teste
    os.environ['TEST_DATABASE_PATH'] = db_path
    # Retorna o caminho do banco de dados temporário
    yield db_path    
    # Remove o arquivo temporário ao concluir o teste
    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)


# @pytest.fixture
# def usuario_exemplo() -> Usuario:
#     """Objeto padrão de usuário para uso em testes."""
#     return Usuario(
#         id=0,
#         nome="Usuario Exemplo",
#         email="exemplo@teste.com",
#         hashed_password="senha_super_segura_123",
#         data_nascimento="2000-01-15",
#         sexo="F",
#         user_type="cliente"
#     )


# @pytest.fixture
# def profissional_exemplo() -> Cliente:
#     """Objeto de exemplo do tipo Cliente com user_type 'profissional'."""
#     return Cliente(
#         id=0,
#         nome="Profissional Exemplo",
#         email="profissional@teste.com",
#         hashed_password="senha_super_segura_123",
#         data_nascimento="1985-10-30",
#         sexo="F",
#         user_type="profissional",
#         master=False
#     )

```

