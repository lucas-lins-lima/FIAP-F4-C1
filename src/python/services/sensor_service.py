from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from database import SensorRecordRepository


class SensorRecordService:
    def __init__(self, session: Session):
        self.repo = SensorRecordRepository(session)

    def create_sensor_record(self, data: dict) -> dict:
        try:
            record = self.repo.create(
                sensor_id=data['sensor_id'],
                soil_moisture=data['soil_moisture'],
                phosphorus_present=data['phosphorus_present'],
                potassium_present=data['potassium_present'],
                soil_ph=data['soil_ph'],
                irrigation_status=data.get('irrigation_status', 'DESLIGADA')
            )
            record = self._process_irrigation_logic(record)
            return record.__dict__
        except SQLAlchemyError as e:
            self.repo.session.rollback()
            raise e

    def get_sensor_record(self, record_id: str) -> Optional[dict]:
        record = self.repo.get_by_id(record_id)
        return record.__dict__ if record else None

    def list_sensor_records(self) -> List[dict]:
        return [record.__dict__ for record in self.repo.get_all()]

    def update_sensor_record(self, record_id: str, data: dict) -> Optional[dict]:
        try:
            updated_record = self.repo.update(record_id, **data)
            if updated_record:
                updated_record = self._process_irrigation_logic(updated_record)
            return updated_record.__dict__ if updated_record else None
        except SQLAlchemyError as e:
            self.repo.session.rollback()
            raise e

    def delete_sensor_record(self, record_id: str) -> bool:
        try:
            return self.repo.delete(record_id)
        except SQLAlchemyError as e:
            self.repo.session.rollback()
            raise e

    def list_records_by_sensor(self, sensor_id: str) -> List[dict]:
        return [record.__dict__ for record in self.repo.get_by_sensor(sensor_id)]

    def get_latest_record_by_sensor(self, sensor_id: str) -> Optional[dict]:
        record = self.repo.get_latest_by_sensor(sensor_id)
        return record.__dict__ if record else None

    def get_average_values_by_sensor(self, sensor_id: str) -> dict:
        return self.repo.get_average_values_by_sensor(sensor_id)

    def _process_irrigation_logic(self, record) -> SensorRecordRepository:
        should_irrigate = (
            record.soil_moisture < 30.0 or  # Umidade muito baixa
            record.soil_ph < 5.0 or record.soil_ph > 8.0 or  # pH fora do ideal
            not record.phosphorus_present or  # Falta de fósforo
            not record.potassium_present  # Falta de potássio
        )
        record.irrigation_status = "ATIVADA" if should_irrigate else "DESLIGADA"
        self.repo.session.commit()
        return record
