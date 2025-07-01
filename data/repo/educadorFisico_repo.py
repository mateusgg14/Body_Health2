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
