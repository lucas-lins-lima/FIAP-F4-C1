import logging
from tkinter.font import names

from database.setup import create_all_tables, drop_all_tables
from database.utils import print_mer
from logs.logger import config_logger
from services.component_service import list_components, create_component


def main():
    config_logger()
    logger = logging.getLogger(__name__)
    logger.info("Iniciando o sistema...")

    try:
        logger.info("Criando tabelas no banco, se necessário...")
        create_all_tables()

        print_mer()

        logger.info("Conexão com o banco de dados bem-sucedida.")
        logger.info("Tabelas criadas/verificadas com sucesso.")

    except Exception as e:
        logger.exception("Erro ao iniciar o sistema ou conectar ao banco de dados.")
        raise e

    logger.info("Sistema finalizado.")

if __name__ == "__main__":
    main()
