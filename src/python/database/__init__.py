"""
Módulo de banco de dados para o sistema de monitoramento agrícola.
"""
from .models import (
    Component,
    SensorRecord,
    ClimateData,
    Producer,
    Crop,
    Application
)
from .repositories import (
    ProducerRepository,
    CropRepository,
    ComponentRepository,
    SensorRecordRepository,
    ApplicationRepository,
    ClimateDataRepository
)
from .oracle import get_session, close_session, engine

__all__ = [
    'Component',
    'SensorRecord',
    'ClimateData',
    'Producer',
    'Crop',
    'Application',
    'ProducerRepository',
    'CropRepository',
    'ComponentRepository',
    'SensorRecordRepository',
    'ApplicationRepository',
    'ClimateDataRepository',
    'get_session',
    'close_session',
    'engine'
]