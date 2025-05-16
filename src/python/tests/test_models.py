import pytest
from datetime import datetime
from database.models import SensorRecord

def test_sensor_record_creation():
    timestamp = datetime.now()
    sensor_record = SensorRecord(
        sensor_id="123e4567-e89b-12d3-a456-426614174000",
        soil_moisture=45.0,
        soil_ph=6.5,
        phosphorus_present=True,
        potassium_present=False,
        irrigation_status="ATIVADA",
        timestamp=timestamp
    )

    assert sensor_record.sensor_id == "123e4567-e89b-12d3-a456-426614174000"
    assert sensor_record.soil_moisture == 45.0
    assert sensor_record.soil_ph == 6.5
    assert sensor_record.phosphorus_present is True
    assert sensor_record.potassium_present is False
    assert sensor_record.irrigation_status == "ATIVADA"
    assert sensor_record.timestamp == timestamp

def test_sensor_record_repr():
    sensor_record = SensorRecord(
        sensor_id="123e4567-e89b-12d3-a456-426614174000",
        soil_moisture=45.0,
        soil_ph=6.5,
        phosphorus_present=True,
        potassium_present=False,
        irrigation_status="ATIVADA"
    )

    expected_repr = f"<SensorRecord(id={sensor_record.id}, moisture=45.0, ph=6.5)>"
    assert repr(sensor_record) == expected_repr

def test_sensor_record_to_dict():
    timestamp = datetime.now()
    sensor_record = SensorRecord(
        sensor_id="123e4567-e89b-12d3-a456-426614174000",
        timestamp=timestamp,
        phosphorus_present=True,
        potassium_present=False,
        soil_ph=6.5,
        soil_moisture=45.0,
        irrigation_status="ATIVADA"
    )

    data_dict = sensor_record.to_dict()
    assert data_dict['sensor_id'] == "123e4567-e89b-12d3-a456-426614174000"
    assert data_dict['timestamp'] == timestamp.isoformat()
    assert data_dict['phosphorus_present'] is True
    assert data_dict['potassium_present'] is False
    assert data_dict['soil_ph'] == 6.5
    assert data_dict['soil_moisture'] == 45.0
    assert data_dict['irrigation_status'] == "ATIVADA"

def test_sensor_record_from_dict():
    timestamp = datetime.now()
    data_dict = {
        'sensor_id': "123e4567-e89b-12d3-a456-426614174000",
        'timestamp': timestamp.isoformat(),
        'phosphorus_present': True,
        'potassium_present': False,
        'soil_ph': 6.5,
        'soil_moisture': 45.0,
        'irrigation_status': "ATIVADA"
    }

    sensor_record = SensorRecord.from_dict(data_dict)
    assert sensor_record.sensor_id == "123e4567-e89b-12d3-a456-426614174000"
    assert isinstance(sensor_record.timestamp, datetime)
    assert sensor_record.phosphorus_present is True
    assert sensor_record.potassium_present is False
    assert sensor_record.soil_ph == 6.5
    assert sensor_record.soil_moisture == 45.0
    assert sensor_record.irrigation_status == "ATIVADA"
