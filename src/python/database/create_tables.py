from sqlalchemy import text
from .oracle import engine
from .models import Base

def create_tables():
    """Cria todas as tabelas definidas nos modelos."""
    try:
        # Cria as tabelas
        Base.metadata.create_all(engine)
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {str(e)}")
        raise

def create_sequences():
    """Cria as sequências necessárias no banco de dados."""
    sequences = [
        'produtor_seq',
        'cultura_seq',
        'sensor_seq',
        'leitura_sensor_seq',
        'aplicacao_seq',
        'sensor_data_seq'
    ]
    
    for seq in sequences:
        try:
            # Tenta criar a sequência
            with engine.connect() as conn:
                conn.execute(text(f"""
                    BEGIN
                        EXECUTE IMMEDIATE 'CREATE SEQUENCE {seq}';
                    EXCEPTION
                        WHEN OTHERS THEN
                            IF SQLCODE = -955 THEN
                                NULL; -- Sequência já existe
                            ELSE
                                RAISE;
                            END IF;
                    END;
                """))
                conn.commit()
            print(f"Sequência {seq} criada ou já existente.")
        except Exception as e:
            print(f"Erro ao criar sequência {seq}: {str(e)}")
            raise

if __name__ == "__main__":
    create_sequences()
    create_tables() 