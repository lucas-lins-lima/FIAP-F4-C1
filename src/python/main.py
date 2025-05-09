from datetime import datetime, timedelta
import json
from typing import Dict, Any

from config.database_config import DatabaseConfig
from database.repositories.sensor_repository import SensorRepository
from services.sensor_service import SensorService
from database.models.sensor_data import SensorData

def simulate_sensor_data() -> Dict[str, Any]:
    """Simula dados de sensores para teste."""
    return {
        'timestamp': datetime.now(),
        'phosphorus_level': True,
        'potassium_level': True,
        'ph_level': 6.5,
        'soil_moisture': 45.0,
        'irrigation_active': False
    }

def main():

    config = DatabaseConfig()
    repository = SensorRepository(config)
    service = SensorService(repository)


    print("\n=== Simulando dados dos sensores ===")
    sensor_data = SensorData.from_dict(simulate_sensor_data())
    processed_data = service.process_sensor_data(sensor_data)
    print(f"Dados processados: {json.dumps(processed_data.to_dict(), indent=2, default=str)}")


    print("\n=== Todos os registros ===")
    all_data = service.get_all_sensor_data()
    for data in all_data:
        print(f"Registro: {json.dumps(data.to_dict(), indent=2, default=str)}")

if __name__ == "__main__":
    main()
