from typing import List, Optional, Type
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from ..models import SensorRecord
from sqlalchemy import func, Float

class SensorRecordRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, sensor_id: str, soil_moisture: float, phosphorus_present: bool, potassium_present: bool, soil_ph: float, irrigation_status: str) -> SensorRecord:
        record = SensorRecord(
            sensor_id=sensor_id,
            soil_moisture=soil_moisture,
            phosphorus_present=phosphorus_present,
            potassium_present=potassium_present,
            soil_ph=soil_ph,
            irrigation_status=irrigation_status,
            timestamp=datetime.now(timezone.utc)
        )
        self.session.add(record)
        self.session.commit()
        return record

    def get_by_id(self, id: str) -> Optional[SensorRecord]:
        return self.session.query(SensorRecord).filter(SensorRecord.id == id).first()

    def get_all(self) -> List[Type[SensorRecord]]:
        return self.session.query(SensorRecord).all()

    def update(self, id: str, **kwargs) -> Optional[SensorRecord]:
        record = self.get_by_id(id)
        if record:
            for key, value in kwargs.items():
                if hasattr(record, key) and key != 'id':
                    setattr(record, key, value)
            self.session.commit()
        return record

    def delete(self, id: str) -> bool:
        record = self.get_by_id(id)
        if record:
            self.session.delete(record)
            self.session.commit()
            return True
        return False

    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Type[SensorRecord]]:
        return self.session.query(SensorRecord).filter(
            SensorRecord.timestamp >= start_date,
            SensorRecord.timestamp <= end_date
        ).all()

    def get_by_sensor(self, sensor_id: str) -> List[Type[SensorRecord]]:
        return self.session.query(SensorRecord).filter(SensorRecord.sensor_id == sensor_id).all()

    def get_latest_by_sensor(self, sensor_id: str) -> Optional[SensorRecord]:
        return self.session.query(SensorRecord).filter(
            SensorRecord.sensor_id == sensor_id
        ).order_by(SensorRecord.timestamp.desc()).first()

    def get_average_values_by_sensor(self, sensor_id: str, start_date: datetime = None, end_date: datetime = None) -> dict:
        query = self.session.query(
            func.avg(SensorRecord.soil_moisture).label('soil_moisture'),
            func.avg(SensorRecord.soil_ph).label('soil_ph'),
            func.avg(SensorRecord.phosphorus_present.cast(Float)).label('phosphorus_present'),
            func.avg(SensorRecord.potassium_present.cast(Float)).label('potassium_present')
        ).filter(SensorRecord.sensor_id == sensor_id)
        if start_date and end_date:
            query = query.filter(SensorRecord.timestamp.between(start_date, end_date))
        result = query.first()
        return {
            'soil_moisture': result.soil_moisture or 0,
            'soil_ph': result.soil_ph or 0,
            'phosphorus_present': result.phosphorus_present or 0,
            'potassium_present': result.potassium_present or 0
        }
