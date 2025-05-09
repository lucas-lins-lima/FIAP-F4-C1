import pytest
from datetime import datetime, timedelta

from ..database.models.sensor_data import SensorData

def test_create_sensor_data(sensor_repository, sample_sensor_data):
    created_data = sensor_repository.create(sample_sensor_data)
    assert created_data.id is not None
    assert created_data.phosphorus_level == sample_sensor_data.phosphorus_level
    assert created_data.potassium_level == sample_sensor_data.potassium_level
    assert created_data.ph_level == sample_sensor_data.ph_level
    assert created_data.soil_moisture == sample_sensor_data.soil_moisture
    assert created_data.irrigation_active == sample_sensor_data.irrigation_active

def test_get_sensor_data_by_id(sensor_repository, sample_sensor_data):
    created_data = sensor_repository.create(sample_sensor_data)
    retrieved_data = sensor_repository.get_by_id(created_data.id)
    
    assert retrieved_data is not None
    assert retrieved_data.id == created_data.id
    assert retrieved_data.phosphorus_level == created_data.phosphorus_level
    assert retrieved_data.potassium_level == created_data.potassium_level
    assert retrieved_data.ph_level == created_data.ph_level
    assert retrieved_data.soil_moisture == created_data.soil_moisture
    assert retrieved_data.irrigation_active == created_data.irrigation_active

def test_get_all_sensor_data(sensor_repository, sample_sensor_data):
    # Criar múltiplos registros
    for _ in range(3):
        sensor_repository.create(sample_sensor_data)
    
    all_data = sensor_repository.get_all()
    assert len(all_data) == 3
    assert all(isinstance(data, SensorData) for data in all_data)

def test_update_sensor_data(sensor_repository, sample_sensor_data):
    created_data = sensor_repository.create(sample_sensor_data)
    
    # Modificar os dados
    created_data.ph_level = 7.0
    created_data.soil_moisture = 50.0
    created_data.irrigation_active = True
    
    updated_data = sensor_repository.update(created_data)
    assert updated_data is not None
    assert updated_data.id == created_data.id
    assert updated_data.ph_level == 7.0
    assert updated_data.soil_moisture == 50.0
    assert updated_data.irrigation_active is True

def test_delete_sensor_data(sensor_repository, sample_sensor_data):
    created_data = sensor_repository.create(sample_sensor_data)
    assert sensor_repository.delete(created_data.id) is True
    assert sensor_repository.get_by_id(created_data.id) is None

def test_get_by_date_range(sensor_repository, sample_sensor_data):
    # Criar registros com diferentes timestamps
    now = datetime.now()
    for i in range(3):
        data = SensorData(
            timestamp=now - timedelta(hours=i),
            phosphorus_level=True,
            potassium_level=True,
            ph_level=6.5,
            soil_moisture=45.0,
            irrigation_active=False
        )
        sensor_repository.create(data)
    
    # Buscar registros das últimas 2 horas
    start_date = now - timedelta(hours=2)
    end_date = now
    results = sensor_repository.get_by_date_range(start_date, end_date)
    
    assert len(results) == 2
    assert all(start_date <= data.timestamp <= end_date for data in results) 