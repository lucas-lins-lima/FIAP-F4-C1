from typing import List, Optional
from datetime import datetime, timedelta

from ..database.models.sensor_data import SensorData
from ..database.repositories.sensor_repository import SensorRepository

class SensorService:
    """Serviço para gerenciar a lógica de negócios dos sensores."""

    def __init__(self, repository: SensorRepository):
        self.repository = repository

    def process_sensor_data(self, sensor_data: SensorData) -> SensorData:
        """Processa os dados dos sensores e determina se a irrigação deve ser ativada."""
        # Lógica para determinar se a irrigação deve ser ativada
        should_irrigate = (
            sensor_data.soil_moisture < 30.0 or  # Umidade muito baixa
            (sensor_data.ph_level < 5.0 or sensor_data.ph_level > 8.0) or  # pH fora do ideal
            not sensor_data.phosphorus_level or  # Falta de fósforo
            not sensor_data.potassium_level  # Falta de potássio
        )
        
        sensor_data.irrigation_active = should_irrigate
        return self.repository.create(sensor_data)

    def get_sensor_data(self, id: int) -> Optional[SensorData]:
        """Obtém dados de um sensor específico."""
        return self.repository.get_by_id(id)

    def get_all_sensor_data(self) -> List[SensorData]:
        """Obtém todos os dados dos sensores."""
        return self.repository.get_all()

    def update_sensor_data(self, sensor_data: SensorData) -> Optional[SensorData]:
        """Atualiza os dados de um sensor."""
        return self.repository.update(sensor_data)

    def delete_sensor_data(self, id: int) -> bool:
        """Remove os dados de um sensor."""
        return self.repository.delete(id)

    def get_sensor_data_by_date_range(self, start_date: datetime, end_date: datetime) -> List[SensorData]:
        """Obtém dados dos sensores dentro de um intervalo de datas."""
        return self.repository.get_by_date_range(start_date, end_date)

    def get_last_24_hours_data(self) -> List[SensorData]:
        """Obtém dados dos sensores das últimas 24 horas."""
        end_date = datetime.now()
        start_date = end_date - timedelta(hours=24)
        return self.get_sensor_data_by_date_range(start_date, end_date)

    def get_sensor_statistics(self, start_date: datetime, end_date: datetime) -> dict:
        """Calcula estatísticas dos dados dos sensores em um período."""
        data = self.get_sensor_data_by_date_range(start_date, end_date)
        
        if not data:
            return {
                'average_ph': 0,
                'average_moisture': 0,
                'irrigation_time_percentage': 0,
                'phosphorus_deficiency_percentage': 0,
                'potassium_deficiency_percentage': 0
            }

        total_records = len(data)
        total_irrigation_time = sum(1 for d in data if d.irrigation_active)
        total_phosphorus_deficiency = sum(1 for d in data if not d.phosphorus_level)
        total_potassium_deficiency = sum(1 for d in data if not d.potassium_level)

        return {
            'average_ph': sum(d.ph_level for d in data) / total_records,
            'average_moisture': sum(d.soil_moisture for d in data) / total_records,
            'irrigation_time_percentage': (total_irrigation_time / total_records) * 100,
            'phosphorus_deficiency_percentage': (total_phosphorus_deficiency / total_records) * 100,
            'potassium_deficiency_percentage': (total_potassium_deficiency / total_records) * 100
        }
