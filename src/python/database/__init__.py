"""
Módulo de banco de dados para o sistema de monitoramento agrícola.
"""
from .models import (
    Produtor,
    Cultura,
    Sensor,
    LeituraSensor,
    Aplicacao,
    SensorData
)
from .repositories import (
    ProdutorRepository,
    CulturaRepository,
    SensorRepository,
    LeituraSensorRepository,
    AplicacaoRepository,
    SensorDataRepository
)
from .oracle import get_session, close_session, engine

__all__ = [
    'Produtor',
    'Cultura',
    'Sensor',
    'LeituraSensor',
    'Aplicacao',
    'SensorData',
    'ProdutorRepository',
    'CulturaRepository',
    'SensorRepository',
    'LeituraSensorRepository',
    'AplicacaoRepository',
    'SensorDataRepository',
    'get_session',
    'close_session',
    'engine'
] 