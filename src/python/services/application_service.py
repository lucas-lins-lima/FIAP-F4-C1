from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from database import ApplicationRepository


class ApplicationService:
    def __init__(self, session: Session):
        self.repo = ApplicationRepository(session)

    def create_application(self, data: dict) -> dict:
        try:
            application = self.repo.create(
                crop_id=data['crop_id'],
                type=data['type'],
                quantity=data['quantity'],
                timestamp=datetime.now()
            )
            return application.__dict__
        except SQLAlchemyError as e:
            self.repo.session.rollback()
            raise e

    def get_application(self, application_id: str) -> Optional[dict]:
        application = self.repo.get_by_id(application_id)
        return application.__dict__ if application else None

    def list_applications(self) -> List[dict]:
        return [application.__dict__ for application in self.repo.get_all()]

    def update_application(self, application_id: str, data: dict) -> Optional[dict]:
        try:
            updated_application = self.repo.update(application_id, **data)
            return updated_application.__dict__ if updated_application else None
        except SQLAlchemyError as e:
            self.repo.session.rollback()
            raise e

    def delete_application(self, application_id: str) -> bool:
        try:
            return self.repo.delete(application_id)
        except SQLAlchemyError as e:
            self.repo.session.rollback()
            raise e

    def get_applications_by_crop(self, crop_id: str) -> List[dict]:
        return [application.__dict__ for application in self.repo.get_by_crop(crop_id)]

    def get_total_quantity_by_type(self, crop_id: str, app_type: str) -> float:
        applications = self.repo.get_by_crop(crop_id)
        return sum(app.quantity for app in applications if app.type == app_type)

    def get_application_summary(self, crop_id: str) -> dict:
        applications = self.repo.get_by_crop(crop_id)
        total_quantity = sum(app.quantity for app in applications)
        types = list(set(app.type for app in applications))
        return {
            'total_applications': len(applications),
            'types_applied': types,
            'total_quantity': total_quantity
        }
