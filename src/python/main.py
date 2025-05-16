"""
Ponto de entrada principal da aplicação.
"""
import logging.config

from dotenv import load_dotenv
import time

from database.seed import run_seed
from database.setup import reset_database, drop_all_tables

# Configura logging
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

def main():
    """
    Função principal da aplicação.
    """
    logger.info("Iniciando aplicação...")
    
    # Cria as sequências e tabelas necessárias
    try:
        # Cria e popula o banco de dados
        reset_database()
        run_seed()
        logger.info("✅ Banco de dados inicializado com sucesso. Seeds carregadas")
    except Exception as e:
        logger.error(f"Erro ao criar tabelas: {str(e)}")
        return



if __name__ == "__main__":
    main()
