from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import date

from database import CropRepository


class CropService:
    def __init__(self, session: Session):
        self.repo = CropRepository(session)

    def create_crop(self, data: dict) -> dict:
        try:
            crop = self.repo.create(
                name=data['name'],
                type=data['type'],
                start_date=date.fromisoformat(data['start_date']),
                end_date=date.fromisoformat(data.get('end_date')) if data.get('end_date') else None,
                producer_id=data['producer_id']
            )
            return crop.__dict__
        except SQLAlchemyError as e:
            self.repo.session.rollback()
            raise e

    def get_crop(self, crop_id: str) -> Optional[dict]:
        crop = self.repo.get_by_id(crop_id)
        return crop.__dict__ if crop else None

    def list_crops(self) -> List[dict]:
        return [crop.__dict__ for crop in self.repo.get_all()]

    def update_crop(self, crop_id: str, data: dict) -> Optional[dict]:
        try:
            updated_crop = self.repo.update(crop_id, **data)
            return updated_crop.__dict__ if updated_crop else None
        except SQLAlchemyError as e:
            self.repo.session.rollback()
            raise e

    def delete_crop(self, crop_id: str) -> bool:
        try:
            return self.repo.delete(crop_id)
        except SQLAlchemyError as e:
            self.repo.session.rollback()
            raise e

    def list_active_crops(self) -> List[dict]:
        return [crop.__dict__ for crop in self.repo.get_active_crops()]

    def get_crops_by_producer(self, producer_id: str) -> List[dict]:
        return self.repo.get_by_producer(producer_id)

    def get_crop_components(self, crop_id: str) -> List[dict]:
        crop = self.repo.get_by_id(crop_id)
        if not crop:
            return []
        return [component.__dict__ for component in crop.components]

    def get_crop_applications(self, crop_id: str) -> List[dict]:
        crop = self.repo.get_by_id(crop_id)
        if not crop:
            return []
        return [application.__dict__ for application in crop.applications]

    def get_crop_details(self, crop_id: str) -> Optional[dict]:
        crop = self.repo.get_by_id(crop_id)
        if not crop:
            return None
        return {
            **crop.__dict__,
            "components": self.get_crop_components(crop_id),
            "applications": self.get_crop_applications(crop_id)
        }
