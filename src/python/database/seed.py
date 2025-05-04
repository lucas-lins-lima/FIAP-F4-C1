from database.oracle import db
from database.models import Component, SensorRecord, ClimateData
from datetime import datetime, timezone, timedelta

components = [
    Component(name='Sensor de Umidade', type='Sensor'),
    Component(name='Atuador da Bomba', type='Actuator'),
    Component(name='Sensor de pH', type='Sensor'),
    Component(name='Controle Central', type='Actuator'),
    Component(name='Relé de Irrigação', type='Actuator'),
    Component(name='Sensor de Nutrientes', type='Sensor'),
    Component(name='Detector de Fósforo', type='Sensor'),
    Component(name='Detector de Potássio', type='Sensor'),
    Component(name='Sensor Ambiental', type='Sensor'),
    Component(name='Atuador de Emergência', type='Actuator')
]

sensors = [
    SensorRecord(soil_moisture=12.0, phosphorus_present=True, potassium_present=True, soil_ph=5.5, irrigation_status='ATIVADA', timestamp=datetime.now(timezone.utc) - timedelta(days=0)),
    SensorRecord(soil_moisture=15.5, phosphorus_present=False, potassium_present=False, soil_ph=6.0, irrigation_status='DESLIGADA', timestamp=datetime.now(timezone.utc) - timedelta(days=1)),
    SensorRecord(soil_moisture=19.0, phosphorus_present=True, potassium_present=False, soil_ph=6.5, irrigation_status='ATIVADA', timestamp=datetime.now(timezone.utc) - timedelta(days=2)),
    SensorRecord(soil_moisture=22.5, phosphorus_present=False, potassium_present=True, soil_ph=7.0, irrigation_status='DESLIGADA', timestamp=datetime.now(timezone.utc) - timedelta(days=3)),
    SensorRecord(soil_moisture=26.0, phosphorus_present=True, potassium_present=False, soil_ph=5.5, irrigation_status='ATIVADA', timestamp=datetime.now(timezone.utc) - timedelta(days=4)),
    SensorRecord(soil_moisture=29.5, phosphorus_present=False, potassium_present=False, soil_ph=6.0, irrigation_status='DESLIGADA', timestamp=datetime.now(timezone.utc) - timedelta(days=5)),
    SensorRecord(soil_moisture=33.0, phosphorus_present=True, potassium_present=True, soil_ph=6.5, irrigation_status='ATIVADA', timestamp=datetime.now(timezone.utc) - timedelta(days=6)),
    SensorRecord(soil_moisture=36.5, phosphorus_present=False, potassium_present=False, soil_ph=7.0, irrigation_status='DESLIGADA', timestamp=datetime.now(timezone.utc) - timedelta(days=7)),
    SensorRecord(soil_moisture=40.0, phosphorus_present=True, potassium_present=True, soil_ph=5.5, irrigation_status='ATIVADA', timestamp=datetime.now(timezone.utc) - timedelta(days=8)),
    SensorRecord(soil_moisture=43.5, phosphorus_present=False, potassium_present=False, soil_ph=6.0, irrigation_status='DESLIGADA', timestamp=datetime.now(timezone.utc) - timedelta(days=9))
]

climas = [
    ClimateData(temperature=20.0, air_humidity=45.0, rain_forecast=True, timestamp=datetime.now(timezone.utc) - timedelta(days=0)),
    ClimateData(temperature=21.8, air_humidity=48.2, rain_forecast=False, timestamp=datetime.now(timezone.utc) - timedelta(days=1)),
    ClimateData(temperature=23.6, air_humidity=51.4, rain_forecast=True, timestamp=datetime.now(timezone.utc) - timedelta(days=2)),
    ClimateData(temperature=25.4, air_humidity=54.6, rain_forecast=False, timestamp=datetime.now(timezone.utc) - timedelta(days=3)),
    ClimateData(temperature=27.2, air_humidity=57.8, rain_forecast=True, timestamp=datetime.now(timezone.utc) - timedelta(days=4)),
    ClimateData(temperature=29.0, air_humidity=61.0, rain_forecast=False, timestamp=datetime.now(timezone.utc) - timedelta(days=5)),
    ClimateData(temperature=30.8, air_humidity=64.2, rain_forecast=True, timestamp=datetime.now(timezone.utc) - timedelta(days=6)),
    ClimateData(temperature=32.6, air_humidity=67.4, rain_forecast=False, timestamp=datetime.now(timezone.utc) - timedelta(days=7)),
    ClimateData(temperature=34.4, air_humidity=70.6, rain_forecast=True, timestamp=datetime.now(timezone.utc) - timedelta(days=8)),
    ClimateData(temperature=36.2, air_humidity=73.8, rain_forecast=False, timestamp=datetime.now(timezone.utc) - timedelta(days=9))
]


def run_seed():
    try:
        with db.session.begin():
            db.session.add_all(components)
            db.session.add_all(sensors)
            db.session.add_all(climas)

        print("✅ Banco populado com sucesso.")
        return

    except Exception as e:
        print(f"❌ Erro ao popular banco de dados: {e}")


if __name__ == "__main__":
    run_seed()