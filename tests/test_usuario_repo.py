import sys
import os
from data.repo.usuario_repo import *
from data.models.usuario_model import Usuario


class TestUsuarioRepo:
    def test_criar_tabela_usuario(self, test_db):
        resultado = criar_tabela()
        assert resultado == True, "A tabela de usuários não foi criada corretamente."       



    def test_inserir_usuario(self, test_db):
        criar_tabela()
        usuario_teste = Usuario(0, "Usuario Teste", "Usuario@gmail.com", "senha123", "1990-01-01", "M", "cliente")
        id_usuario_db = inserir(usuario_teste)
        usuario_db = obter_por_id(id_usuario_db)
        assert usuario_db is not None, "O usuário inserido não deve ser None"
        assert usuario_db.id == 1, "O ID do usuário inserido deve ser igual a 1"
        assert usuario_db.nome == "Usuario Teste", "O nome do usuário inserido não confere"
        assert usuario_db.email == "Usuario@gmail.com", "O email do usuário inserido não confere"
        assert usuario_db.hashed_password == "senha123", "A senha do usuário inserido não confere"
        assert usuario_db.data_nascimento == "1990-01-01", "A data de nascimento do usuário inserido não confere"
        assert usuario_db.sexo == "M", "O sexo do usuário inserido não confere"
        assert usuario_db.user_type == "cliente", "O tipo de usuário inserido não confere"
        
    