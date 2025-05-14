from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from ..models import SensorData

class SensorDataRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, sensor_data: SensorData) -> SensorData:
        self.session.add(sensor_data)
        self.session.commit()
        return sensor_data

    def get_by_id(self, id: int) -> Optional[SensorData]:
        return self.session.query(SensorData).filter(SensorData.id == id).first()

    def get_all(self) -> List[SensorData]:
        return self.session.query(SensorData).all()

    def update(self, sensor_data: SensorData) -> Optional[SensorData]:
        existing = self.get_by_id(sensor_data.id)
        if existing:
            for key, value in sensor_data.__dict__.items():
                if not key.startswith('_'):
                    setattr(existing, key, value)
            self.session.commit()
            return existing
        return None

    def delete(self, id: int) -> bool:
        sensor_data = self.get_by_id(id)
        if sensor_data:
            self.session.delete(sensor_data)
            self.session.commit()
            return True
        return False

    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[SensorData]:
        return self.session.query(SensorData).filter(
            SensorData.timestamp >= start_date,
            SensorData.timestamp <= end_date
        ).all() 