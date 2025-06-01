# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Nome do projeto

CAP 1 - Um mapa do tesouro
Sistema de irrigação inteligente com ESP32 e Python

## Nome do grupo

Grupo 73

## 👨‍🎓 Integrantes:

- <a href="https://www.linkedin.com/in/anacornachi/">Ana Cornachi</a>
- <a href="https://www.linkedin.com/in/carlamaximo/">Carla Máximo</a>
- <a href="https://www.linkedin.com/in/lucas-lins-lima/">Lucas Lins</a>

## 👩‍🏫 Professores:

### Tutor(a)

- <a href="https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/">Lucas Gomes Moreira</a>

### Coordenador(a)

- <a href="https://www.linkedin.com/in/andregodoichiovato/">André Godoi Chiovato</a>

## 📜 Descrição

O presente projeto propõe uma **solução de irrigação inteligente** desenvolvida em duas camadas: uma camada física embarcada com **ESP32** simulada no Wokwi e uma camada lógica em **Python**, responsável por decisões com base em dados meteorológicos e armazenamentos em banco de dados SQL.

A iniciativa parte de uma problemática real: o desperdício de água e a ineficiência na irrigação agrícola, especialmente em pequenas propriedades. Como solução, construímos um sistema que **lê variáveis ambientais** (umidade do solo, pH, nutrientes) e as combina com **dados climáticos reais** (via OpenWeather API), para decidir **automaticamente** se a bomba de irrigação deve ser ativada ou não.

No ambiente simulado, a parte física foi modelada com o simulador Wokwi, utilizando sensores como:

- Botões para simular presença de Fósforo (P) e Potássio (K)
- Sensor LDR simulando pH do solo
- Sensor DHT22 para umidade
- Relé e LED controlando a bomba de irrigação

Já o código Python consome uma API pública de clima, grava os dados em banco de dados relacional, permite análises via dashboard Streamlit, e simula o envio de comandos ao ESP32 via serial (ou via JSON em contexto de simulação).

Além disso, exploramos os conceitos de **IoT, automação agrícola, integração com APIs REST, banco de dados, POO, testes e dashboards interativos**, reforçando a aplicação prática de conteúdos aprendidos.

Diagrama DAP - Funcionamento da Solução
![DAP da aplicação](assets/DAP.png)

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

```
src/
├── esp32/ # Projeto do microcontrolador ESP32 (PlatformIO + C++)
├── python/ # Scripts Python (API, banco, dashboard, integração)
├── assets/ # Imagens, gráficos e materiais estáticos
├── document/ # Documentos acadêmicos e relatórios
```

Para mais detalhes sobre cada parte, consulte os READMEs específicos:

[📘 README do projeto ESP32](src/esp32/README.md)

[🐍 README do projeto Python + Dashboard](src/python/README.md)

## Entregas realizadas

### Entrega 1 - Sistema de Sensores e Controle com ESP32

Implementação do sistema físico simulado no Wokwi com lógica em C++. Inclui sensores de umidade (DHT22), pH (LDR), fósforo e potássio (botões), e controle do relé para ativar a bomba de irrigação.

- **Pasta de desenvolvimento**: src/esp32
- **Documentação Específica**: [📘 README do projeto ESP32](src/esp32/README.md)

- **Metas**:

  - Construir o circuito no Wokwi
  - Desenvolver código em C++
  - Documentar toda a lógica de controle

- **Entregáveis**:

  - Código C++ funcional
  - Imagem do circuito no Wokwi
  - Documentação detalhada

  ![Circuito Wokwi](/assets/circuito-esp32-wokwi.png)
  [Demonstração do circuito (video)](/assets/circuito-esp32-wokwi.mp4)

### Entrega 2 - Armazenamento de Dados em Banco SQL com Python

Sistema completo de armazenamento, processamento e visualização de dados dos sensores. Inclui integração com a API OpenWeather, banco de dados relacional e dashboard para análise dos dados, escopos do ir além 1 e 2, a serem descritos abaixo.

- **Pasta de desenvolvimento**: src/python
- **Documentação Específica**: [🐍 README do projeto Python + Dashboard](src/python/README.md)

- **Metas**:

  - Criar scripts para armazenamento em SQL
  - Implementar CRUD completo
  - Justificar estrutura de dados e relacionar com o MER da fase anterio

- **Entregáveis**:

  - Script Python funcional
  - Tabelas de exemplo com dados populados

  ![Diagrama do banco de dados](/assets/diagram.png)

### Ir Além 1 - Dashboard em Python

Painel visual com gráficos interativos para análise dos dados dos sensores. Inclui gráficos de tendência, dispersão, barras e linha, além de exportação para CSV.

- **Pasta de desenvolvimento**: src/python
- **Documentação Específica**: [🐍 README do projeto Python + Dashboard](src/python/README.md)

- **Metas**:

  -Criar visualizações claras e intuitivas para dados coletados

  - Permitir filtros e exportações

- **Entregáveis**:

  - Dashboard completo com gráficos interativos

  ![Dashbaord com graficos](/assets/dashboard_tabela.png)

### Ir Além 2 - Integração com API Pública

Integração com a API da OpenWeather para dados climáticos em tempo real, permitindo decisões de irrigação mais inteligentes. Inclui lógica para desativação da bomba em caso de previsão de chuva.

- **Pasta de desenvolvimento**: src/python
- **Documentação Específica**: [🐍 README do projeto Python + Dashboard](src/python/README.md)

