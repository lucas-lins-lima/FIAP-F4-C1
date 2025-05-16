from typing import List, Optional, Type
from datetime import datetime, date, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import Component, SensorRecord, ClimateData, Producer, Crop, Application

class ComponentRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name: str, type: str, crop_id: Optional[str] = None) -> Component:
        component = Component(name=name, type=type, crop_id=crop_id)
        self.session.add(component)
        self.session.commit()
        return component

    def get_by_id(self, comp_id: str) -> Optional[Component]:
        return self.session.query(Component).filter(Component.id == comp_id).first()

    def get_all(self) -> List[Type[Component]]:
        return self.session.query(Component).all()

    def get_by_type(self, type: str) -> List[Type[Component]]:
        return self.session.query(Component).filter(Component.type == type).all()

    def update(self, id: str, **kwargs) -> Optional[Component]:
        component = self.get_by_id(id)
        if component:
            for key, value in kwargs.items():
                if hasattr(component, key):
                    setattr(component, key, value)
            self.session.commit()
        return component

    def delete(self, comp_id: str) -> bool:
        component = self.get_by_id(comp_id)
        if component:
            self.session.delete(component)
            self.session.commit()
            return True
        return False