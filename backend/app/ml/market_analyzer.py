import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import os
from sklearn.linear_model import LinearRegression
import joblib

class MarketAnalyzer:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.model = LinearRegression()
        self.crops = {
            "maize": "Maize",
            "beans": "Beans",
            "coffee": "Coffee",
            "bananas": "Bananas",
            "cassava": "Cassava"
        }
        self.regions = ["central", "eastern", "northern", "western"]
        self._load_data()

    def _load_data(self):
        """Load historical market data"""
        if os.path.exists(self.data_path):
            self.data = pd.read_csv(self.data_path)
            self.data['date'] = pd.to_datetime(self.data['date'])
        else:
            # Initialize with empty DataFrame if no data exists
            self.data = pd.DataFrame(columns=[
                'crop', 'region', 'price', 'unit', 'date', 'source'
            ])

    def add_price_data(self, crop: str, region: str, price: float, 
                      unit: str, source: str):
        """Add new price data to the dataset"""
        new_data = pd.DataFrame([{
            'crop': crop,
            'region': region,
            'price': price,
            'unit': unit,
            'date': datetime.now(),
            'source': source
        }])
        self.data = pd.concat([self.data, new_data], ignore_index=True)
        self.data.to_csv(self.data_path, index=False)

    def get_current_prices(self, crop: Optional[str] = None, 
                          region: Optional[str] = None) -> List[Dict]:
        """Get current market prices with optional filters"""
        recent_data = self.data[
            self.data['date'] > datetime.now() - timedelta(days=7)
        ]
        
        if crop:
            recent_data = recent_data[recent_data['crop'] == crop]
        if region:
            recent_data = recent_data[recent_data['region'] == region]
            
        return recent_data.to_dict('records')

    def predict_price_trend(self, crop: str, region: str, 
                          days_ahead: int = 30) -> Dict:
        """Predict price trend for a specific crop and region"""
        crop_data = self.data[
            (self.data['crop'] == crop) & 
            (self.data['region'] == region)
        ].copy()
        
        if len(crop_data) < 2:
            return {
                "error": "Insufficient data for prediction",
                "crop": crop,
                "region": region
            }
        
        # Prepare features for prediction
        crop_data['days'] = (crop_data['date'] - crop_data['date'].min()).dt.days
        X = crop_data[['days']].values
        y = crop_data['price'].values
        
        # Train model
        self.model.fit(X, y)
        
        # Make predictions
        future_days = np.array(range(
            crop_data['days'].max() + 1,
            crop_data['days'].max() + days_ahead + 1
        )).reshape(-1, 1)
        
        predicted_prices = self.model.predict(future_days)
        
        return {
            "crop": crop,
            "region": region,
            "current_price": float(crop_data['price'].iloc[-1]),
            "predicted_prices": predicted_prices.tolist(),
            "trend": "increasing" if predicted_prices[-1] > predicted_prices[0] else "decreasing",
            "confidence": 0.8  # Placeholder for actual confidence calculation
        }

    def get_market_insights(self, crop: str, region: str) -> Dict:
        """Get comprehensive market insights for a crop in a region"""
        current_prices = self.get_current_prices(crop, region)
        price_trend = self.predict_price_trend(crop, region)
        
        return {
            "crop": crop,
            "region": region,
            "current_prices": current_prices,
            "price_trend": price_trend,
            "recommendation": self._generate_recommendation(price_trend),
            "last_updated": datetime.now().isoformat()
        }

    def _generate_recommendation(self, price_trend: Dict) -> str:
        """Generate recommendation based on price trend"""
        if price_trend["trend"] == "increasing":
            return "Consider holding onto your produce as prices are expected to rise"
        else:
            return "Consider selling now as prices are expected to decrease"

class MarketAnalyzerFactory:
    @staticmethod
    def create_analyzer() -> MarketAnalyzer:
        data_path = os.getenv("MARKET_DATA_PATH", "./data/market_prices.csv")
        return MarketAnalyzer(data_path) 