- **Metas**:

  -Criar integração robusta com API

  - Implementar lógica condicional para irrigação
  - Armazenar dados meteorológicos no banco

- **Entregáveis**:

  - Scripts Python para integração com API
  - Tabelas populadas com dados climáticos
  - Documentação detalhada

### Fase 4 - Automação e Inteligência na FarmTech Solutions

Esta fase traz avanços significativos no projeto, incorporando tecnologias como Scikit-learn, Streamlit aprimorado, e otimizações no ESP32.

- **Pasta de desenvolvimento**: src/esp32 e src/python
- **Documentação Específica**: [📘 README do projeto ESP32](src/esp32/README.md) e [🐍 README do projeto Python + Dashboard](src/python/README.md)

- **Metas**:
  - Incorporar Scikit-learn para predição de necessidade de irrigação
  - Aprimorar o dashboard utilizando Streamlit
  - Adicionar display LCD I2C no circuito ESP32
  - Implementar monitoramento com Serial Plotter
  - Otimizar o uso de memória no ESP32

- **Entregáveis**:
  - Código C++ otimizado com suporte a LCD I2C
  - Implementação de Serial Plotter
  - Modelo preditivo com Scikit-learn
  - Dashboard avançado com Streamlit
  - Documentação atualizada

  ![Circuito com LCD I2C](/assets/circuito-fase4.png)
  ![Tela de Predição](/assets/dashboard-predicao.png)
  ![Serial Plotter](/assets/serial-plotter.png)
  
### 📌 Observações Finais

Como este projeto foi desenvolvido em um ambiente 100% simulado, não é possível estabelecer comunicação direta entre ESP32 e Python por porta serial. Para isso, utilizamos um arquivo climate.json como ponte de simulação dos dados meteorológicos.

Em um cenário real, essa comunicação seria feita com um ESP32 físico e uma conexão serial real utilizando pyserial.

## 🗃 Histórico de lançamentos

- 0.5.0 - 01/06/2025
  - ESP32 (src/esp32)
    - Adição de display LCD I2C para visualização local de informações
    - Implementação de formatação para Serial Plotter
    - Otimização do código C++ para eficiência de memória
    - Documentação das otimizações e monitoramento
  - Python (src/python)
    - Implementação de modelo preditivo com Scikit-learn
    - Previsão inteligente de necessidade de irrigação
    - Programação automática de horários ótimos para irrigação
    - Dashboard aprimorado com visualizações avançadas e interativas
  - Geral:
    - Documentação atualizada com explicações sobre o modelo ML
    - Testes e validações do sistema integrado
    - Vídeo demonstrativo da solução completa
- 0.4.0 - 18/05/2025
  - Ajustes na documentação, incluindo imagens e vídeos.
  - Padronização dos nomes das tabelas e colunas para inglês.
  - Correção do tipo de dado para fósforo e potássio.
  - Atualização dos models, services e repositories para refletir essas mudanças.
- 0.3.1 - 09/05/2025
  - Justificativa para mudança no banco de dados.
  - Criação dos repositories para todos os modelos com métodos CRUD completos e buscas específicas.
  - Incremento nos services para aproveitar ao máximo os relacionamentos entre tabelas.
  - Ajustes na documentação para refletir a nova estrutura do banco de dados.
- 0.3.0 - 04/05/2025
  - ESP32 (src/esp32)
    - Suporte à integração com climate.json (simulação da API OpenWeather).
    - Delay ajustado para 10 minutos por ciclo.
    - Código C++ comentado e otimizado.
    - README atualizado com lógica, simulações sugeridas e limitações do Wokwi.
  - Python (src/python)
    - Integração com API OpenWeather para coleta e envio de dados climáticos simulados.
    - CRUD completo com SQLAlchemy para climate_data, sensor_records e components.
  - Dashboard interativo com Streamlit:
    - Gráficos (linha, dispersão, histograma)
    - Exportação para CSV/PDF
    - Edição e exclusão de registros
    - Logger colorido e estruturado por arquivo.
  - Geral:
    - README principal reestruturado com base em PBL.
    - Inclusão de imagem DAP explicando o fluxo da aplicação local.
    - Links diretos para os projetos específicos (/src/esp32 e /src/python).
- 0.2.0 - 02/05/2025
  - Python (src/python)
    - Implementação da dashboard interativa com Streamlit.
    - Visualização completa dos dados climáticos, sensores e componentes.
    - Funcionalidades:
      - Cadastro, edição e exclusão de registros (CRUD)
      - Gráficos dinâmicos (temperatura, umidade, correlação)
      - Exportação de dados para CSV e PDF
      - Integração com serviços existentes do projeto python (sem necessidade de duplicação de lógica).
- 0.1.0 - 30/04/2025
  - Implementação inicial do sistema de irrigação inteligente utilizando ESP32
  - Adicionada leitura de sensores: umidade do solo (DHT22), presença de fósforo e potássio (botões físicos) e simulação de pH (sensor LDR)
  - Desenvolvimento da lógica de ativação e desativação da bomba de irrigação com base nas condições do solo
  - Integração do controle do relé e indicador LED
  - Construção do circuito completo no Wokwi para simulação do hardware
  - Criação de documentação detalhada no README, incluindo descrição do projeto, lógica de decisão baseada em fontes acadêmicas e imagem do circuito

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>

```

```
