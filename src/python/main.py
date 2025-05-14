"""
Ponto de entrada principal da aplicação.
"""

import logging
import logging.config
from datetime import datetime
import json
import os
from dotenv import load_dotenv
import time

from config.settings import LOG_CONFIG
from services.sensor_service import SensorService
from services.irrigation_service import IrrigationService
from database.create_tables import create_tables, create_sequences
from database.repositories import SensorRepository, CulturaRepository, ProdutorRepository
from database import get_session, close_session

# Configura logging
logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

def criar_dados_iniciais():
    """Cria os dados iniciais necessários para o funcionamento da aplicação."""
    max_retries = 3
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Tentativa {attempt + 1} de {max_retries} para criar dados iniciais")
            session = get_session()
            
            # Cria um produtor
            produtor_repo = ProdutorRepository(session)
            produtor = produtor_repo.create(
                nome="Produtor Teste",
                email="produtor@teste.com",
                telefone="(11) 99999-9999"
            )
            logger.info(f"Produtor criado com ID: {produtor.id_produtor}")
            
            # Cria uma cultura
            cultura_repo = CulturaRepository(session)
            cultura = cultura_repo.create(
                nome="Soja",
                tipo="Grão",
                data_inicio=datetime.now(),
                id_produtor=produtor.id_produtor
            )
            logger.info(f"Cultura criada com ID: {cultura.id_cultura}")
            
            # Cria um sensor
            sensor_repo = SensorRepository(session)
            sensor = sensor_repo.create(
                tipo="Umidade",
                modelo="Sensor-X1",
                localizacao="Campo 1",
                id_cultura=cultura.id_cultura
            )
            logger.info(f"Sensor criado com ID: {sensor.id_sensor}")
            
            session.commit()
            return sensor.id_sensor
            
        except Exception as e:
            logger.error(f"Erro ao criar dados iniciais (tentativa {attempt + 1}): {str(e)}")
            if session:
                session.rollback()
            if attempt < max_retries - 1:
                logger.info(f"Aguardando {retry_delay} segundos antes da próxima tentativa...")
                time.sleep(retry_delay)
            else:
                return None
        finally:
            if session:
                close_session()
    
    return None

def processar_dados_sensor(dados_json: str) -> dict:
    """
    Processa dados recebidos do sensor.
    
    Args:
        dados_json: String JSON com os dados do sensor
        
    Returns:
        Dict com o resultado do processamento
    """
    try:
        # Converte JSON para dict
        dados = json.loads(dados_json)
        
        # Valida dados obrigatórios
        if 'id_sensor' not in dados:
            raise ValueError("ID do sensor não fornecido")
            
        # Processa leitura
        sensor_service = SensorService()
        resultado = sensor_service.processar_leitura(
            id_sensor=dados['id_sensor'],
            dados=dados
        )
        
        if resultado:
            # Verifica necessidade de irrigação
            irrigation_service = IrrigationService()
            status_irrigacao = irrigation_service.verificar_irrigacao(dados['id_sensor'])
            
            return {
                'status': 'sucesso',
                'leitura': resultado,
                'irrigacao': status_irrigacao
            }
        else:
            return {
                'status': 'erro',
                'mensagem': 'Falha ao processar leitura'
            }
            
    except json.JSONDecodeError:
        logger.error("Erro ao decodificar JSON")
        return {
            'status': 'erro',
            'mensagem': 'JSON inválido'
        }
    except Exception as e:
        logger.error(f"Erro ao processar dados: {str(e)}")
        return {
            'status': 'erro',
            'mensagem': str(e)
        }

def main():
    """
    Função principal da aplicação.
    """
    logger.info("Iniciando aplicação...")
    
    # Cria as sequências e tabelas necessárias
    try:
        create_sequences()
        create_tables()
    except Exception as e:
        logger.error(f"Erro ao criar tabelas: {str(e)}")
        return
    
    # Cria dados iniciais
    id_sensor = criar_dados_iniciais()
    if not id_sensor:
        logger.error("Falha ao criar dados iniciais")
        return
    
    # Exemplo de uso
    dados_exemplo = {
        'id_sensor': id_sensor,
        'umidade': 25.5,
        'ph': 6.8,
        'fosforo': 15.0,
        'potassio': 20.0
    }
    
    resultado = processar_dados_sensor(json.dumps(dados_exemplo))
    print(json.dumps(resultado, indent=2))

if __name__ == "__main__":
    main()
