from typing import Optional, Any
from data.models.profissional_model import Profissional
from data.models.usuario_model import Usuario
from data.sql.profissional_sql import *
from data.repo import usuario_repo
from data.util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return (cursor.rowcount > 0)

def inserir(profissional: Profissional) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        # Primeiro, insere na tabela de usuário
        id_usuario = usuario_repo.inserir(profissional, cursor)
        if id_usuario is None:
            return None

        # Depois, insere na tabela de profissional
        cursor.execute(INSERIR, (
            profissional.tipo_profissional,
            profissional.status,
            int(profissional.master)))
        conn.commit()
        return id_usuario

def alterar(profissional: Profissional) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        ok_usuario = usuario_repo.alterar(profissional, cursor)
        cursor.execute(ALTERAR, (
            profissional.tipo_profissional,
            profissional.status,
            int(profissional.master),
            profissional.id))
        conn.commit()
        return ok_usuario and cursor.rowcount > 0

def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        ok_profissional = cursor.rowcount > 0
        ok_usuario = usuario_repo.excluir(id, cursor)
        conn.commit()
        return ok_profissional and ok_usuario

def obter_por_id(id: int) -> Optional[Profissional]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row is None:
            return None
        profissional = Profissional(
            id=row["id"],
            nome=row["nome"],
            email=row["email"],
            senha=row["senha"],
            data_nascimento="",  # Você pode preencher com nova query se necessário
            sexo="",
            user_type="profissional",
            tipo_profissional=row["tipo_profissional"],
            status=row["status"],
            master=bool(row["master"])
        )
        return profissional

def obter_todos() -> list[Profissional]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        profissionais = [
            Profissional(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                data_nascimento="",
                sexo="",
                user_type="profissional",
                tipo_profissional=row["tipo_profissional"],
                status=row["status"],
                master=bool(row["master"])
            ) for row in rows
        ]
        return profissionais
