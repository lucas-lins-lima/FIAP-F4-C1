from typing import List, Optional, Type
from sqlalchemy.orm import Session
from ..models import Producer

class ProducerRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name: str, email: str, phone: str) -> Producer:
        producer = Producer(
            name=name,
            email=email,
            phone=phone
        )
        self.session.add(producer)
        self.session.commit()
        return producer

    def get_by_id(self, id: str) -> Optional[Producer]:
        return self.session.query(Producer).filter(Producer.id == id).first()

    def get_all(self) -> List[Type[Producer]]:
        return self.session.query(Producer).all()

    def update(self, id: str, **kwargs) -> Optional[Producer]:
        producer = self.get_by_id(id)
        if producer:
            for key, value in kwargs.items():
                if hasattr(producer, key) and key != 'id':
                    setattr(producer, key, value)
            self.session.commit()
        return producer

    def delete(self, id: str) -> bool:
        producer = self.get_by_id(id)
        if producer:
            self.session.delete(producer)
            self.session.commit()
            return True
        return False

    def get_by_email(self, email: str) -> Optional[Producer]:
        return self.session.query(Producer).filter(Producer.email == email).first()

    def get_by_phone(self, phone: str) -> Optional[Producer]:
        return self.session.query(Producer).filter(Producer.phone == phone).first()

    def get_by_name(self, name: str) -> List[Type[Producer]]:
        return self.session.query(Producer).filter(Producer.name.ilike(f"%{name}%")).all()

    def get_crops_by_producer(self, producer_id: str) -> List[dict]:
        producer = self.get_by_id(producer_id)
        if producer and producer.crops:
            return [
                {
                    'id': crop.id,
                    'name': crop.name,
                    'type': crop.type,
                    'start_date': crop.start_date,
                    'end_date': crop.end_date
                } for crop in producer.crops
            ]
        return []
