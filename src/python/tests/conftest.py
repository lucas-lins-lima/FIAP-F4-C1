import pytest
from datetime import datetime
from typing import Generator
from sqlalchemy import text
from dotenv import load_dotenv
import os

from database.models import Base, SensorRecord
from database.repositories import (
    ProducerRepository,
    CropRepository,
    ComponentRepository,
    SensorRecordRepository,
    ApplicationRepository
)
from database import engine, get_session, close_session
from services.sensor_service import ComponentService

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
        'producer_seq',
        'crop_seq',
        'component_seq',
        'sensor_record_seq',
        'application_seq'
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
def producer_repo(session):
    """Fixture que fornece um repositório de produtores."""
    return ProducerRepository(session)


@pytest.fixture
def crop_repo(session):
    """Fixture que fornece um repositório de culturas."""
    return CropRepository(session)


@pytest.fixture
def component_repo(session):
    """Fixture que fornece um repositório de componentes."""
    return ComponentRepository(session)


@pytest.fixture
def sensor_record_repo(session):
    """Fixture que fornece um repositório de registros de sensor."""
    return SensorRecordRepository(session)


@pytest.fixture
def application_repo(session):
    """Fixture que fornece um repositório de aplicações."""
    return ApplicationRepository(session)


@pytest.fixture
def sensor_service(component_repo: ComponentRepository) -> ComponentService:
    """Fixture para o serviço de sensores."""
    return ComponentService(component_repo)


@pytest.fixture
def sample_sensor_record() -> SensorRecord:
    """Fixture para dados de sensor de exemplo."""
    return SensorRecord(
        sensor_id="123e4567-e89b-12d3-a456-426614174000",
        timestamp=datetime.now(),
        phosphorus_present=True,
        potassium_present=True,
        soil_ph=6.5,
        soil_moisture=45.0,
        irrigation_status="DESLIGADA"
    )
