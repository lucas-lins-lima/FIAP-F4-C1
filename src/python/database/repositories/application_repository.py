from typing import List, Optional, Type
from datetime import datetime, date, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import Component, SensorRecord, ClimateData, Producer, Crop, Application

class ApplicationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, crop_id: str, type: str, quantity: float) -> Application:
        application = Application(crop_id=crop_id, type=type, quantity=quantity, timestamp=datetime.now(timezone.utc))
        self.session.add(application)
        self.session.commit()
        return application

    def get_by_id(self, id: str) -> Optional[Application]:
        return self.session.query(Application).filter(Application.id == id).first()

    def get_all(self) -> List[Type[Application]]:
        return self.session.query(Application).all()

    def get_by_crop(self, crop_id: str) -> List[Type[Application]]:
        return self.session.query(Application).filter(Application.crop_id == crop_id).all()

    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Type[Application]]:
        return self.session.query(Application).filter(Application.timestamp.between(start_date, end_date)).all()

    def get_by_type(self, type: str) -> List[Type[Application]]:
        return self.session.query(Application).filter(Application.type == type).all()

    def update(self, id: str, **kwargs) -> Optional[Application]:
        application = self.get_by_id(id)
        if application:
            for key, value in kwargs.items():
                if hasattr(application, key):
                    setattr(application, key, value)
            self.session.commit()
        return application

    def delete(self, id: str) -> bool:
        application = self.get_by_id(id)
        if application:
            self.session.delete(application)
            self.session.commit()
            return True
        return False

    def get_total_quantity_by_type(self, type: str, start_date: datetime = None, end_date: datetime = None) -> float:
        query = self.session.query(Application).filter(Application.type == type)
        if start_date and end_date:
            query = query.filter(Application.timestamp.between(start_date, end_date))
        return sum(app.quantity for app in query.all())

    def get_crop_application_summary(self, crop_id: str) -> dict:
        applications = self.get_by_crop(crop_id)
        if not applications:
            return {
                'total_applications': 0,
                'types_applied': [],
                'total_quantity': 0
            }
        types = set(app.type for app in applications)
        total_quantity = sum(app.quantity for app in applications)
        return {
            'total_applications': len(applications),
            'types_applied': list(types),
            'total_quantity': total_quantity
        }
