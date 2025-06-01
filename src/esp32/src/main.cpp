#include <Arduino.h>
#include "DHT.h"
#include <ArduinoJson.h> 
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Definições de pinos (usando tipos otimizados)
const uint8_t PHOSPHORUS_PIN = 14;  // Botão simulando presença de fósforo
const uint8_t POTASSIUM_PIN = 4;    // Botão simulando presença de potássio
const uint8_t PH_SENSOR_PIN = 34;   // LDR simulando o sensor de pH
const uint8_t DHT_PIN = 5;          // Pino de dados do DHT22 (umidade)
const uint8_t RELAY_PIN = 12;       // Controle do relé (bomba de irrigação)
const uint8_t LED_PIN = 13;         // LED indicador

// Constantes I2C
const uint8_t I2C_SDA = 21;         // Pino SDA do I2C
const uint8_t I2C_SCL = 22;         // Pino SCL do I2C
const uint8_t LCD_ADDR = 0x27;      // Endereço I2C do LCD (padrão: 0x27)
const uint8_t LCD_COLS = 16;        // Número de colunas do LCD
const uint8_t LCD_ROWS = 2;         // Número de linhas do LCD

// Configuração do sensor DHT
#define DHTTYPE DHT22
DHT dht(DHT_PIN, DHTTYPE);

// Inicializa o LCD I2C
LiquidCrystal_I2C lcd(LCD_ADDR, LCD_COLS, LCD_ROWS);

// Variáveis para armazenar leituras (otimizadas)
float humidity = 0.0;
float ph = 0.0;
bool phosphorus_present = false;
bool potassium_present = false;
bool rain_forecast = false;
float air_humidity = 0.0;
float temperature = 0.0;

// Variáveis para Serial Plotter
uint32_t last_plot_time = 0;
const uint16_t PLOT_INTERVAL = 1000; // Intervalo para plotagem em ms

void setup() {
  Serial.begin(115200);

  // Inicialização dos pinos
  pinMode(PHOSPHORUS_PIN, INPUT_PULLUP);
  pinMode(POTASSIUM_PIN, INPUT_PULLUP);
  pinMode(PH_SENSOR_PIN, INPUT);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);

  // Inicializa o sensor DHT
  dht.begin();
  
  // Inicializa o display LCD
  Wire.begin(I2C_SDA, I2C_SCL);
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(F("FarmTech Fase 4"));
  lcd.setCursor(0, 1);
  lcd.print(F("Inicializando..."));
  
  // Inicia com a bomba desligada
  digitalWrite(RELAY_PIN, LOW);
  digitalWrite(LED_PIN, LOW);

  delay(100);
  
  // Mensagem de inicialização
  Serial.println(F("Sistema de irrigação inteligente inicializado - Fase 4"));
  Serial.println(F("Display LCD I2C conectado"));

  // Simula dados climáticos vindos de script Python (como se fossem enviados via porta serial)
  // Usando F() para economizar memória RAM
  const char* climate_json = "{"temperature": 22.5, "air_humidity": 75.0, "rain_forecast": false}";

  // Parseia os dados recebidos - Usando tamanho otimizado do buffer JSON
  StaticJsonDocument<96> doc; // Tamanho reduzido, calculado com ArduinoJson Assistant
  DeserializationError error = deserializeJson(doc, climate_json);

  if (error) {
    Serial.print(F("Erro ao ler dados climáticos: "));
    Serial.println(error.c_str());
    
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(F("Erro clima"));
  } else {
    temperature = doc["temperature"];
    air_humidity = doc["air_humidity"];
    rain_forecast = doc["rain_forecast"];

    Serial.print(F("Temperatura externa: "));
    Serial.println(temperature);
    Serial.print(F("Umidade do ar: "));
    Serial.println(air_humidity);
    Serial.print(F("Previsão de chuva: "));
    Serial.println(rain_forecast ? F("Sim") : F("Não"));
    
    // Exibe no LCD
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(F("Temp:"));
    lcd.print(temperature, 1);
    lcd.print(F("C"));
    
    lcd.setCursor(0, 1);
    lcd.print(F("Umid:"));
    lcd.print(air_humidity, 0);
    lcd.print(F("%"));
    
    if(rain_forecast) {
      lcd.setCursor(10, 1);
      lcd.print(F("CHUVA"));
    }
  }
  
  // Inicializa o tempo para Serial Plotter
  last_plot_time = millis();
}

