import sys
import os
from data.repo.cliente_repo import *
from data.models.cliente_model import *
from data.sql.cliente_sql import *
from data.repo.usuario_repo import *

class TestClienteRepo:
    def test_criar_tabela_cliente(self, test_db):
        resultado = criar_tabela_cliente()
        assert resultado == True, "A tabela de usuários não foi criada corretamente."       


    def test_inserir_cliente(self, test_db):
        criar_tabela_usuario()
        criar_tabela_cliente()
        cliente_teste = Cliente(0, "Cliente Teste", "Cliente@gmail.com", "senha123", "1990-01-01", "M", "cliente")
        id_usuario_db = inserir(cliente_teste)
        cliente_db = obter_por_id_cliente(id_usuario_db)
        assert cliente_db is not None, "O cliente inserido não deve ser None"
        assert cliente_db.id == 1, "O ID do cliente inserido deve ser igual a 1"
        assert cliente_db.nome == "Cliente Teste", "O nome do cliente inserido não confere"
        assert cliente_db.email == "Cliente@gmail.com", "O email do cliente inserido não confere"
        assert cliente_db.hashed_password == "senha123", "A senha do cliente inserido não confere"
        assert cliente_db.data_nascimento == "1990-01-01", "A data de nascimento do cliente inserido não confere"
        assert cliente_db.sexo == "M", "O sexo do cliente inserido não confere"
        assert cliente_db.user_type == "cliente", "O tipo de cliente inserido não confere"
        assert cliente_db.tipo_conta == "cliente", "O tipo de conta do cliente inserido não confere"
#
#  def test_obter_cliente_por_id_existente(self, test_db, cliente_exemplo):
#         # Arrange
#         cliente_repo.criar_tabela()        
#         id_cliente_inserido = cliente_repo.inserir(cliente_exemplo)
#         # Act
#         cliente_db = cliente_repo.obter_por_id(id_cliente_inserido)
#         # Assert
#         assert cliente_db is not None, "o cliente retornado deveria ser diferente de None"
#         assert cliente_db.id == id_cliente_inserido, "O id do cliente buscado deveria ser igual ao id do cliente inserido"
#         assert cliente_db.nome == cliente_exemplo.nome, "O nome do cliente buscado deveria ser igual ao nome do cliente inserido"

# def test_obter_cliente_por_id_inexistente(self, test_db):
#         # Arrange
#         cliente_repo.criar_tabela()
#         # Act
#         cliente_db = cliente_repo.obter_por_id(999)
#         # Assert
#         assert cliente_db is None, "O Cliente buscado com ID inexistente deveria retornar None"



# def test_excluir_cliente_existente(self, test_db, cliente_exemplo):
#         # Arrange
#         cliente_repo.criar_tabela()        
#         id_cliente_inserido = cliente_repo.inserir(cliente_exemplo)
#         # Act
#         resultado =cliente_repo.excluir(id_cliente_inserido)
#         # Assert
#         assert resultado == True, "O resultado da exclusão deveria ser True"
#         cliente_excluido = cliente_repo.obter_por_id(id_cliente_inserido)
#         assert cliente_excluido is None, "O cliente excluído deveria ser None"

# def test_excluir_cliente_inexistente(self, test_db):
#         # Arrange
#         cliente_repo.criar_tabela()
#         # Act
#         resultado = cliente_repo.excluir(999)
#         # Assert
#         assert resultado == False, "A exclusão de um cliente inexistente deveria retornar False"
