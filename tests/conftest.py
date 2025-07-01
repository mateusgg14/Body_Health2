from datetime import datetime
import pytest
import os
import sys
import tempfile
from data.models.cliente_model import *
from data.models.usuario_model import *
from data.repo.usuario_repo import *
from data.models.profissional_model import *
from data.repo.profissional_repo import *
from data.models.administrador_model import *
from data.repo.administrador_repo import *
from data.repo.administrador_repo import *


# Configuração do ambiente de teste
# Adiciona o diretório raiz do projeto ao PYTHONPATH
# Isso permite importar módulos do projeto nos testes
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Fixture para criar um banco de dados temporário para testes
@pytest.fixture
def test_db():
    # Cria um arquivo temporário para o banco de dados
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    # Configura a variável de ambiente para usar o banco de teste
    os.environ['TEST_DATABASE_PATH'] = db_path
    # Retorna o caminho do banco de dados temporário
    yield db_path    
    # Remove o arquivo temporário ao concluir o teste
    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture
def usuario_exemplo() -> Usuario:
    """Objeto padrão de usuário para uso em testes."""
    return Usuario(
        id=0,
        nome="Usuario Exemplo",
        email="exemplo@teste.com",
        hashed_password="senha_super_segura_123",
        data_nascimento="2000-01-15",
        sexo="F",
        user_type="cliente"
    )


@pytest.fixture
def profissional_exemplo() -> Profissional:
    """Objeto de exemplo do tipo Profissional."""
    return Profissional(
        id=0,
        nome="Profissional Exemplo",
        email="profissional@teste.com",
        hashed_password="senha_super_segura_123",
        data_nascimento="1985-10-30",
        sexo="F",
        user_type="profissional",
        tipo_profissional="nutricionista",
        status="ativo"
    )

@pytest.fixture
def administrador_exemplo() -> Administrador:
    """Objeto padrão de usuário para uso em testes."""
    return Administrador(
        id=0,
        nome="Usuario Exemplo",
        email="exemplo@teste.com",
        hashed_password="senha_super_segura_123",
        data_nascimento="2000-01-15",
        sexo="F",
        user_type="cliente",
        master= True
    )