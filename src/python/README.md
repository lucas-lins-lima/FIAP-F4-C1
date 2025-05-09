# Sistema de Irrigação Inteligente - FarmTech Solutions

Este é um sistema de irrigação inteligente que utiliza sensores para monitorar e controlar a irrigação de culturas agrícolas.

## Estrutura do Projeto

```
src/python/
├── database/
│   ├── __init__.py
│   ├── models.py
│   ├── oracle.py
│   ├── setup.py
│   └── repositories/
│       ├── __init__.py
│       ├── produtor_repository.py
│       ├── cultura_repository.py
│       ├── sensor_repository.py
│       ├── leitura_sensor_repository.py
│       └── aplicacao_repository.py
├── examples/
│   └── repository_example.py
├── tests/
│   └── test_repositories.py
├── requirements.txt
├── pytest.ini
└── README.md
```

## Requisitos

- Python 3.8+
- Oracle Database (XE Edition)
- Docker e Docker Compose (opcional)

## Configuração

1. Clone o repositório
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure as variáveis de ambiente:
   ```bash
   ORACLE_USER=system
   ORACLE_PASSWORD=oracle
   ORACLE_HOST=localhost
   ORACLE_PORT=1521
   ORACLE_SERVICE=XE
   ```

## Executando com Docker

1. Construa e inicie os containers:
   ```bash
   docker-compose up -d
   ```

2. Para executar os testes:
   ```bash
   docker-compose run test
   ```

## Executando Localmente

1. Inicialize o banco de dados:
   ```bash
   python -m database.setup
   ```

2. Execute os testes:
   ```bash
   pytest
   ```

## Modelo de Dados

### Tabelas

#### Produtor
```sql
CREATE TABLE produtor (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR2(100) NOT NULL,
    email VARCHAR2(100) UNIQUE NOT NULL,
    telefone VARCHAR2(20)
);
```

#### Cultura
```sql
CREATE TABLE cultura (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR2(100) NOT NULL,
    tipo VARCHAR2(50) NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE,
    id_produtor NUMBER NOT NULL,
    FOREIGN KEY (id_produtor) REFERENCES produtor(id)
);
```

#### Sensor
```sql
CREATE TABLE sensor (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tipo VARCHAR2(50) NOT NULL,
    modelo VARCHAR2(50) NOT NULL,
    localizacao VARCHAR2(100) NOT NULL,
    id_cultura NUMBER NOT NULL,
    FOREIGN KEY (id_cultura) REFERENCES cultura(id)
);
```

#### Leitura Sensor
```sql
CREATE TABLE leitura_sensor (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_sensor NUMBER NOT NULL,
    data_hora TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    valor_umidade NUMBER(5,2),
    valor_ph NUMBER(4,2),
    valor_npk_fosforo NUMBER(5,2),
    valor_npk_potassio NUMBER(5,2),
    FOREIGN KEY (id_sensor) REFERENCES sensor(id)
);
```

#### Aplicação
```sql
CREATE TABLE aplicacao (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_cultura NUMBER NOT NULL,
    tipo VARCHAR2(50) NOT NULL,
    quantidade NUMBER(10,2) NOT NULL,
    data_hora TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    FOREIGN KEY (id_cultura) REFERENCES cultura(id)
);
```

## Testes

O projeto utiliza pytest para testes unitários e de integração. Os testes estão localizados no diretório `tests/` e podem ser executados de duas formas:

1. Usando Docker:
   ```bash
   docker-compose run test
   ```

2. Localmente:
   ```bash
   pytest
   ```

Os testes incluem:
- Testes de repositório para todas as entidades
- Fixtures para configuração do ambiente de teste
- Cobertura de código com pytest-cov

## Exemplos

O diretório `examples/` contém exemplos de uso dos repositórios:

- `repository_example.py`: Demonstra o uso básico dos repositórios para criar, buscar, atualizar e deletar registros.

Para executar o exemplo:
```bash
python examples/repository_example.py
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

4. **Docker para Desenvolvimento**
   - Ambiente consistente entre desenvolvedores
   - Fácil configuração do banco Oracle
   - Isolamento de dependências

## Observações

- O sistema foi projetado para ser facilmente extensível
- As operações CRUD são documentadas e testadas
- O código segue as melhores práticas de Python
- A estrutura do banco permite futuras expansões
- O ambiente Docker facilita o desenvolvimento e testes

