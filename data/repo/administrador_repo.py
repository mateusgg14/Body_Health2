from typing import Optional
from data.models.usuario_model import *
from data.models.administrador_model import Administrador
from data.sql.administrador_sql import *
from data.models.usuario_model import Usuario
from data.repo import usuario_repo
from data.util import get_connection

def criar_tabela_administrador() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
        return False

def inserir_administrador(administrador: Administrador) -> Optional[int]:
     with get_connection() as conn:
        cursor = conn.cursor()
        usuario = Usuario(0,
            administrador.nome,
            administrador.email,
            administrador.hashed_password,
            administrador.data_nascimento,
            administrador.sexo,
            administrador.user_type)
        cod_administrador = usuario_repo.inserir(usuario)
        cursor.execute(INSERIR, (
            administrador.id,
            administrador.master)),
        return cod_administrador
      
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

def obter_por_id_administrador(id: int) -> Optional[Administrador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Administrador(
            id=row["id"],
            nome=row["nome"],
            email=row["email"],
            hashed_password=row["senha"],
            data_nascimento="",
            sexo="",
            user_type="administrador",
            master=row["master"])   
    
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