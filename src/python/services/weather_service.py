import os
import time
import json
import serial
import requests

from logs.logger import Logger
from services.climate_service import create_climate_data

logger = Logger(__name__)() 


SERIAL_DOOR = os.getenv("PORTA_SERIAL", "/dev/ttyUSB0")
API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
CITY = os.getenv("OPEN_WEATHER_CITY")


def send_to_serial(json_data: str):
    """
    Envia dados JSON ao ESP32 via conexão serial.
    """
    try:
        with serial.Serial(SERIAL_DOOR, 115200, timeout=2) as ser:
            time.sleep(2)
            ser.write((json_data + "\n").encode())
            logger.info("[OK] Dados enviados ao ESP32 via serial")
    except serial.SerialException as e:
        logger.error(f"[ERRO] Porta serial indisponível: {e}")
    except Exception as e:
        logger.exception(f"[ERRO] Erro inesperado ao enviar dados via serial: {e}")




def fetch_weather_data():
    """
    Busca dados climáticos atuais da API OpenWeatherMap.
    Retorna um dicionário com: temperatura, umidade e previsão de chuva.
    """
    if not API_KEY or not CITY:
        raise ValueError("API_KEY ou CIDADE não configurados no .env")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=pt_br"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        print(f"Response from API: {data}")

        return {
            "temperature": data["main"]["temp"],
            "air_humidity": data["main"]["humidity"],
            "rain_forecast": "rain" in data
        }

    except requests.exceptions.HTTPError as http_err:
        print(f"[ERRO] Erro HTTP: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"[ERRO] Falha ao conectar à API: {err}")
    except Exception as e:
        print(f"[ERRO] Erro inesperado: {e}")

    return None

def run_weather_integration():
    """
    Executa o fluxo completo:
    1. Busca dados do clima
    2. Salva no banco de dados
    3. Envia via serial ao ESP32
    """
    logger.info("Iniciando integração climática...")

    try:
        data = fetch_weather_data()

        if not data:
            logger.warning("[ERRO] Dados climáticos não foram obtidos da API.")
            return

        logger.info("[OK] Dados climáticos obtidos com sucesso")

        # 1. Salva no banco de dados
        try:
            record = create_climate_data(data)
            logger.info(f"[OK] Registro salvo no banco: ID {record['id']}")
        except Exception as db_error:
            logger.exception(f"[ERRO] Falha ao salvar dados no banco: {db_error}")
            return

        # 2. Envia via serial
        try:
            send_to_serial(json.dumps(data))
        except Exception as serial_error:
            logger.exception(f"[ERRO] Falha ao enviar dados via serial: {serial_error}")
            return

    except Exception as e:
        logger.exception(f"[FATAL] Erro inesperado na integração climática: {e}")
