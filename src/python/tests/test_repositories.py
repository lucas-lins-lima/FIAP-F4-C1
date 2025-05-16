import pytest
from datetime import datetime, date, timedelta
from sqlalchemy import text
from database import get_session, close_session
from database.models import (
    Producer,
    Crop,
    Component,
    SensorRecord,
    Application
)
from database.repositories import (
    ProducerRepository,
    CropRepository,
    ComponentRepository,
    SensorRecordRepository,
    ApplicationRepository
)


@pytest.fixture
def session():
    """Fixture que fornece uma sessão do banco de dados."""
    session = get_session()
    yield session
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


def test_producer_repository(producer_repo, session):
    """Testa as operações do repositório de produtores."""
    # Criar produtor
    producer = producer_repo.create(
        name="Maria Santos",
        email="maria.santos@email.com",
        phone="(11) 98888-8888"
    )
    assert producer.id is not None
    assert producer.name == "Maria Santos"

    # Buscar por ID
    producer_search = producer_repo.get_by_id(producer.id)
    assert producer_search is not None
    assert producer_search.email == "maria.santos@email.com"

    # Atualizar
    producer_repo.update(producer.id, phone="(11) 97777-7777")
    producer_updated = producer_repo.get_by_id(producer.id)
    assert producer_updated.phone == "(11) 97777-7777"

    # Listar todos
    producers = producer_repo.get_all()
    assert len(producers) > 0

    # Deletar
    producer_repo.delete(producer.id)
    producer_deleted = producer_repo.get_by_id(producer.id)
    assert producer_deleted is None


def test_crop_repository(crop_repo, producer_repo, session):
    """Testa as operações do repositório de culturas."""
    # Criar produtor para teste
    producer = producer_repo.create(
        name="José Oliveira",
        email="jose.oliveira@email.com",
        phone="(11) 96666-6666"
    )

    # Criar cultura
    crop = crop_repo.create(
        name="Soja",
        type="Grão",
        start_date=date(2024, 3, 1),
        producer_id=producer.id
    )
    assert crop.id is not None
    assert crop.name == "Soja"

    # Buscar por ID
    crop_search = crop_repo.get_by_id(crop.id)
    assert crop_search is not None
    assert crop_search.type == "Grão"

    # Atualizar
    crop_repo.update(crop.id, name="Soja Transgênica")
    crop_updated = crop_repo.get_by_id(crop.id)
    assert crop_updated.name == "Soja Transgênica"

    # Deletar
    crop_repo.delete(crop.id)
    crop_deleted = crop_repo.get_by_id(crop.id)
    assert crop_deleted is None


def test_component_repository(component_repo, crop_repo, producer_repo, session):
    """Testa as operações do repositório de componentes."""
    # Criar produtor e cultura para teste
    producer = producer_repo.create(
        name="Ana Costa",
        email="ana.costa@email.com",
        phone="(11) 95555-5555"
    )
    crop = crop_repo.create(
        name="Café",
        type="Permanente",
        start_date=date(2024, 3, 1),
        producer_id=producer.id
    )

    # Criar componente (sensor)
    component = component_repo.create(
        name="Sensor de Umidade",
        type="Sensor",
        crop_id=crop.id
    )
    assert component.id is not None
    assert component.name == "Sensor de Umidade"

    # Buscar por ID
    component_search = component_repo.get_by_id(component.id)
    assert component_search is not None
    assert component_search.name == "Sensor de Umidade"

    # Atualizar
    component_repo.update(component.id, name="Sensor de Temperatura")
    component_updated = component_repo.get_by_id(component.id)
    assert component_updated.name == "Sensor de Temperatura"

    # Deletar
    component_repo.delete(component.id)
    component_deleted = component_repo.get_by_id(component.id)
    assert component_deleted is None


def test_application_repository(application_repo, crop_repo, producer_repo, session):
    """Testa as operações do repositório de aplicações."""
    # Criar produtor e cultura para teste
    producer = producer_repo.create(
        name="Carlos Silva",
        email="carlos.silva@email.com",
        phone="(11) 93333-3333"
    )
    crop = crop_repo.create(
        name="Milho",
        type="Grão",
        start_date=date(2024, 3, 1),
        producer_id=producer.id
    )

    # Criar aplicação
    application = application_repo.create(
        crop_id=crop.id,
        type="Fertilizante",
        quantity=100.0
    )
    assert application.id is not None
    assert application.type == "Fertilizante"

    # Atualizar
    application_repo.update(application.id, quantity=150.0)
    application_updated = application_repo.get_by_id(application.id)
    assert application_updated.quantity == 150.0

    # Deletar
    application_repo.delete(application.id)
    application_deleted = application_repo.get_by_id(application.id)
    assert application_deleted is None