void updateLCD() {
  // Função para atualizar o LCD com os dados atuais
  lcd.clear();
  
  // Linha 1: Umidade e pH
  lcd.setCursor(0, 0);
  lcd.print(F("U:"));
  lcd.print(humidity, 1);
  lcd.print(F("% pH:"));
  lcd.print(ph, 1);
  
  // Linha 2: Nutrientes e status da irrigação
  lcd.setCursor(0, 1);
  
  // Exibe P para fósforo e K para potássio
  lcd.print(F("P:"));
  lcd.print(phosphorus_present ? F("S") : F("N"));
  
  lcd.print(F(" K:"));
  lcd.print(potassium_present ? F("S") : F("N"));
  
  // Status da irrigação
  lcd.setCursor(9, 1);
  if (digitalRead(RELAY_PIN) == HIGH) {
    lcd.print(F("LIGADA"));
  } else {
    lcd.print(F("DESL"));
  }
}

void outputSerialPlotterData() {
  // Função para enviar dados formatados para o Serial Plotter
  // O formato é: "Umidade:valor,pH:valor,Irrigacao:valor"
  
  // Verifica se passou o intervalo de plotagem
  uint32_t current_time = millis();
  if (current_time - last_plot_time >= PLOT_INTERVAL) {
    last_plot_time = current_time;
    
    // Formata os dados para o Serial Plotter
    Serial.print(F("Umidade:"));
    Serial.print(humidity);
    Serial.print(F(",pH:"));
    Serial.print(ph);
    Serial.print(F(",Irrigacao:"));
    Serial.println(digitalRead(RELAY_PIN) * 100); // Multiplica por 100 para melhor visualização
  }
}

void loop() {
  // Otimização: Usa variáveis locais para armazenar temporariamente os valores
  // isso reduz o acesso à memória global
  bool should_irrigate = false;
  
  // Leitura dos botões: pressionado = presença detectada
  phosphorus_present = (digitalRead(PHOSPHORUS_PIN) == LOW);
  potassium_present = (digitalRead(POTASSIUM_PIN) == LOW);

  // Leitura do pH via LDR (simulado)
  uint16_t ldr_value = analogRead(PH_SENSOR_PIN); // Tipo uint16_t é suficiente para 0-4095
  ph = ((float)ldr_value / 4095.0f) * 14.0f;  // Convertido para float para maior precisão

  // Leitura da umidade do solo
  humidity = dht.readHumidity();

  // Exibe as leituras no monitor serial (usando F() para economizar memória)
  Serial.print(F("Umidade: "));
  Serial.print(humidity);
  Serial.print(F("% | Fosforo: "));
  Serial.print(phosphorus_present ? F("Presente") : F("Ausente"));
  Serial.print(F(" | Potassio: "));
  Serial.print(potassium_present ? F("Presente") : F("Ausente"));
  Serial.print(F(" | pH: "));
  Serial.println(ph, 1);

  // Saída para Serial Plotter
  outputSerialPlotterData();

  // Lógica de decisão:
  // 1. Não irrigar se houver previsão de chuva detectada
  if (rain_forecast) {
    Serial.println(F("Previsão de chuva detectada. Irrigação cancelada."));
    should_irrigate = false;
  } else {
    // 2. Irrigar se umidade < 40% e fósforo presente
    if (humidity < 40.0f && phosphorus_present) {
      should_irrigate = true;
    }
  
    // 3. Não irrigar se potássio presente e umidade > 60%
    if (potassium_present && humidity > 60.0f) {
      should_irrigate = false;
    }
  
    // 4. Irrigar apenas se pH estiver entre 5.5 e 7.0 (faixa ótima)
    if (humidity < 40.0f && (ph < 5.5f || ph > 7.0f)) {
      should_irrigate = false;
    }
  
    // 5. Nunca irrigar se umidade > 70%
    if (humidity > 70.0f) {
      should_irrigate = false;
    }
  
    // 6. Irrigar se faltar fósforo ou potássio, mas com umidade entre 30% e 50%
    if ((!phosphorus_present || !potassium_present) && (humidity >= 30.0f && humidity <= 50.0f)) {
      should_irrigate = true;
    }
  }

  // Aciona ou desliga a bomba de acordo com a decisão final
  digitalWrite(RELAY_PIN, should_irrigate ? HIGH : LOW);
  digitalWrite(LED_PIN, should_irrigate ? HIGH : LOW); 
  
  Serial.println(should_irrigate ? F("Irrigação: ATIVADA") : F("Irrigação: DESLIGADA"));
  
  // Atualiza o LCD com os dados atuais
  updateLCD();

  // Aguarda 10 segundos antes da próxima leitura (reduzido para teste)
  // Em produção usar 600000 (10 minutos)
  delay(10000);
}
