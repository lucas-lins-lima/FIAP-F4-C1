import pytest
from datetime import datetime, date
from sqlalchemy import text
from database import get_session, close_session
from database.models import (
    Produtor,
    Cultura,
    Sensor,
    LeituraSensor,
    Aplicacao
)
from database.repositories import (
    ProdutorRepository,
    CulturaRepository,
    SensorRepository,
    LeituraSensorRepository,
    AplicacaoRepository
)

@pytest.fixture
def session():
    """Fixture que fornece uma sessão do banco de dados."""
    session = get_session()
    yield session
    close_session()

@pytest.fixture
def produtor_repo(session):
    """Fixture que fornece um repositório de produtores."""
    return ProdutorRepository(session)

@pytest.fixture
def cultura_repo(session):
    """Fixture que fornece um repositório de culturas."""
    return CulturaRepository(session)

@pytest.fixture
def sensor_repo(session):
    """Fixture que fornece um repositório de sensores."""
    return SensorRepository(session)

@pytest.fixture
def leitura_repo(session):
    """Fixture que fornece um repositório de leituras."""
    return LeituraSensorRepository(session)

@pytest.fixture
def aplicacao_repo(session):
    """Fixture que fornece um repositório de aplicações."""
    return AplicacaoRepository(session)

def test_produtor_repository(produtor_repo, session):
    """Testa as operações do repositório de produtores."""
    # Criar produtor
    produtor = produtor_repo.create(
        nome="Maria Santos",
        email="maria.santos@email.com",
        telefone="(11) 98888-8888"
    )
    assert produtor.id_produtor is not None
    assert produtor.nome == "Maria Santos"
    
    # Buscar por ID
    produtor_busca = produtor_repo.get_by_id(produtor.id_produtor)
    assert produtor_busca is not None
    assert produtor_busca.email == "maria.santos@email.com"
    
    # Buscar por email
    produtor_email = produtor_repo.get_by_email("maria.santos@email.com")
    assert produtor_email is not None
    assert produtor_email.id_produtor == produtor.id_produtor
    
    # Atualizar
    produtor_repo.update(produtor.id_produtor, telefone="(11) 97777-7777")
    produtor_atualizado = produtor_repo.get_by_id(produtor.id_produtor)
    assert produtor_atualizado.telefone == "(11) 97777-7777"
    
    # Listar todos
    produtores = produtor_repo.get_all()
    assert len(produtores) > 0
    
    # Deletar
    produtor_repo.delete(produtor.id_produtor)
    produtor_deletado = produtor_repo.get_by_id(produtor.id_produtor)
    assert produtor_deletado is None

def test_cultura_repository(cultura_repo, produtor_repo, session):
    """Testa as operações do repositório de culturas."""
    # Criar produtor para teste
    produtor = produtor_repo.create(
        nome="José Oliveira",
        email="jose.oliveira@email.com",
        telefone="(11) 96666-6666"
    )
    
    # Criar cultura
    cultura = cultura_repo.create(
        nome="Soja",
        tipo="Grão",
        data_inicio=date(2024, 3, 1),
        id_produtor=produtor.id_produtor
    )
    assert cultura.id_cultura is not None
    assert cultura.nome == "Soja"
    
    # Buscar por ID
    cultura_busca = cultura_repo.get_by_id(cultura.id_cultura)
    assert cultura_busca is not None
    assert cultura_busca.tipo == "Grão"
    
    # Buscar por produtor
    culturas_produtor = cultura_repo.get_by_produtor(produtor.id_produtor)
    assert len(culturas_produtor) > 0
    assert culturas_produtor[0].id_cultura == cultura.id_cultura
    
    # Buscar culturas ativas
    culturas_ativas = cultura_repo.get_active_cultures()
    assert len(culturas_ativas) > 0
    
    # Buscar por tipo
    culturas_tipo = cultura_repo.get_cultures_by_type("Grão")
    assert len(culturas_tipo) > 0
    
    # Atualizar
    cultura_repo.update(cultura.id_cultura, nome="Soja Transgênica")
    cultura_atualizada = cultura_repo.get_by_id(cultura.id_cultura)
    assert cultura_atualizada.nome == "Soja Transgênica"
    
    # Deletar
    cultura_repo.delete(cultura.id_cultura)
    cultura_deletada = cultura_repo.get_by_id(cultura.id_cultura)
    assert cultura_deletada is None

