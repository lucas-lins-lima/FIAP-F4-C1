#include <Arduino.h>
#include "DHT.h"

// Definições de pinos
#define PHOSPHORUS_PIN 14     // Botão simulando presença de fósforo
#define POTASSIUM_PIN 4      // Botão simulando presença de potássio
#define PH_SENSOR_PIN 34     // LDR simulando o sensor de pH
#define DHT_PIN 5            // Pino de dados do DHT22 (umidade)
#define RELAY_PIN 12         // Controle do relé (bomba de irrigação)
#define LED_PIN 13

// Configuração do sensor DHT
#define DHTTYPE DHT22
DHT dht(DHT_PIN, DHTTYPE);

// Variáveis para armazenar leituras
float humidity = 0.0;
float ph = 0.0;
bool phosphorus_present = false;
bool potassium_present = false;

void setup() {
  Serial.begin(115200);

  pinMode(PHOSPHORUS_PIN, INPUT_PULLUP);
  pinMode(POTASSIUM_PIN, INPUT_PULLUP);
  pinMode(PH_SENSOR_PIN, INPUT);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);

  dht.begin();
  digitalWrite(RELAY_PIN, LOW);

  delay(100);
  Serial.println("Sistema de irrigação inteligente inicializado");
}

void loop() {
  // Leitura dos botões: pressionado = presença detectada
  phosphorus_present = (digitalRead(PHOSPHORUS_PIN) == LOW);
  potassium_present = (digitalRead(POTASSIUM_PIN) == LOW);

  // Leitura do pH via LDR (simulado)
  int ldr_value = analogRead(PH_SENSOR_PIN);
  Serial.print(ldr_value);
  ph = ((float)ldr_value / 4095.0) * 14.0;  // Converte o valor da LDR para a escala de pH

  // Leitura da umidade do solo
  humidity = dht.readHumidity();

  // Exibe as leituras no monitor serial
  Serial.print("Umidade: ");
  Serial.print(humidity);
  Serial.print("% | Fosforo: ");
  Serial.print(phosphorus_present ? "Presente" : "Ausente");
  Serial.print(" | Potassio: ");
  Serial.print(potassium_present ? "Presente" : "Ausente");
  Serial.print(" | pH: ");
  Serial.println(ph, 1);

  // Variável para decisão de irrigação
  bool irrigate = false;

  // Lógica de decisão:
  // 1. Irrigar se umidade < 40% e fósforo presente
  if (humidity < 40 && phosphorus_present) {
    irrigate = true;
  }

  // 2. Não irrigar se potássio presente e umidade > 60%
  if (potassium_present && humidity > 60) {
    irrigate = false;
  }

  // 3. Irrigar apenas se pH estiver entre 5.5 e 7.0 (faixa ótima)
  if (humidity < 40 && (ph < 5.5 || ph > 7.0)) {
    irrigate = false;
  }

  // 4. Nunca irrigar se umidade > 70%
  if (humidity > 70) {
    irrigate = false;
  }

  // 5. Irrigar se faltar fósforo ou potássio, mas com umidade entre 30% e 50%
  if ((!phosphorus_present || !potassium_present) && (humidity >= 30 && humidity <= 50)) {
    irrigate = true;
  }

  // Aciona ou desliga a bomba de acordo com a decisão final
  if (irrigate) {
    digitalWrite(RELAY_PIN, HIGH);
    digitalWrite(LED_PIN, HIGH); 
    Serial.println("Irrigação: ATIVADA");
  } else {
    digitalWrite(RELAY_PIN, LOW);
    digitalWrite(LED_PIN, LOW); 
    Serial.println("Irrigação: DESLIGADA");
  }

  // Aguarda 2 segundos antes da próxima leitura
  delay(2000);
}