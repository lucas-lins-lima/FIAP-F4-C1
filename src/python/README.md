# Entrega 2: Armazenamento de Dados em Banco SQL com Python

Este projeto simula a coleta de dados agrícolas utilizando sensores físicos conectados a um ESP32.  
A aplicação em Python foi desenvolvida para armazenar, visualizar e analisar esses dados em um banco de dados Oracle, seguindo boas práticas de arquitetura, organização e clean code.


## Como Executar o Projeto

### Pré-requisitos

- [Python 3.9+](https://www.python.org/downloads/)
- Oracle Instant Client instalado e configurado
- Banco Oracle disponível (ou acesso ao banco simulado pela FIAP)
- IDE recomendada: VSCode

### Configuração do Ambiente

1. **Clonar o projeto**:
```bash
git clone hhttps://github.com/anacornachi/FIAP-F3-C1.git
cd fiap_fase3_cap1
```

2. **Criar e ativar ambiente virtual**:
```bash
# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

3. **Instalar dependências**:
```bash
pip install -r requirements.txt
```

4. **Configurar variáveis de ambiente**:
Crie um arquivo `.env` na pasta `src/python` com as variáveis do banco de dados da FIAP


5. **Inicializar o banco de dados**:
```bash
cd src/python
PYTHONPATH=$PYTHONPATH:$(pwd) python3 -m database.setup
```

Este script irá:
- Criar todas as tabelas necessárias
- Inicializar o banco com dados de exemplo
- Configurar as conexões necessárias

6. **Executar o sistema**:
```bash
python main.py
```

### Executando os Testes

Para executar os testes do projeto:

```bash
# Na pasta src/python
PYTHONPATH=$PYTHONPATH:$(pwd) pytest
```

# Verificar logs dos testes
pytest -v
```

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

#### produtor
```sql
CREATE TABLE produtor (
    id_produtor NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR2(200) NOT NULL,
    email VARCHAR2(200) NOT NULL,
    telefone VARCHAR2(30) NOT NULL
);
```

#### cultura
```sql
CREATE TABLE cultura (
    id_cultura NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR2(100) NOT NULL,
    tipo VARCHAR2(50) NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE,
    id_produtor NUMBER NOT NULL,
    CONSTRAINT fk_cultura_produtor FOREIGN KEY (id_produtor) 
        REFERENCES produtor(id_produtor)
);
```

#### sensor
```sql
CREATE TABLE sensor (
    id_sensor NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tipo VARCHAR2(50) NOT NULL,
    modelo VARCHAR2(50) NOT NULL,
    localizacao VARCHAR2(100) NOT NULL,
    id_cultura NUMBER NOT NULL,
    CONSTRAINT fk_sensor_cultura FOREIGN KEY (id_cultura) 
        REFERENCES cultura(id_cultura)
);
```

#### leitura_sensor
```sql
CREATE TABLE leitura_sensor (
    id_leitura NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_sensor NUMBER NOT NULL,
    data_hora TIMESTAMP NOT NULL,
    valor_umidade NUMBER,
    valor_ph NUMBER,
    valor_npk_fosforo NUMBER,
    valor_npk_potassio NUMBER,
    CONSTRAINT fk_leitura_sensor FOREIGN KEY (id_sensor) 
        REFERENCES sensor(id_sensor)
);
```

#### aplicacao
```sql
CREATE TABLE aplicacao (
    id_aplicacao NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_cultura NUMBER NOT NULL,
    data_hora TIMESTAMP NOT NULL,
    tipo VARCHAR2(50) NOT NULL,
    quantidade NUMBER NOT NULL,
    CONSTRAINT fk_aplicacao_cultura FOREIGN KEY (id_cultura) 
        REFERENCES cultura(id_cultura)
);
```

### 3. Relação com MER da Fase 2

A estrutura do banco de dados foi projetada seguindo o MER desenvolvido na Fase 2, com as seguintes considerações:

- **Entidades Principais**:
  - Produtor: Responsável pela plantação
  - Cultura: Plantação gerenciada
  - Sensor: Equipamento de coleta de dados
  - Leitura_Sensor: Dados coletados
  - Aplicacao: Ações realizadas na lavoura

- **Relacionamentos**:
  - 1 Produtor → N Culturas
  - 1 Cultura → N Sensores
  - 1 Sensor → N Leituras
  - 1 Cultura → N Aplicações

- **Adaptações Práticas**:
  - Uso de NUMBER em vez de INT/DOUBLE para compatibilidade Oracle
  - Adição de constraints para garantir integridade referencial
  - Timestamps para rastreamento temporal
  - Campos opcionais em leitura_sensor para diferentes tipos de sensores

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

## Estrutura do Projeto

```
src/python/
├── config/                    # Configurações do projeto
│   ├── __init__.py
│   └── settings.py           # Configurações gerais e constantes
│
├── database/                 # Camada de acesso a dados
│   ├── __init__.py
│   ├── models.py            # Definição dos modelos SQLAlchemy
│   ├── oracle.py            # Configuração da conexão Oracle
│   ├── setup.py             # Script de inicialização do banco
│   └── repositories/        # Implementação dos repositórios
│       ├── __init__.py
│       ├── produtor_repository.py
│       ├── cultura_repository.py
│       ├── sensor_repository.py
│       ├── leitura_sensor_repository.py
│       └── aplicacao_repository.py
│
├── examples/                 # Exemplos de uso
│   ├── __init__.py
│   └── repository_example.py # Exemplo de uso dos repositórios
│
├── logs/                    # Logs do sistema
│
├── services/               # Camada de serviços
│   ├── __init__.py
│   ├── sensor_service.py   # Serviço de processamento de sensores
│   ├── irrigation_service.py # Serviço de controle de irrigação
│   ├── produtor_service.py # Serviço de gerenciamento de produtores
│   ├── cultura_service.py  # Serviço de gerenciamento de culturas
│   └── aplicacao_service.py # Serviço de gerenciamento de aplicações
│
├── tests/                  # Testes automatizados
│   ├── __init__.py
│   ├── conftest.py        # Configurações dos testes
│   ├── test_models.py     # Testes dos modelos
│   ├── test_repositories.py # Testes dos repositórios
│   └── test_services.py   # Testes dos serviços
│
├── .env                    # Variáveis de ambiente
├── .gitignore             # Arquivos ignorados pelo git
├── main.py               # Ponto de entrada da aplicação
├── pytest.ini            # Configuração do pytest
├── README.md             # Documentação do projeto
└── requirements.txt      # Dependências do projeto
```

### Descrição dos Diretórios

#### config/
Contém as configurações do projeto, incluindo:
- Configurações do banco de dados
- Constantes do sistema
- Configurações de logging
- Variáveis de ambiente

#### database/
Implementa a camada de acesso a dados:
- `models.py`: Define as classes que mapeiam as tabelas do banco
- `oracle.py`: Gerencia a conexão com o banco Oracle
- `setup.py`: Script para inicialização do banco
- `repositories/`: Implementa o padrão Repository para cada entidade

#### examples/
Contém exemplos de uso do sistema:
- Exemplos de uso dos repositórios
- Exemplos de consultas complexas
- Exemplos de integração com serviços

#### logs/
Armazena os logs do sistema:
- Logs da aplicação em produção
- Logs dos testes
- Logs de erro e debug

#### services/
Implementa a lógica de negócio:
- Processamento de dados dos sensores
- Lógica de controle de irrigação
- Regras de negócio do sistema

#### tests/
Contém os testes automatizados:
- Testes unitários
- Testes de integração
- Fixtures e configurações de teste