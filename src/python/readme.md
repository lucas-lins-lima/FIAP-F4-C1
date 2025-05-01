# FarmTech Solutions - Python Irrigation Managment

Este projeto simula a coleta de dados agrícolas utilizando sensores físicos conectados a um ESP32.  
A aplicação em Python foi desenvolvida para armazenar, visualizar e analisar esses dados em um banco de dados Oracle, seguindo boas práticas de arquitetura, organização e clean code.

## Funcionalidades

- Armazenamento de dados de sensores (umidade, pH, fósforo e potássio)
- Armazenamento de dados climáticos externos
- Operações completas de CRUD para todos os dados
- Geração automática do DDL e visualização do MER
- Sistema robusto de logs
- Preparado para futuras extensões (Dashboard Streamlit)

## Como executar o código

Este projeto foi desenvolvido em Python e executa via terminal.

---

### Pré-requisitos

- [Python 3.9+](https://www.python.org/downloads/)
- Oracle Instant Client instalado e configurado
- Banco Oracle disponível (ou acesso ao banco simulado pela FIAP)
- IDE recomendada: VSCode

---

### Fase 1: Clonar o projeto

```bash
git clone https://github.com/Hinten/fiap_fase3_cap1.git
cd fiap_fase3_cap1
```

---

### Fase 2: Criar e ativar ambiente virtual (venv)

#### Linux/Mac:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

### Fase 3: Instalar as dependências

Certifique-se de que o arquivo `requirements.txt` está na raiz do projeto:

```bash
pip install -r requirements.txt
```

---

### Fase 4: Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis preenchidas:

```
ORACLE_USER=seu_usuario
ORACLE_PASSWORD=sua_senha
ORACLE_HOST=oracle.fiap.com.br
ORACLE_PORT=1521
ORACLE_SERVICE=ORCL
```

> **Dica:** O `.env` será lido automaticamente pelo projeto para realizar a conexão com o banco Oracle.  
> O carregamento é feito via `python-dotenv`, já incluída no `requirements.txt`.

---

### Fase 5: Criar as tabelas no banco Oracle

Execute o script abaixo para criar todas as tabelas necessárias:

```bash
python src/python/database/setup.py
```

As tabelas criadas serão:
- `components`
- `sensor_records`
- `climate_data`

---

### Fase 6: Executar o sistema

Com o ambiente configurado, execute o sistema principal via terminal:

```bash
python src/python/main.py
```

✅ O sistema irá:

- Configurar os logs
- Conectar-se ao banco Oracle
- Criar as tabelas automaticamente (caso não existam)
- Exibir e registrar o log de toda a execução

## 🧰 DDL e MER do banco de dados

Para gerar o arquivo DDL e MER, basta executar esse comando. O resultado poderá ser visto no terminal

```bash
python src/python/utils.py
```

- **Criar componentes, sensores e climas** (via services):

```python
from services.component_service import create_component

create_component({
    "name": "DHT22 Sensor",
    "type": "Sensor"
})
```

## Serviços Disponíveis (CRUD)

- `create_component(data: dict)`
- `list_components()`
- `update_component(id, data)`
- `delete_component(id)`

- `create_sensor_record(data: dict)`
- `list_sensor_records()`

(Disponível para **Componentes**, **Sensores** e **Climas**)

---

## Observação sobre o Banco

Cada registro de sensor (`SensorRecord`) agrega:

- Umidade do solo
- pH do solo
- Presença de fósforo
- Presença de potássio
- Status da irrigação (ATIVADA/DESLIGADA)
