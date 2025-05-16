from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, date

from database import ProducerRepository


class ProducerService:
    def __init__(self, session: Session):
        self.repo = ProducerRepository(session)

    def create_producer(self, data: dict) -> dict:
        try:
            producer = self.repo.create(
                name=data['name'],
                email=data['email'],
                phone=data['phone']
            )
            return producer.__dict__
        except SQLAlchemyError as e:
            self.repo.session.rollback()
            raise e

    def get_producer(self, producer_id: str) -> Optional[dict]:
        producer = self.repo.get_by_id(producer_id)
        return producer.__dict__ if producer else None

    def list_producers(self) -> List[dict]:
        return [producer.__dict__ for producer in self.repo.get_all()]

    def update_producer(self, producer_id: str, data: dict) -> Optional[dict]:
        try:
            updated_producer = self.repo.update(producer_id, **data)
            return updated_producer.__dict__ if updated_producer else None
        except SQLAlchemyError as e:
            self.repo.session.rollback()
            raise e

    def delete_producer(self, producer_id: str) -> bool:
        try:
            return self.repo.delete(producer_id)
        except SQLAlchemyError as e:
            self.repo.session.rollback()
            raise e

    def get_producer_crops(self, producer_id: str) -> List[dict]:
        return self.repo.get_crops_by_producer(producer_id)