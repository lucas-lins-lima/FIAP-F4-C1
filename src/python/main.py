
from database.setup import create_all_tables, drop_all_tables
from database.utils import print_mer
from logs.logger import Logger
from services.weather_service import run_weather_integration

logger = Logger(__name__)()


def main():
    logger.info("Iniciando o sistema...")

    try:
        logger.info("Criando tabelas no banco, se necessário...")
        # create_all_tables()

        run_weather_integration()

        # print_mer()

        logger.info("Conexão com o banco de dados bem-sucedida.")
        logger.info("Tabelas criadas/verificadas com sucesso.")

    except Exception as e:
        logger.exception("Erro ao iniciar o sistema ou conectar ao banco de dados.")
        raise e

    logger.info("Sistema finalizado.")

if __name__ == "__main__":
    main()
