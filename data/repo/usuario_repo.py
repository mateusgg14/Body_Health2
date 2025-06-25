from typing import Any, Optional
from data.models.usuario_model import Usuario
from data.sql.usuario_sql import *
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return (cursor.rowcount > 0)

def inserir(usuario: Usuario, cursor: Any) -> Optional[int]:
    cursor.execute(INSERIR, (
        usuario.nome,
        usuario.email,
        usuario.hashed_password,
        usuario.data_nascimento,
        usuario.sexo,
        usuario.user_type))
    return cursor.lastrowid
    
def alterar(usuario: Usuario, cursor: Any) -> bool:
    cursor.execute(ALTERAR, (
        usuario.nome,
        usuario.email,
        usuario.data_nascimento,
        usuario.sexo,
        usuario.user_type,
        usuario.id))
    return (cursor.rowcount > 0)
    
def atualizar_senha(id: int, hashed_password: str, cursor: Any) -> bool:
    cursor.execute(ALTERAR_SENHA, (hashed_password, id))
    return (cursor.rowcount > 0)
    
def excluir(id: int, cursor: Any) -> bool:
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
                senha=row["senha"],
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
                senha=row["senha"],
                data_nascimento=row["data_nascimento"],
                sexo=row["sexo"],
                user_type=row["user_type"]) 
                for row in rows]
        return usuarios