import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from typing import Dict, List
import joblib
import os
from datetime import datetime, timedelta

class WeatherPredictor:
    def __init__(self, model_path: str):
        self.model = self._load_model(model_path)
        self.regions = {
            "central": {"lat": 0.3476, "lon": 32.5825},
            "eastern": {"lat": 0.5333, "lon": 33.4833},
            "northern": {"lat": 2.7746, "lon": 32.2980},
            "western": {"lat": 0.6111, "lon": 30.6549}
        }

    def _load_model(self, model_path: str) -> RandomForestRegressor:
        """Load the trained weather prediction model"""
        if os.path.exists(model_path):
            return joblib.load(model_path)
        else:
            # Initialize a new model if none exists
            return RandomForestRegressor(n_estimators=100, random_state=42)

    def prepare_features(self, region: str, date: datetime) -> np.ndarray:
        """Prepare features for weather prediction"""
        region_data = self.regions[region]
        features = [
            region_data["lat"],
            region_data["lon"],
            date.month,
            date.day,
            date.year
        ]
        return np.array(features).reshape(1, -1)

    def predict_weather(self, region: str, date: datetime) -> Dict:
        """Predict weather for a specific region and date"""
        if region not in self.regions:
            raise ValueError(f"Unknown region: {region}")

        features = self.prepare_features(region, date)
        
        # Predict temperature, rainfall, and humidity
        temperature = self.model.predict(features)[0]
        
        # Add some randomness to simulate weather variability
        rainfall = np.random.uniform(0, 50)  # mm
        humidity = np.random.uniform(30, 90)  # percentage
        
        return {
            "temperature": round(temperature, 2),
            "rainfall": round(rainfall, 2),
            "humidity": round(humidity, 2),
            "date": date.strftime("%Y-%m-%d"),
            "region": region
        }

    def get_weekly_forecast(self, region: str) -> List[Dict]:
        """Get weather forecast for the next 7 days"""
        forecasts = []
        today = datetime.now()
        
        for i in range(7):
            date = today + timedelta(days=i)
            forecast = self.predict_weather(region, date)
            forecasts.append(forecast)
            
        return forecasts

class WeatherPredictorFactory:
    @staticmethod
    def create_predictor() -> WeatherPredictor:
        model_path = os.getenv("WEATHER_MODEL_PATH", "./ml/models/weather_predictor.joblib")
        return WeatherPredictor(model_path) 