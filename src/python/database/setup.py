from database.models import Base
from database.oracle import db

import logging

def create_all_tables():
    """
        Cria todas as tabelas do banco de dados definidas no model.
    """
    logger = logging.getLogger(__name__)
    try:
        Base.metadata.create_all(bind=db.engine)
        logger.info("Tabelas criadas com sucesso.")
    except Exception as e:
        logger.exception("Erro ao criar tabelas no banco de dados.")
        raise

def drop_all_tables():
    """
        Dropa todas as tabelas do banco de dados.
    """
    logger = logging.getLogger(__name__)
    try:
        Base.metadata.drop_all(bind=db.engine)
        logger.info("Tabelas removidas com sucesso.")
    except Exception as e:
        logger.exception("Erro ao remover tabelas do banco de dados.")
        raise


if __name__ == "__main__":
    drop_all_tables()
    create_all_tables()