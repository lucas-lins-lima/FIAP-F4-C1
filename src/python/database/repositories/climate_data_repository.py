from typing import List, Optional, Type
from sqlalchemy.orm import Session
from sqlalchemy import func, Float
from datetime import datetime, timezone
from ..models import ClimateData

class ClimateDataRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, temperature: float, air_humidity: float, rain_forecast: bool) -> ClimateData:
        data = ClimateData(
            temperature=temperature,
            air_humidity=air_humidity,
            rain_forecast=rain_forecast,
            timestamp=datetime.now(timezone.utc)
        )
        self.session.add(data)
        self.session.commit()
        return data

    def get_by_id(self, id: str) -> Optional[ClimateData]:
        return self.session.query(ClimateData).filter(ClimateData.id == id).first()

    def get_all(self) -> List[Type[ClimateData]]:
        return self.session.query(ClimateData).all()

    def update(self, id: str, **kwargs) -> Optional[ClimateData]:
        data = self.get_by_id(id)
        if data:
            for key, value in kwargs.items():
                if hasattr(data, key) and key != 'id':
                    setattr(data, key, value)
            self.session.commit()
        return data

    def delete(self, id: str) -> bool:
        data = self.get_by_id(id)
        if data:
            self.session.delete(data)
            self.session.commit()
            return True
        return False

    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Type[ClimateData]]:
        return self.session.query(ClimateData).filter(
            ClimateData.timestamp >= start_date,
            ClimateData.timestamp <= end_date
        ).all()

    def get_latest(self) -> Optional[ClimateData]:
        return self.session.query(ClimateData).order_by(ClimateData.timestamp.desc()).first()

    def get_average_values(self, start_date: datetime = None, end_date: datetime = None) -> dict:
        query = self.session.query(
            func.avg(ClimateData.temperature).label('temperature'),
            func.avg(ClimateData.air_humidity).label('air_humidity'),
            func.avg(ClimateData.rain_forecast.cast(Float)).label('rain_forecast')
        )
        if start_date and end_date:
            query = query.filter(ClimateData.timestamp.between(start_date, end_date))
        result = query.first()
        return {
            'temperature': result.temperature or 0,
            'air_humidity': result.air_humidity or 0,
            'rain_forecast': result.rain_forecast or 0
        }
