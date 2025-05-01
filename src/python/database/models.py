import uuid
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Tabela que representa o cadastro de sensores e atuadores físicos
class Component(Base):
    __tablename__ = "components"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)  # Nome do componente
    type = Column(String(30), nullable=False)  # 'Sensor' ou 'Actuator'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
        }


# Tabela que armazena os registros de sensores no solo
class SensorRecord(Base):
    __tablename__ = "sensor_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)  # Momento da coleta
    soil_moisture = Column(Float, nullable=False)  # Umidade do solo (%)
    phosphorus_present = Column(Boolean, nullable=False)  # Presença de fósforo
    potassium_present = Column(Boolean, nullable=False)  # Presença de potássio
    soil_ph = Column(Float, nullable=False)  # Valor de pH do solo
    irrigation_status = Column(String(10), nullable=False)  # Status da irrigação (ATIVADA / DESLIGADA)

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "soil_moisture": self.soil_moisture,
            "phosphorus_present": self.phosphorus_present,
            "potassium_present": self.potassium_present,
            "soil_ph": self.soil_ph,
            "irrigation_status": self.irrigation_status,
            "component_id": self.component_id,
        }


# Tabela que armazena os dados meteorológicos obtidos de API externa
class ClimateData(Base):
    __tablename__ = "climate_data"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, nullable=False, default=datetime)  # Momento da coleta dos dados climáticos
    temperature = Column(Float, nullable=False)  # Temperatura ambiente (°C)
    air_humidity = Column(Float, nullable=False)  # Umidade do ar (%)
    rain_forecast = Column(Boolean, nullable=False)  # Previsão de chuva (True/False)

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "temperature": self.temperature,
            "air_humidity": self.air_humidity,
            "rain_forecast": self.rain_forecast,
        }
