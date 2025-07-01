from data.repo import usuario_repo
from data.repo.usuario_repo import *
from data.models.usuario_model import Usuario


class TestUsuarioRepo:
    def test_criar_tabela_usuario(self, test_db):
        resultado = criar_tabela_usuario()
        assert resultado == True, "A tabela de usuários não foi criada corretamente."       

    def test_inserir_usuario(self, test_db):
        criar_tabela_usuario()
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
        
    def test_obter_usuario_por_id_existente(self, test_db, usuario_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuario()        
        id_usuario_inserido = usuario_repo.inserir(usuario_exemplo)
        # Act
        usuario_db = usuario_repo.obter_por_id(id_usuario_inserido)
        # Assert
        assert usuario_db is not None, "o usuario retornado deveria ser diferente de None"
        assert usuario_db.id == id_usuario_inserido, "O id do usuario buscado deveria ser igual ao id do usuario inserido"
        assert usuario_db.nome == usuario_exemplo.nome, "O nome do usuario buscado deveria ser igual ao nome do usuario inserido"

    def test_alterar_usuario_existente(self, test_db, usuario_exemplo):
        usuario_repo.criar_tabela_usuario()  # <-- necessário!
        # Arrange
        id_inserido = usuario_repo.inserir(usuario_exemplo)
        usuario_para_alterar = usuario_repo.obter_por_id(id_inserido)
        # Act: Altera o nome e o tipo do usuário
        usuario_para_alterar.nome = "Nome Alterado"
        usuario_para_alterar.user_type = "profissional"
        resultado = usuario_repo.alterar(usuario_para_alterar)
        usuario_alterado_db = usuario_repo.obter_por_id(id_inserido)
        # Assert
        assert resultado is True
        assert usuario_alterado_db.nome == "Nome Alterado"

    def test_atualizar_senha_existente(self, test_db, usuario_exemplo):
        usuario_repo.criar_tabela_usuario()  # <-- necessário!
        # Arrange
        id_inserido = usuario_repo.inserir(usuario_exemplo)
        nova_senha = "nova_senha_123"
        # Act: Chama a função corretamente com (id, senha)
        resultado = usuario_repo.atualizar_senha(id_inserido, nova_senha)
        usuario_atualizado_db = usuario_repo.obter_por_id(id_inserido)
        # Assert
        assert resultado is True
        assert usuario_atualizado_db.hashed_password == nova_senha

    def test_atualizar_senha_usuario_inexistente(self, test_db):
        usuario_repo.criar_tabela_usuario()  # <-- necessário!
        """Testa a falha ao tentar atualizar a senha de um ID que não existe."""
        # Act: Chama a função corretamente com (id, senha) para um usuário que não existe
        resultado = usuario_repo.atualizar_senha(id=999, hashed_password="nova_senha")        
        # Assert: O resultado DEVE ser False
        assert resultado is False

# Em tests/test_usuario_repo.py

    def test_excluir_usuario_existente(self, test_db, usuario_exemplo):
        usuario_repo.criar_tabela_usuario()  # <-- necessário!
        # Arrange: Insere um usuário para poder excluí-lo
        id_inserido = usuario_repo.inserir(usuario_exemplo)        
        # Act: Exclui o usuário e depois tenta buscá-lo
        resultado = usuario_repo.excluir(id_inserido)
        usuario_excluido = usuario_repo.obter_por_id(id_inserido)        
        # Assert: O resultado da exclusão deve ser True e o usuário não deve ser encontrado
        assert resultado is True
        assert usuario_excluido is None

    def test_excluir_usuario_inexistente(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuario()
        # Act
        resultado = usuario_repo.excluir(999)
        # Assert
        assert resultado == False, "A exclusão de um usuário inexistente deveria retornar False"
