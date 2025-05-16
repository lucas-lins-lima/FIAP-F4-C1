from database.oracle import db
from database.models import Component, SensorRecord, ClimateData, Application, Producer, Crop
from datetime import datetime, timezone, timedelta
import uuid

# Criando dados dos produtores
producers = [
    Producer(id=str(uuid.uuid4()), name="João Silva", email="joao.silva@email.com", phone="(11) 99999-9999"),
    Producer(id=str(uuid.uuid4()), name="Maria Oliveira", email="maria.oliveira@email.com", phone="(21) 98888-8888")
]

# Criando dados das culturas
crops = [
    Crop(id=str(uuid.uuid4()), name="Milho", type="Grão", start_date=datetime(2024, 1, 1).date(), producer_id=producers[0].id),
    Crop(id=str(uuid.uuid4()), name="Soja", type="Grão", start_date=datetime(2024, 2, 1).date(), producer_id=producers[1].id)
]

# Criando dados dos componentes
components = [
    Component(id=str(uuid.uuid4()), name='Sensor de Umidade', type='Sensor', crop_id=crops[0].id),
    Component(id=str(uuid.uuid4()), name='Atuador da Bomba', type='Actuator', crop_id=crops[0].id),
    Component(id=str(uuid.uuid4()), name='Sensor de pH', type='Sensor', crop_id=crops[1].id),
    Component(id=str(uuid.uuid4()), name='Controle Central', type='Actuator', crop_id=crops[1].id),
    Component(id=str(uuid.uuid4()), name='Relé de Irrigação', type='Actuator', crop_id=crops[0].id),
    Component(id=str(uuid.uuid4()), name='Sensor de Nutrientes', type='Sensor', crop_id=crops[1].id),
    Component(id=str(uuid.uuid4()), name='Detector de Fósforo', type='Sensor', crop_id=crops[0].id),
    Component(id=str(uuid.uuid4()), name='Detector de Potássio', type='Sensor', crop_id=crops[1].id),
    Component(id=str(uuid.uuid4()), name='Sensor Ambiental', type='Sensor', crop_id=crops[0].id),
    Component(id=str(uuid.uuid4()), name='Atuador de Emergência', type='Actuator', crop_id=crops[1].id)
]

# Criando dados dos registros de sensores
sensor_records = [
    SensorRecord(id=str(uuid.uuid4()), sensor_id=components[0].id, soil_moisture=0.12, phosphorus_present=True, potassium_present=True, soil_ph=5.5, irrigation_status="ATIVADA", timestamp=datetime.now(timezone.utc) - timedelta(days=0)),
    SensorRecord(id=str(uuid.uuid4()), sensor_id=components[2].id, soil_moisture=0.15, phosphorus_present=False, potassium_present=False, soil_ph=6.0, irrigation_status="DESLIGADA", timestamp=datetime.now(timezone.utc) - timedelta(days=1)),
    SensorRecord(id=str(uuid.uuid4()), sensor_id=components[0].id, soil_moisture=0.19, phosphorus_present=True, potassium_present=False, soil_ph=6.5, irrigation_status="ATIVADA", timestamp=datetime.now(timezone.utc) - timedelta(days=2)),
    SensorRecord(id=str(uuid.uuid4()), sensor_id=components[2].id, soil_moisture=0.22, phosphorus_present=False, potassium_present=True, soil_ph=7.0, irrigation_status="DESLIGADA", timestamp=datetime.now(timezone.utc) - timedelta(days=3))
]

# Criando dados dos registros climáticos
climate_records = [
    ClimateData(id=str(uuid.uuid4()), temperature=20.0, air_humidity=45.0, rain_forecast=True, timestamp=datetime.now(timezone.utc) - timedelta(days=0)),
    ClimateData(id=str(uuid.uuid4()), temperature=21.8, air_humidity=48.2, rain_forecast=False, timestamp=datetime.now(timezone.utc) - timedelta(days=1)),
    ClimateData(id=str(uuid.uuid4()), temperature=23.6, air_humidity=51.4, rain_forecast=True, timestamp=datetime.now(timezone.utc) - timedelta(days=2)),
    ClimateData(id=str(uuid.uuid4()), temperature=25.4, air_humidity=54.6, rain_forecast=False, timestamp=datetime.now(timezone.utc) - timedelta(days=3))
]

# Criando dados das aplicações
applications = [
    Application(id=str(uuid.uuid4()), crop_id=crops[0].id, timestamp=datetime.now(timezone.utc) - timedelta(days=0), type="Fertilizante", quantity=100.0),
    Application(id=str(uuid.uuid4()), crop_id=crops[1].id, timestamp=datetime.now(timezone.utc) - timedelta(days=1), type="Defensivo", quantity=150.0)
]

def run_seed():
    try:
        with db.session.begin():
            db.session.add_all(producers)
            db.session.add_all(crops)
            db.session.add_all(components)
            db.session.add_all(sensor_records)
            db.session.add_all(climate_records)
            db.session.add_all(applications)

        print("✅ Banco populado com sucesso.")
        return

    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro ao popular banco de dados: {e}")


if __name__ == "__main__":
    run_seed()
