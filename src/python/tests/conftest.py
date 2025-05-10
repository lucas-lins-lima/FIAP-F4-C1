import pytest
from datetime import datetime
from typing import Generator
from sqlalchemy import text
from dotenv import load_dotenv
import os

from database.models import Base, SensorData
from database.repositories import (
    ProdutorRepository,
    CulturaRepository,
    SensorRepository,
    LeituraSensorRepository,
    AplicacaoRepository
)
from services.sensor_service import SensorService
from database import engine, get_session, close_session

# Carrega as variáveis de ambiente
load_dotenv()

def create_sequence(engine, seq_name):
    """Cria uma sequência no banco de dados."""
    with engine.connect() as conn:
        conn.execute(text(f"""
            BEGIN
                EXECUTE IMMEDIATE 'CREATE SEQUENCE {seq_name} START WITH 1 INCREMENT BY 1';
            EXCEPTION
                WHEN OTHERS THEN
                    IF SQLCODE = -955 THEN
                        NULL; -- Sequência já existe
                    ELSE
                        RAISE;
                    END IF;
            END;
        """))
        conn.commit()

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Fixture para configurar o banco de dados."""
    # Criar todas as tabelas
    Base.metadata.create_all(engine)
    
    # Criar sequências
    sequences = [
        'produtor_seq',
        'cultura_seq',
        'sensor_seq',
        'leitura_sensor_seq',
        'aplicacao_seq',
        'sensor_data_seq'
    ]
    
    for seq in sequences:
        create_sequence(engine, seq)
    
    yield
    
    # Limpar após os testes
    Base.metadata.drop_all(engine)

@pytest.fixture
def session():
    """Fixture que fornece uma sessão do banco de dados."""
    session = get_session()
    yield session
    session.rollback()
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

@pytest.fixture
def sensor_service(sensor_repo: SensorRepository) -> SensorService:
    """Fixture para o serviço de sensores."""
    return SensorService(sensor_repo)

@pytest.fixture
def sample_sensor_data() -> SensorData:
    """Fixture para dados de sensor de exemplo."""
    return SensorData(
        timestamp=datetime.now(),
        phosphorus_level=True,
        potassium_level=True,
        ph_level=6.5,
        soil_moisture=45.0,
        irrigation_active=False
    ) 