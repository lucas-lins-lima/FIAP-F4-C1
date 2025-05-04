from database.oracle import db
from database.models import SensorRecord
from datetime import datetime
from typing import List, Optional

def create_sensor_record(data: dict) -> dict:
   return

def get_sensor_record(sensor_id: str) -> Optional[dict]:
   return

def list_sensor_records() -> List[dict]:
    records = db.session.query(SensorRecord).order_by(SensorRecord.timestamp.desc()).all()
    return [r.to_dict() for r in records]

def update_sensor_record(sensor_id: str, data: dict) -> Optional[dict]:
    return

def delete_sensor_record(sensor_id: str) -> bool:
    return
