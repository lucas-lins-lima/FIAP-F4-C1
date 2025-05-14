from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
import os
from dotenv import load_dotenv

from .models import Base, Produtor, Cultura, Sensor, LeituraSensor, Aplicacao

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da conexão com o banco
DB_USER = os.getenv('DB_USER', 'system')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'oracle')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', '1521'))  # Convertendo para inteiro
DB_SERVICE = os.getenv('DB_SERVICE', 'XE')

# String de conexão
DATABASE_URL = f"oracle+cx_oracle://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/?service_name={DB_SERVICE}"

def create_sequences(engine):
    sequences = [
        "CREATE SEQUENCE produtor_seq START WITH 1 INCREMENT BY 1",
        "CREATE SEQUENCE cultura_seq START WITH 1 INCREMENT BY 1",
        "CREATE SEQUENCE sensor_seq START WITH 1 INCREMENT BY 1",
        "CREATE SEQUENCE leitura_sensor_seq START WITH 1 INCREMENT BY 1",
        "CREATE SEQUENCE aplicacao_seq START WITH 1 INCREMENT BY 1"
    ]
    
    with engine.connect() as connection:
        for seq in sequences:
            try:
                connection.execute(text(seq))
                connection.commit()
            except Exception as e:
                print(f"Erro ao criar sequência: {e}")
                # Se a sequência já existe, continua
                continue

def init_db():
    """Inicializa o banco de dados criando todas as tabelas."""
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    
    # Cria uma sessão para inserir dados de exemplo
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Verifica se já existem dados
        if session.query(Produtor).first():
            print("Banco de dados já populado.")
            return
        
        # Cria um produtor de exemplo
        produtor = Produtor(
            nome="João Silva",
            email="joao.silva@email.com",
            telefone="(11) 99999-9999"
        )
        session.add(produtor)
        session.commit()
        
        # Cria uma cultura de exemplo
        cultura = Cultura(
            nome="Milho",
            tipo="grão",
            data_inicio=date(2024, 1, 1),
            id_produtor=produtor.id_produtor
        )
        session.add(cultura)
        session.commit()
        
        # Cria sensores de exemplo
        sensores = [
            Sensor(
                tipo="umidade",
                modelo="DHT22",
                localizacao="Setor A",
                id_cultura=cultura.id_cultura
            ),
            Sensor(
                tipo="ph",
                modelo="pH-2000",
                localizacao="Setor B",
                id_cultura=cultura.id_cultura
            )
        ]
        session.add_all(sensores)
        session.commit()
        
        # Cria leituras de exemplo
        for sensor in sensores:
            leitura = LeituraSensor(
                id_sensor=sensor.id_sensor,
                valor_umidade=65.5 if sensor.tipo == "umidade" else None,
                valor_ph=6.5 if sensor.tipo == "ph" else None,
                valor_npk_fosforo=45.0 if sensor.tipo == "ph" else None,
                valor_npk_potassio=35.0 if sensor.tipo == "ph" else None
            )
            session.add(leitura)
        
        # Cria aplicações de exemplo
        aplicacao = Aplicacao(
            id_cultura=cultura.id_cultura,
            tipo="irrigação",
            quantidade=100.0
        )
        session.add(aplicacao)
        
        session.commit()
        print("Banco de dados populado com sucesso!")
        
    except Exception as e:
        session.rollback()
        print(f"Erro ao popular banco de dados: {str(e)}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    init_db()
