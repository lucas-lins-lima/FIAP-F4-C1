from typing import List, Optional, Type
from datetime import date
from sqlalchemy.orm import Session
from ..models import Crop

class CropRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name: str, type: str, start_date: date, producer_id: str, end_date: Optional[date] = None) -> Crop:
        crop = Crop(
            name=name,
            type=type,
            start_date=start_date,
            end_date=end_date,
            producer_id=producer_id
        )
        self.session.add(crop)
        self.session.commit()
        return crop

    def get_by_id(self, id: str) -> Optional[Crop]:
        return self.session.query(Crop).filter(Crop.id == id).first()

    def get_all(self) -> List[Type[Crop]]:
        return self.session.query(Crop).all()

    def update(self, id: str, **kwargs) -> Optional[Crop]:
        crop = self.get_by_id(id)
        if crop:
            for key, value in kwargs.items():
                if hasattr(crop, key) and key != 'id':
                    setattr(crop, key, value)
            self.session.commit()
        return crop

    def delete(self, id: str) -> bool:
        crop = self.get_by_id(id)
        if crop:
            self.session.delete(crop)
            self.session.commit()
            return True
        return False

    def get_active_crops(self) -> List[Type[Crop]]:
        return self.session.query(Crop).filter(Crop.end_date.is_(None)).all()

    def get_by_type(self, type: str) -> List[Type[Crop]]:
        return self.session.query(Crop).filter(Crop.type == type).all()

    def get_by_producer(self, producer_id: str) -> List[Type[Crop]]:
        return self.session.query(Crop).filter(Crop.producer_id == producer_id).all()

    def get_crops_with_applications(self) -> List[dict]:
        crops = self.get_all()
        return [
            {
                'id': crop.id,
                'name': crop.name,
                'type': crop.type,
                'start_date': crop.start_date,
                'end_date': crop.end_date,
                'applications': [
                    {
                        'id': app.id,
                        'type': app.type,
                        'quantity': app.quantity,
                        'timestamp': app.timestamp
                    } for app in crop.applications
                ]
            } for crop in crops if crop.applications
        ]