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
    
def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return (cursor.rowcount > 0)
    
def obter_por_id(id: int) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
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