def test_sensor_repository(sensor_repo, cultura_repo, produtor_repo, session):
    """Testa as operações do repositório de sensores."""
    # Criar produtor e cultura para teste
    produtor = produtor_repo.create(
        nome="Ana Costa",
        email="ana.costa@email.com",
        telefone="(11) 95555-5555"
    )
    cultura = cultura_repo.create(
        nome="Café",
        tipo="Permanente",
        data_inicio=date(2024, 3, 1),
        id_produtor=produtor.id_produtor
    )
    
    # Criar sensor
    sensor = sensor_repo.create(
        tipo="Umidade",
        modelo="SHT30",
        localizacao="Setor B",
        id_cultura=cultura.id_cultura
    )
    assert sensor.id_sensor is not None
    assert sensor.tipo == "Umidade"
    
    # Buscar por ID
    sensor_busca = sensor_repo.get_by_id(sensor.id_sensor)
    assert sensor_busca is not None
    assert sensor_busca.modelo == "SHT30"
    
    # Buscar por cultura
    sensores_cultura = sensor_repo.get_by_cultura(cultura.id_cultura)
    assert len(sensores_cultura) > 0
    assert sensores_cultura[0].id_sensor == sensor.id_sensor
    
    # Buscar por tipo
    sensores_tipo = sensor_repo.get_by_type("Umidade")
    assert len(sensores_tipo) > 0
    
    # Buscar por modelo
    sensores_modelo = sensor_repo.get_by_model("SHT30")
    assert len(sensores_modelo) > 0
    
    # Atualizar
    sensor_repo.update(sensor.id_sensor, localizacao="Setor C")
    sensor_atualizado = sensor_repo.get_by_id(sensor.id_sensor)
    assert sensor_atualizado.localizacao == "Setor C"
    
    # Deletar
    sensor_repo.delete(sensor.id_sensor)
    sensor_deletado = sensor_repo.get_by_id(sensor.id_sensor)
    assert sensor_deletado is None

def test_leitura_sensor_repository(leitura_repo, sensor_repo, cultura_repo, produtor_repo, session):
    produtor = produtor_repo.create(
        nome="Pedro Lima",
        email="pedro.lima@email.com",
        telefone="(11) 94444-4444"
    )
    cultura = cultura_repo.create(
        nome="Algodão",
        tipo="Fibra",
        data_inicio=date(2024, 3, 1),
        id_produtor=produtor.id_produtor
    )
    sensor = sensor_repo.create(
        tipo="NPK",
        modelo="NPK-01",
        localizacao="Setor A",
        id_cultura=cultura.id_cultura
    )
    
    # Criar leitura
    leitura = leitura_repo.create(
        id_sensor=sensor.id_sensor,
        valor_umidade=45.5,
        valor_ph=6.8,
        valor_npk_fosforo=15.2,
        valor_npk_potassio=20.1
    )
    assert leitura.id_leitura is not None
    assert leitura.valor_umidade == 45.5
    
    # Buscar por ID
    leitura_busca = leitura_repo.get_by_id(leitura.id_leitura)
    assert leitura_busca is not None
    assert leitura_busca.valor_ph == 6.8
    
    # Buscar por sensor
    leituras_sensor = leitura_repo.get_by_sensor(sensor.id_sensor)
    assert len(leituras_sensor) > 0
    assert leituras_sensor[0].id_leitura == leitura.id_leitura
    
    # Buscar por data
    data_inicio = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    data_fim = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
    leituras_periodo = leitura_repo.get_by_date_range(data_inicio, data_fim)
    assert len(leituras_periodo) > 0
    
    # Atualizar
    leitura_repo.update(leitura.id_leitura, valor_umidade=50.0)
    leitura_atualizada = leitura_repo.get_by_id(leitura.id_leitura)
    assert leitura_atualizada.valor_umidade == 50.0
    
    # Deletar
    leitura_repo.delete(leitura.id_leitura)
    leitura_deletada = leitura_repo.get_by_id(leitura.id_leitura)
    assert leitura_deletada is None

def test_aplicacao_repository(aplicacao_repo, cultura_repo, produtor_repo, session):
    """Testa as operações do repositório de aplicações."""
    # Criar produtor e cultura para teste
    produtor = produtor_repo.create(
        nome="Carlos Silva",
        email="carlos.silva@email.com",
        telefone="(11) 93333-3333"
    )
    cultura = cultura_repo.create(
        nome="Milho",
        tipo="Grão",
        data_inicio=date(2024, 3, 1),
        id_produtor=produtor.id_produtor
    )
    
    # Criar aplicação
    aplicacao = aplicacao_repo.create(
        id_cultura=cultura.id_cultura,
        tipo="Fertilizante",
        quantidade=100.0
    )
    assert aplicacao.id_aplicacao is not None
    assert aplicacao.tipo == "Fertilizante"
    
    # Buscar por ID
    aplicacao_busca = aplicacao_repo.get_by_id(aplicacao.id_aplicacao)
    assert aplicacao_busca is not None
    assert aplicacao_busca.quantidade == 100.0
    
    # Buscar por cultura
    aplicacoes_cultura = aplicacao_repo.get_by_cultura(cultura.id_cultura)
    assert len(aplicacoes_cultura) > 0
    assert aplicacoes_cultura[0].id_aplicacao == aplicacao.id_aplicacao
    
    # Buscar por tipo
    aplicacoes_tipo = aplicacao_repo.get_by_type("Fertilizante")
    assert len(aplicacoes_tipo) > 0
    
    # Atualizar
    aplicacao_repo.update(aplicacao.id_aplicacao, quantidade=150.0)
    aplicacao_atualizada = aplicacao_repo.get_by_id(aplicacao.id_aplicacao)
    assert aplicacao_atualizada.quantidade == 150.0
    
    # Deletar
    aplicacao_repo.delete(aplicacao.id_aplicacao)
    aplicacao_deletada = aplicacao_repo.get_by_id(aplicacao.id_aplicacao)
    assert aplicacao_deletada is None 