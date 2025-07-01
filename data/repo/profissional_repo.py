from typing import Optional
from data.models.usuario_model import *
from data.repo.usuario_repo import *
from data.sql.profissional_sql import *
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
        usuario = Usuario(0,
            profissional.nome,
            profissional.email,
            profissional.hashed_password,
            profissional.data_nascimento,
            profissional.sexo,
            profissional.user_type)
        cod_profissional = usuario_repo.inserir(usuario)
        cursor.execute(INSERIR, (
            profissional.tipo_profissional,
            profissional.status)),
        return cod_profissional                        



def alterar(profissional: Profissional) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Atualiza o nome na tabela usuario
            cursor.execute("""
                UPDATE usuario
                SET nome = ?
                WHERE id = ?
            """, (profissional.nome, profissional.id))
            
            # Atualiza tipo_profissional e status na tabela profissional
            cursor.execute("""
                UPDATE profissional
                SET tipo_profissional = ?, status = ?
                WHERE id = ?
            """, (profissional.tipo_profissional, profissional.status, profissional.id))
            
            conn.commit()
            return True
    except Exception as e:
        print(f"Erro ao alterar profissional: {e}")
        return False

    


def excluir(id: int) -> bool:
    try:
        return usuario_repo.excluir(id)  # só passa o id mesmo
    except Exception as e:
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
