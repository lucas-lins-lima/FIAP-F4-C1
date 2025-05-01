from typing import List, Optional

from database.models import Component
from database.oracle import db

def create_component(data: dict) -> dict:
    component = Component(
        name=data['name'],
        type=data['type']
    )
    db.session.add(component)
    db.session.commit()
    db.session.refresh(component)
    return component.to_dict()

def get_component(component_id: str) -> Optional[dict]:
    return

def list_components() -> List[dict]:
    components = db.session.query(Component).all()
    return [component.to_dict() for component in components]

def update_component(component_id: str, data: dict) -> Optional[dict]:
    return

def delete_component(component_id: str) -> bool:
    return
