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
