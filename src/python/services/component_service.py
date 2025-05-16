from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from database import ComponentRepository


class ComponentService:
    def __init__(self, session: Session):
        self.repo = ComponentRepository(session)

    def create_component(self, data: dict) -> dict:
        try:
            component = self.repo.create(name=data['name'], type=data['type'], crop_id=data.get('crop_id'))
            return component.__dict__
        except SQLAlchemyError as e:
            self.repo.session.rollback()
            raise e

    def get_component(self, component_id: str) -> Optional[dict]:
        component = self.repo.get_by_id(component_id)
        return component.__dict__ if component else None

    def list_components(self) -> List[dict]:
        return [component.__dict__ for component in self.repo.get_all()]

    def update_component(self, component_id: str, data: dict) -> Optional[dict]:
        try:
            updated_component = self.repo.update(component_id, **data)
            return updated_component.__dict__ if updated_component else None
        except SQLAlchemyError as e:
            self.repo.session.rollback()
            raise e

    def delete_component(self, component_id: str) -> bool:
        try:
            return self.repo.delete(component_id)
        except SQLAlchemyError as e:
            self.repo.session.rollback()
            raise e