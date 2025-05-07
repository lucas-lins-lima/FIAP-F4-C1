from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

from ..models.sensor_data import SensorData
from ...config.database_config import DatabaseConfig

class SensorRepository:
    """Repositório para operações com dados dos sensores no banco de dados."""

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._create_table_if_not_exists()

    def _get_connection(self):
        """Estabelece conexão com o banco de dados."""
        return psycopg2.connect(self.config.connection_string)

    def _create_table_if_not_exists(self):
        """Cria a tabela de sensores se ela não existir."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS sensor_data (
                        id SERIAL PRIMARY KEY,
                        timestamp TIMESTAMP NOT NULL,
                        phosphorus_level BOOLEAN NOT NULL,
                        potassium_level BOOLEAN NOT NULL,
                        ph_level FLOAT NOT NULL,
                        soil_moisture FLOAT NOT NULL,
                        irrigation_active BOOLEAN NOT NULL
                    )
                """)
                conn.commit()

    def create(self, sensor_data: SensorData) -> SensorData:
        """Insere um novo registro de dados dos sensores."""
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    INSERT INTO sensor_data 
                    (timestamp, phosphorus_level, potassium_level, ph_level, soil_moisture, irrigation_active)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING *
                """, (
                    sensor_data.timestamp,
                    sensor_data.phosphorus_level,
                    sensor_data.potassium_level,
                    sensor_data.ph_level,
                    sensor_data.soil_moisture,
                    sensor_data.irrigation_active
                ))
                result = cur.fetchone()
                conn.commit()
                return SensorData.from_dict(dict(result))

    def get_by_id(self, id: int) -> Optional[SensorData]:
        """Busca um registro pelo ID."""
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM sensor_data WHERE id = %s", (id,))
                result = cur.fetchone()
                return SensorData.from_dict(dict(result)) if result else None

    def get_all(self) -> List[SensorData]:
        """Retorna todos os registros."""
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC")
                results = cur.fetchall()
                return [SensorData.from_dict(dict(row)) for row in results]

    def update(self, sensor_data: SensorData) -> Optional[SensorData]:
        """Atualiza um registro existente."""
        if not sensor_data.id:
            return None

        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    UPDATE sensor_data
                    SET timestamp = %s,
                        phosphorus_level = %s,
                        potassium_level = %s,
                        ph_level = %s,
                        soil_moisture = %s,
                        irrigation_active = %s
                    WHERE id = %s
                    RETURNING *
                """, (
                    sensor_data.timestamp,
                    sensor_data.phosphorus_level,
                    sensor_data.potassium_level,
                    sensor_data.ph_level,
                    sensor_data.soil_moisture,
                    sensor_data.irrigation_active,
                    sensor_data.id
                ))
                result = cur.fetchone()
                conn.commit()
                return SensorData.from_dict(dict(result)) if result else None

    def delete(self, id: int) -> bool:
        """Remove um registro pelo ID."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM sensor_data WHERE id = %s", (id,))
                conn.commit()
                return cur.rowcount > 0

    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[SensorData]:
        """Busca registros dentro de um intervalo de datas."""
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM sensor_data 
                    WHERE timestamp BETWEEN %s AND %s 
                    ORDER BY timestamp DESC
                """, (start_date, end_date))
                results = cur.fetchall()
                return [SensorData.from_dict(dict(row)) for row in results] 