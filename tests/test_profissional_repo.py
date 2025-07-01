# tests/test_profissional_repo.py (versão final completa)

from data.repo.profissional_repo import *
from data.repo import usuario_repo
from data.models.profissional_model import *
from data.sql.profissional_sql import *

class TestProfissionalRepo:
    def test_criar_tabela_profissional(self, test_db):
        resultado = criar_tabela()
        assert resultado == True, "A tabela de usuários não foi criada corretamente."       

    def test_inserir_profissional(self, test_db, profissional_exemplo):
        criar_tabela_usuario()
        criar_tabela()
        # Act
        id_inserido = inserir(profissional_exemplo)
        profissional_db = obter_por_id(id_inserido)
        
        # Assert
        assert profissional_db is not None, "O profissional inserido não deveria ser None"
        assert profissional_db.id == id_inserido, "O ID do profissional não confere"
        assert profissional_db.nome == profissional_exemplo.nome, "O nome não confere"
        assert profissional_db.tipo_profissional == profissional_exemplo.tipo_profissional, "O tipo de profissional não confere"



    def test_obter_profissional_por_id_existente(self, test_db, profissional_exemplo):
        criar_tabela()
        criar_tabela_usuario()
        id_inserido = inserir(profissional_exemplo)

        # Act
        profissional_encontrado = obter_por_id(id_inserido)

        # Assert
        assert profissional_encontrado is not None, "Deveria encontrar o profissional inserido"
        assert profissional_encontrado.id == id_inserido, "O ID do profissional encontrado não confere"
        assert profissional_encontrado.nome == profissional_exemplo.nome, "O nome do profissional encontrado não confere"

    def test_obter_profissional_por_id_inexistente(self, test_db):
        criar_tabela_usuario()
        criar_tabela()
        profissional_db = obter_por_id(999)
        # Assert
        assert profissional_db is None, "Deveria retornar None para um ID inexistente"

    def test_alterar_profissional_existente(self, test_db, profissional_exemplo):
        criar_tabela_usuario()
        criar_tabela()
        # Arrange
        id_inserido = inserir(profissional_exemplo)
        profissional_para_alterar = obter_por_id(id_inserido)

        # Act
        profissional_para_alterar.nome = "Dra. Exemplo Alterada"
        profissional_para_alterar.status = "inativo"
        resultado = alterar(profissional_para_alterar)
        profissional_alterado_db = obter_por_id(id_inserido)

        # Assert
        assert resultado is True, "A operação de alterar deveria retornar True"
        assert profissional_alterado_db.nome == "Dra. Exemplo Alterada", "O nome não foi alterado corretamente"
        assert profissional_alterado_db.status == "inativo", "O status não foi alterado corretamente"
        
    def test_alterar_profissional_inexistente(self, test_db, profissional_exemplo):
        # Arrange
        profissional_exemplo.id = 999  # Um ID que não existe
        # Act
        resultado = alterar(profissional_exemplo)
        # Assert
        assert resultado is False, "A tentativa de alterar um profissional inexistente deveria retornar False"

    def test_excluir_profissional_existente(self, test_db, profissional_exemplo):
        criar_tabela_usuario()
        criar_tabela()

        # Arrange
        id_inserido = inserir(profissional_exemplo)
        
        # Act
        resultado = excluir(id_inserido)
        profissional_excluido = obter_por_id(id_inserido)

        # Assert
        assert resultado is True, "A operação de excluir deveria retornar True"
        assert profissional_excluido is None, "O registro na tabela 'profissional' deveria ter sido excluído"

    def test_excluir_profissional_inexistente(self, test_db):
        # Act
        resultado = excluir(999)
        # Assert
        assert resultado is False, "A tentativa de excluir um profissional inexistente deveria retornar False"

    def test_atualizar_senha_profissional_existente(self, test_db, profissional_exemplo):
        criar_tabela_usuario()
        criar_tabela()
        """
        Testa a atualização da senha de um profissional existente.
        A funcionalidade reside no usuario_repo, mas é testada aqui por contexto.
        """
        # Arrange
        id_profissional = inserir(profissional_exemplo)
        nova_senha = "senha_profissional_nova_456"

        # Act
        resultado = usuario_repo.atualizar_senha(id_profissional, nova_senha)

        # Assert
        assert resultado is True, "A função de atualizar senha deveria retornar True"

        # Verificação extra
        usuario_com_senha_alterada = usuario_repo.obter_por_id(id_profissional)
        assert usuario_com_senha_alterada is not None, "Não foi possível encontrar o usuário após a atualização da senha"
        assert usuario_com_senha_alterada.hashed_password == nova_senha, "A senha no banco de dados não corresponde à nova senha"