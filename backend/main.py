from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
import uvicorn
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from app.ml.disease_classifier import DiseaseClassifierFactory
from app.ml.weather_predictor import WeatherPredictorFactory
from app.ml.market_analyzer import MarketAnalyzerFactory
from app.services.weather_service import WeatherService

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AgroGPT-Uganda",
    description="AI-powered agricultural assistant for Ugandan farmers",
    version="1.0.0"
)

# Initialize services
disease_classifier = DiseaseClassifierFactory.create_classifier()
weather_predictor = WeatherPredictorFactory.create_predictor()
market_analyzer = MarketAnalyzerFactory.create_analyzer()
weather_service = WeatherService()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class User(BaseModel):
    id: int
    username: str
    email: str
    user_type: str  # farmer, extension_officer, researcher, policymaker
    language: str
    region: str

class DiseaseQuery(BaseModel):
    image_url: Optional[str] = None
    description: Optional[str] = None
    crop_type: str
    language: str = "en"

class WeatherQuery(BaseModel):
    region: str
    date: str

class MarketPriceQuery(BaseModel):
    crop: str
    region: str
    date: str

# Routes
@app.get("/")
async def root():
    return {"message": "Welcome to AgroGPT-Uganda API"}

@app.post("/diagnose-disease")
async def diagnose_disease(query: DiseaseQuery):
    try:
        if query.image_url:
            # Handle image-based diagnosis
            disease_name, confidence = disease_classifier.predict(query.image_url)
            disease_info = disease_classifier.get_disease_info(disease_name)
            
            return {
                "status": "success",
                "disease": disease_name,
                "confidence": confidence,
                "information": disease_info
            }
        else:
            # Handle text-based diagnosis
            return {
                "status": "error",
                "message": "Text-based diagnosis not supported yet. Please provide an image."
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/weather-forecast")
async def get_weather_forecast(region: str):
    try:
        forecast = weather_predictor.get_weekly_forecast(region)
        agricultural_metrics = await weather_service.get_agricultural_metrics(region)
        
        return {
            "status": "success",
            "forecast": forecast,
            "agricultural_metrics": agricultural_metrics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/market-prices")
async def get_market_prices(crop: str, region: str):
    try:
        insights = market_analyzer.get_market_insights(crop, region)
        return {
            "status": "success",
            "insights": insights
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/planting-calendar")
async def get_planting_calendar(crop: str, region: str):
    try:
        # Get weather forecast for optimal planting conditions
        forecast = weather_predictor.get_weekly_forecast(region)
        
        # Simple logic to determine planting recommendation based on weather
        total_rainfall = sum(day["rainfall"] for day in forecast)
        avg_temperature = sum(day["temperature"] for day in forecast) / len(forecast)
        
        is_suitable = total_rainfall > 20 and 20 <= avg_temperature <= 30
        
        return {
            "status": "success",
            "crop": crop,
            "region": region,
            "is_suitable_for_planting": is_suitable,
            "recommendation": "Suitable for planting" if is_suitable else "Wait for better conditions",
            "forecast": forecast
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 