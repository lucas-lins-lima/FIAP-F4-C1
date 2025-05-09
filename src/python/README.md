# Entrega 2: Armazenamento de Dados em Banco SQL com Python

Este projeto implementa a camada de armazenamento e análise de dados do sistema de irrigação inteligente, focando na captura de dados do ESP32 e seu armazenamento em banco de dados SQL.

## Metas da Entrega

1. **Captura de Dados**
   - Implementar a leitura dos dados do monitor serial do ESP32
   - Processar e validar os dados recebidos
   - Simular a comunicação serial em ambiente de desenvolvimento

2. **Armazenamento em Banco SQL**
   - Criar script Python para simulação do armazenamento
   - Implementar estrutura de banco de dados relacional
   - Garantir integridade e consistência dos dados

3. **Operações CRUD**
   - Implementar operações de inserção (Create)
   - Implementar operações de consulta (Read)
   - Implementar operações de atualização (Update)
   - Implementar operações de remoção (Delete)

4. **Documentação e Justificativa**
   - Relacionar a estrutura de dados com o MER da Fase 2
   - Justificar as escolhas de implementação
   - Documentar as operações CRUD implementadas

## Entregáveis

### 1. Script Python Funcional

O script principal (`main.py`) implementa:
- Leitura de dados do ESP32
- Processamento e validação
- Armazenamento em banco SQL
- Operações CRUD básicas

### 2. Tabelas de Exemplo

#### sensor_records
```sql
CREATE TABLE sensor_records (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    soil_moisture FLOAT NOT NULL,
    ph_level FLOAT NOT NULL,
    phosphorus_level BOOLEAN NOT NULL,
    potassium_level BOOLEAN NOT NULL,
    irrigation_active BOOLEAN NOT NULL
);
```

#### climate_data
```sql
CREATE TABLE climate_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    temperature FLOAT NOT NULL,
    air_humidity FLOAT NOT NULL,
    precipitation FLOAT NOT NULL
);
```

### 3. Relação com MER da Fase 2

A estrutura do banco de dados foi projetada seguindo o MER desenvolvido na Fase 2, com as seguintes considerações:

- **Entidades Principais**:
  - Sensor Records: Armazena leituras dos sensores
  - Climate Data: Armazena dados meteorológicos

- **Relacionamentos**:
  - One-to-Many entre Climate Data e Sensor Records
  - Timestamps para rastreamento temporal

- **Adaptações Práticas**:
  - Adição de índices para otimização
  - Campos de auditoria (created_at, updated_at)
  - Validações de integridade

## Como Executar

1. **Configuração do Ambiente**
   ```bash
   cd src/python
   pip install -r requirements.txt
   ```

2. **Configuração do Banco**
   - Crie um arquivo `.env` na pasta `src/python` com as seguintes variáveis:
   ```bash
   ORACLE_USER=seu_usuario
   ORACLE_PASSWORD=sua_senha
   ORACLE_HOST=localhost
   ORACLE_PORT=1521
   ORACLE_SERVICE=XE
   ```
   - Execute o script de inicialização do banco:
   ```bash
   cd src/python
   python database/setup.py
   ```
   Este script irá:
   - Criar todas as tabelas necessárias
   - Inicializar o banco com dados de exemplo
   - Configurar as conexões necessárias

## Operações CRUD Implementadas

### Create (Inserção)
```python
# Exemplo de inserção de registro de sensor
def insert_sensor_record(soil_moisture, ph_level, phosphorus, potassium, irrigation):
    record = SensorRecord(
        soil_moisture=soil_moisture,
        ph_level=ph_level,
        phosphorus_level=phosphorus,
        potassium_level=potassium,
        irrigation_active=irrigation
    )
    db.session.add(record)
    db.session.commit()
```

### Read (Consulta)
```python
# Exemplo de consulta de registros
def get_sensor_records(start_date, end_date):
    return SensorRecord.query.filter(
        SensorRecord.timestamp.between(start_date, end_date)
    ).all()
```

### Update (Atualização)
```python
# Exemplo de atualização de registro
def update_sensor_record(record_id, new_values):
    record = SensorRecord.query.get(record_id)
    for key, value in new_values.items():
        setattr(record, key, value)
    db.session.commit()
```

### Delete (Remoção)
```python
# Exemplo de remoção de registro
def delete_sensor_record(record_id):
    record = SensorRecord.query.get(record_id)
    db.session.delete(record)
    db.session.commit()
```

## Justificativa das Escolhas

1. **SQLAlchemy como ORM**
   - Facilita o mapeamento objeto-relacional
   - Fornece abstração do banco de dados
   - Suporta múltiplos bancos de dados

2. **Estrutura de Tabelas**
   - Normalização para evitar redundância
   - Índices para otimização de consultas
   - Timestamps para rastreamento

3. **Validações**
   - Verificação de tipos de dados
   - Restrições de integridade
   - Tratamento de erros

## Observações

- O sistema foi projetado para ser facilmente extensível
- As operações CRUD são documentadas e testadas
- O código segue as melhores práticas de Python
- A estrutura do banco permite futuras expansões 