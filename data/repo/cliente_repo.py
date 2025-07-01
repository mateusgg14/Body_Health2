from typing import Optional
from data.repo import usuario_repo
from data.models.cliente_model import Cliente
from data.sql.cliente_sql import *
from data.models.usuario_model import Usuario
from data.util import get_connection


def criar_tabela_cliente() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
        return False

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

def obter_por_id_cliente(id: int) -> Optional[Cliente]:
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
