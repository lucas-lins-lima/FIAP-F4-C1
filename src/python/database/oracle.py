from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from dotenv import load_dotenv
import time
import logging

logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

required_vars = ["ORACLE_USER", "ORACLE_PASSWORD", "ORACLE_HOST", "ORACLE_PORT", "ORACLE_SERVICE"]
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    raise EnvironmentError(f"Erro: Variáveis de ambiente ausentes - {', '.join(missing_vars)}.\nVerifique se o arquivo .env contém todas as configurações necessárias.")

# Configuração da conexão com o banco
ORACLE_USER = os.getenv('ORACLE_USER')
ORACLE_PASSWORD = os.getenv('ORACLE_PASSWORD')
ORACLE_HOST = os.getenv('ORACLE_HOST')
ORACLE_PORT = os.getenv('ORACLE_PORT')
ORACLE_SERVICE = os.getenv('ORACLE_SERVICE')

# String de conexão
DATABASE_URL = f"oracle+oracledb://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}"

# Configurações do engine
ENGINE_CONFIG = {
    'pool_size': 5,
    'max_overflow': 10,
    'pool_timeout': 30,
    'pool_recycle': 1800,  # Recicla conexões a cada 30 minutos
    'pool_pre_ping': True,  # Verifica conexão antes de usar
    'echo': True  # Log de SQL
}

def create_engine_with_retry(max_retries=3, retry_delay=5):
    """Cria o engine com retry logic."""
    for attempt in range(max_retries):
        try:
            logger.info(f"Tentativa {attempt + 1} de {max_retries} para criar engine")
            engine = create_engine(DATABASE_URL, **ENGINE_CONFIG)
            # Testa a conexão
            with engine.connect() as conn:
                conn.execute(text("SELECT 1 FROM DUAL"))
            logger.info("Engine criado com sucesso")
            return engine
        except Exception as e:
            logger.error(f"Erro ao criar engine (tentativa {attempt + 1}): {str(e)}")
            if attempt < max_retries - 1:
                logger.info(f"Aguardando {retry_delay} segundos antes da próxima tentativa...")
                time.sleep(retry_delay)
            else:
                raise

# Cria o engine do SQLAlchemy
engine = create_engine_with_retry()

# Cria a sessão
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

def get_session():
    try:
        session = Session()
        session.execute(text("SELECT 1 FROM DUAL"))
        return session
    except Exception as e:
        logger.error(f"Erro ao obter sessão: {str(e)}")
        Session.remove()  
        raise

def close_session():
    try:
        Session.remove()
    except Exception as e:
        logger.error(f"Erro ao fechar sessão: {str(e)}")

class DB:
    session = Session
    engine = engine

db = DB()
