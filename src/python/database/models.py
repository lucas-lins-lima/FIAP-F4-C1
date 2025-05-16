import uuid
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Date, Sequence
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone, timedelta

Base = declarative_base()
BRT = timezone(timedelta(hours=-3))

# Tabela que representa o cadastro de sensores e atuadores físicos
class Component(Base):
    __tablename__ = "components"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    type = Column(String(30), nullable=False)  # 'Sensor' ou 'Actuator'
    crop_id = Column(String(36), ForeignKey("crops.id", ondelete="CASCADE"), nullable=True)

    crop = relationship("Crop", back_populates="components")
    records = relationship("SensorRecord", back_populates="sensor", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "crop_id": self.crop_id,
        }

    def __repr__(self):
        return f"<Component(id={self.id}, tipo='{self.type}')>"

# Tabela que armazena os registros de sensores no solo
class SensorRecord(Base):
    __tablename__ = "sensor_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sensor_id = Column(String(36), ForeignKey("components.id", ondelete="CASCADE"), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=lambda: datetime.now(BRT))
    soil_moisture = Column(Float, nullable=False)
    phosphorus_present = Column(Boolean, nullable=False)
    potassium_present = Column(Boolean, nullable=False)
    soil_ph = Column(Float, nullable=False)
    irrigation_status = Column(String(10), nullable=False, default="DESLIGADA")

    sensor = relationship("Component", back_populates="records")

    def __repr__(self):
        return f"<SensorRecord(id={self.id}, moisture={self.soil_moisture}, ph={self.soil_ph})>"

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "soil_moisture": self.soil_moisture,
            "phosphorus_present": self.phosphorus_present,
            "potassium_present": self.potassium_present,
            "soil_ph": self.soil_ph,
            "irrigation_status": self.irrigation_status,
            "sensor_id": self.sensor_id
        }

    @classmethod
    def from_dict(cls, data_dict):
        if 'timestamp' in data_dict and isinstance(data_dict['timestamp'], str):
            data_dict['timestamp'] = datetime.fromisoformat(data_dict['timestamp'])
        return cls(**data_dict)

# Tabela que armazena os dados meteorológicos obtidos de API externa
class ClimateData(Base):
    __tablename__ = "climate_data"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, nullable=False, default=lambda: datetime.now(BRT))
    temperature = Column(Float, nullable=False)
    air_humidity = Column(Float, nullable=False)
    rain_forecast = Column(Boolean, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "temperature": self.temperature,
            "air_humidity": self.air_humidity,
            "rain_forecast": self.rain_forecast,
        }

# Tabela que armazena os dados dos produtores
class Producer(Base):
    __tablename__ = 'producers'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    phone = Column(String(30), nullable=False)

    crops = relationship("Crop", back_populates="producer", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Producer(id={self.id}, name='{self.name}')>"

# Tabela que armazena os dados das culturas
class Crop(Base):
    __tablename__ = 'crops'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    producer_id = Column(String(36), ForeignKey('producers.id', ondelete="CASCADE"), nullable=False)

    producer = relationship("Producer", back_populates="crops")
    components = relationship("Component", back_populates="crop", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="crop", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Crop(id={self.id}, name='{self.name}')>"

# Tabela que armazena os dados de aplicação de insumos, como fertilizantes, defensivos, etc.
class Application(Base):
    __tablename__ = 'applications'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    crop_id = Column(String(36), ForeignKey('crops.id', ondelete="CASCADE"), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=lambda: datetime.now(BRT))
    type = Column(String(50), nullable=False)
    quantity = Column(Float, nullable=False)

    crop = relationship("Crop", back_populates="applications")

    def __repr__(self):
        return f"<Application(id={self.id}, crop={self.crop_id}, type='{self.type}')>"
