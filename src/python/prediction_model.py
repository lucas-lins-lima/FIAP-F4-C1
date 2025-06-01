"""
Módulo para implementação de modelo preditivo de irrigação com Scikit-learn.
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import os
import logging
from datetime import datetime, timedelta

from database import SensorRecordRepository, ClimateDataRepository
from database.oracle import get_session

logger = logging.getLogger(__name__)

class IrrigationPredictor:
    """
    Classe para treinamento e predição de necessidades de irrigação
    usando dados históricos dos sensores e clima.
    """
    def __init__(self, model_path='irrigation_model.pkl'):
        self.model_path = model_path
        self.model = None
        self.scaler = StandardScaler()
        self.session = get_session()
        self.sensor_repo = SensorRecordRepository(self.session)
        self.climate_repo = ClimateDataRepository(self.session)
        
    def _prepare_data(self):
        """
        Prepara os dados para treinamento, combinando registros de sensores e dados climáticos.
        """
        # Buscar dados históricos
        sensor_records = self.sensor_repo.get_all()
        climate_data = self.climate_repo.get_all()
        
        if not sensor_records or not climate_data:
            logger.error("Dados insuficientes para treinamento")
            return None, None
            
        # Converter para DataFrames
        sensor_df = pd.DataFrame([
            {
                'timestamp': record.timestamp,
                'soil_moisture': record.soil_moisture,
                'phosphorus_present': int(record.phosphorus_present),
                'potassium_present': int(record.potassium_present),
                'soil_ph': record.soil_ph,
                'irrigation_status': 1 if record.irrigation_status == "ATIVADA" else 0
            } for record in sensor_records
        ])
        
        climate_df = pd.DataFrame([
            {
                'timestamp': record.timestamp,
                'temperature': record.temperature,
                'air_humidity': record.air_humidity,
                'rain_forecast': int(record.rain_forecast)
            } for record in climate_data
        ])
        
        # Mesclar os dados por timestamp próximo
        merged_data = []
        for _, sensor_row in sensor_df.iterrows():
            # Encontrar o registro climático mais próximo no tempo
            sensor_time = sensor_row['timestamp']
            closest_climate = min(
                climate_df.iterrows(), 
                key=lambda x: abs((x[1]['timestamp'] - sensor_time).total_seconds())
            )
            
            # Só considerar se a diferença for menor que 1 hora
            time_diff = abs((closest_climate[1]['timestamp'] - sensor_time).total_seconds())
            if time_diff <= 3600:  # 1 hora em segundos
                merged_data.append({
                    'soil_moisture': sensor_row['soil_moisture'],
                    'phosphorus_present': sensor_row['phosphorus_present'],
                    'potassium_present': sensor_row['potassium_present'],
                    'soil_ph': sensor_row['soil_ph'],
                    'temperature': closest_climate[1]['temperature'],
                    'air_humidity': closest_climate[1]['air_humidity'],
                    'rain_forecast': closest_climate[1]['rain_forecast'],
                    'irrigation_status': sensor_row['irrigation_status']
                })
        
        if not merged_data:
            logger.error("Não foi possível correlacionar dados de sensores e clima")
            return None, None
            
        # Criar DataFrame final
        df = pd.DataFrame(merged_data)
        
        # Separar features e target
        X = df.drop('irrigation_status', axis=1)
        y = df['irrigation_status']
        
        return X, y
    
    def train(self):
        """
        Treina o modelo de predição de irrigação.
        """
        # Preparar dados
        X, y = self._prepare_data()
        if X is None or y is None:
            return False
        
        # Split para treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Normalizar features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Treinar modelo
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train_scaled, y_train)
        
        # Avaliar modelo
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        logger.info(f"Acurácia do modelo: {accuracy:.4f}")
        
        # Relatório detalhado
        report = classification_report(y_test, y_pred)
        logger.info(f"Relatório de classificação:\n{report}")
        
        # Salvar modelo
        with open(self.model_path, 'wb') as f:
            pickle.dump((self.model, self.scaler), f)
        
        logger.info(f"Modelo salvo em: {self.model_path}")
        return True
    
    def load_model(self):
        """
        Carrega o modelo pré-treinado.
        """
        if not os.path.exists(self.model_path):
            logger.error(f"Arquivo de modelo não encontrado: {self.model_path}")
            return False
            
        try:
            with open(self.model_path, 'rb') as f:
                self.model, self.scaler = pickle.load(f)
            logger.info("Modelo carregado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {e}")
            return False
    
    def predict(self, soil_moisture, phosphorus_present, potassium_present, soil_ph, 
                temperature, air_humidity, rain_forecast):
        """
        Faz uma predição sobre a necessidade de irrigação.
        """
        if self.model is None:
            if not self.load_model():
                # Se não conseguir carregar, treina um novo
                self.train()
                
        if self.model is None:
            logger.error("Modelo não disponível para predição")
            return None
            
        # Preparar dados para predição
        data = np.array([[
            soil_moisture, 
            int(phosphorus_present), 
            int(potassium_present),
            soil_ph,
            temperature,
            air_humidity,
            int(rain_forecast)
        ]])
        
        # Normalizar
        data_scaled = self.scaler.transform(data)
        
        # Predizer
        prediction = self.model.predict(data_scaled)
        probability = self.model.predict_proba(data_scaled)
        
        return {
            'should_irrigate': bool(prediction[0]),
            'confidence': float(probability[0][1]) if prediction[0] else float(probability[0][0]),
            'prediction_time': datetime.now()
        }
        
    def predict_next_irrigation(self, hours_ahead=24, interval_hours=1):
        """
        Prevê a necessidade de irrigação para as próximas horas, com base nas tendências.
        Retorna horários recomendados para irrigação.
        """
        # Obter últimas leituras
        latest_sensor = self.sensor_repo.get_all()
        if not latest_sensor:
            return []
            
        latest_sensor = max(latest_sensor, key=lambda x: x.timestamp)
        
        latest_climate = self.climate_repo.get_all()
        if not latest_climate:
            return []
            
        latest_climate = max(latest_climate, key=lambda x: x.timestamp)
        
        # Valores base para previsão
        base_soil_moisture = latest_sensor.soil_moisture
        base_phosphorus = latest_sensor.phosphorus_present
        base_potassium = latest_sensor.potassium_present
        base_ph = latest_sensor.soil_ph
        base_temp = latest_climate.temperature
        base_humidity = latest_climate.air_humidity
        base_rain = latest_climate.rain_forecast
        
        # Simular diminuição de umidade ao longo do tempo (simplificação)
        moisture_decay_rate = 0.5  # % por hora
        
        recommended_times = []
        current_time = datetime.now()
        
        for hour in range(0, hours_ahead, interval_hours):
            # Projetar valores futuros
            future_time = current_time + timedelta(hours=hour)
            
            # Simular diminuição da umidade (simplificação)
            projected_moisture = max(0, base_soil_moisture - (moisture_decay_rate * hour))
            
            # Fazer predição
            prediction = self.predict(
                projected_moisture, 
                base_phosphorus, 
                base_potassium,
                base_ph,
                base_temp,
                base_humidity,
                base_rain
            )
            
            if prediction and prediction['should_irrigate']:
                recommended_times.append({
                    'time': future_time,
                    'predicted_moisture': projected_moisture,
                    'confidence': prediction['confidence']
                })
                
        return recommended_times

def train_irrigation_model():
    """
    Função para treinar o modelo de irrigação.
    """
    predictor = IrrigationPredictor()
    success = predictor.train()
    return success

def get_irrigation_prediction(soil_moisture, phosphorus, potassium, ph, temperature, humidity, rain):
    """
    Obtém uma predição para uma situação específica.
    """
    predictor = IrrigationPredictor()
    return predictor.predict(soil_moisture, phosphorus, potassium, ph, temperature, humidity, rain)

def get_future_irrigation_schedule():
    """
    Obtém uma programação de irrigação para as próximas horas.
    """
    predictor = IrrigationPredictor()
    return predictor.predict_next_irrigation(hours_ahead=48, interval_hours=3)

if __name__ == "__main__":
    # Testar funcionamento
    logging.basicConfig(level=logging.INFO)
    success = train_irrigation_model()
    print(f"Modelo treinado: {success}")
