from data.repo.administrador_repo import *
from data.repo.usuario_repo import *
from data.models.administrador_model import *
from data.sql.administrador_sql import *

class TestAdministradorRepo:
    def test_criar_tabela_administrador(self, test_db):
        resultado = criar_tabela_administrador()
        assert resultado == True, "A tabela de usuários não foi criada corretamente."       

    def test_inserir_administrador(self, test_db, administrador_exemplo):
        criar_tabela_usuario()
        criar_tabela_administrador()
        # Act
        id_inserido = inserir_administrador(administrador_exemplo)
        administrador_db = obter_por_id_administrador(id_inserido)
        
        # Assert
        assert administrador_db is not None, "O usuário inserido não deve ser None"
        assert administrador_db.id == id_inserido, "O ID do profissional não confere"
        assert administrador_db.master == administrador_exemplo.master, "O nome não confere"


    # def test_obter_administrador_por_id_existente(self, test_db, administrador_exemplo, usuario_exemplo):
    #     # Arrange: prepara o banco e insere um administrador
    #     usuario_repo.criar_tabela()
    #     usuario_repo.inserir(usuario_exemplo)
    #     administrador_repo.criar_tabela()
    #     id_administrador_inserido = administrador_repo.inserir(administrador_exemplo)
    #     # Act: busca o administrador pelo ID
    #     administrador_encontrado = administrador_repo.obter_por_id(id_administrador_inserido)
    #     # Assert: verifica se encontrou o administrador correto
    #     assert administrador_encontrado is not None, "Deveria encontrar o administrador inserido"
    #     assert administrador_encontrado.id == id_administrador_inserido, "O ID não confere"
    #     assert administrador_encontrado.nome == administrador_exemplo.nome, "O nome não confere"
    #     assert administrador_encontrado.email == administrador_exemplo.email, "O email não confere"
    #     assert administrador_encontrado.hashed_password == administrador_exemplo.hashed_password, "A senha não confere"
    #     assert administrador_encontrado.sexo == administrador_exemplo.sexo, "O sexo não confere"
    #     assert administrador_encontrado.user_type == administrador_exemplo.user_type, "O tipo de usuário não confere"
    #     assert administrador_encontrado.master == administrador_exemplo.master, "O master não confere"

    # def test_obter_administrador_por_id_inexistente(self, test_db):
    #     # Arrange: prepara o banco (sem inserir administradores)
    #     usuario_repo.criar_tabela()
    #     administrador_repo.criar_tabela()
    #     # Act: tenta buscar um administrador com ID que não existe
    #     administrador_encontrado = administrador_repo.obter_por_id(999)
    #     # Assert: verifica se retorna None
    #     assert administrador_encontrado is None, "Deveria retornar None para administrador inexistente"

    # def test_atualizar_administrador_existente(self, test_db, administrador_exemplo, usuario_exemplo):
    #     # Arrange: insere um administrador para depois atualizar
    #     usuario_repo.criar_tabela()
    #     usuario_repo.inserir(usuario_exemplo)
    #     administrador_repo.criar_tabela()
    #     id_administrador_inserido = administrador_repo.inserir(administrador_exemplo)
    #     administrador_inserido = administrador_repo.obter_por_id(id_administrador_inserido)
    #     # Modifica os dados do administrador
    #     administrador_inserido.nome = "Administrador Atualizado"
    #     administrador_inserido.email = "atualizado@example.com"
    #     administrador_inserido.sexo = "Feminino"
    #     administrador_inserido.user_type = "administrador"
    #     # Act: atualiza o administrador
    #     resultado = administrador_repo.alterar(administrador_inserido)
    #     # Assert: verifica se a atualização foi bem-sucedida
    #     assert resultado == True, "A atualização deveria retornar True"
    #     # Verifica se os dados foram realmente atualizados no banco
    #     administrador_atualizado = administrador_repo.obter_por_id(administrador_inserido.id)
    #     assert administrador_atualizado.nome == "Administrador Atualizado", "O nome não foi atualizado"
    #     assert administrador_atualizado.email == "atualizado@example.com", "O email não foi atualizado"
    #     assert administrador_atualizado.sexo == "Feminino", "O sexo não foi atualizado"
    #     assert administrador_atualizado.user_type == "administrador", "O tipo de usuário não foi atualizado"
    #     assert administrador_atualizado.master == administrador_exemplo.master, "O master não foi atualizado"

    # def test_atualizar_administrador_inexistente(self, test_db, administrador_exemplo):
    #     # Arrange: prepara o banco sem inserir administradores
    #     usuario_repo.criar_tabela()
    #     administrador_repo.criar_tabela()
    #     administrador_exemplo.id = 999  # ID que não existe
    #     # Act: tenta atualizar um administrador inexistente
    #     resultado = administrador_repo.alterar(administrador_exemplo)
    #     # Assert: verifica se retorna False
    #     assert resultado == False, "Deveria retornar False para administrador inexistente"

    # def test_excluir_administrador_existente(self, test_db, administrador_exemplo, usuario_exemplo):
    #     # Arrange: insere um administrador para depois excluir
    #     usuario_repo.criar_tabela()
    #     usuario_repo.inserir(usuario_exemplo)
    #     administrador_repo.criar_tabela()
    #     id_administrador_inserido = administrador_repo.inserir(administrador_exemplo)
    #     # Act: exclui o administrador
    #     resultado = administrador_repo.excluir(id_administrador_inserido)
    #     # Assert: verifica se a exclusão foi bem-sucedida
    #     assert resultado == True, "A exclusão deveria retornar True"
    #     # Verifica se o administrador foi realmente excluído
    #     administrador_excluido = administrador_repo.obter_por_id(id_administrador_inserido)
    #     assert administrador_excluido is None, "O administrador deveria ter sido excluído"

    # def test_excluir_administrador_inexistente(self, test_db):
    #     # Arrange: prepara o banco sem administradores
    #     usuario_repo.criar_tabela()
    #     administrador_repo.criar_tabela()
    #     # Act: tenta excluir um administrador inexistente
    #     resultado = administrador_repo.excluir(999)
    #     # Assert: verifica se retorna False
    #     assert resultado == False, "Deveria retornar False para administrador inexistente"