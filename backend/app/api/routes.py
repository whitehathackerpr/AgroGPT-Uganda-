from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import os
from ..ml.disease_classifier import DiseaseClassifierFactory
from ..ml.weather_predictor import WeatherPredictorFactory
from ..ml.market_analyzer import MarketAnalyzerFactory
from ..utils.translator import TranslatorFactory
from ..services.sms_service import SMSServiceFactory

router = APIRouter()

# Initialize services
disease_classifier = DiseaseClassifierFactory.create_classifier()
weather_predictor = WeatherPredictorFactory.create_predictor()
market_analyzer = MarketAnalyzerFactory.create_analyzer()
translator = TranslatorFactory.create_translator()
sms_service = SMSServiceFactory.create_sms_service()

class DiseaseQuery(BaseModel):
    image_url: Optional[str] = None
    description: Optional[str] = None
    crop_type: str
    language: str = "en"

class WeatherQuery(BaseModel):
    region: str
    language: str = "en"

class MarketQuery(BaseModel):
    crop: str
    region: str
    language: str = "en"

class SMSQuery(BaseModel):
    phone_number: str
    message: str

@router.post("/diagnose-disease")
async def diagnose_disease(query: DiseaseQuery):
    try:
        if query.image_url:
            # Handle image-based diagnosis
            disease_name, confidence = disease_classifier.predict(query.image_url)
            disease_info = disease_classifier.get_disease_info(disease_name)
            
            # Translate if needed
            if query.language != "en":
                disease_info = translator.translate_disease_info(
                    disease_info, query.language
                )
                
            return {
                "status": "success",
                "disease": disease_name,
                "confidence": confidence,
                "information": disease_info
            }
        else:
            # Handle text-based diagnosis
            # This would use NLP to analyze the description
            return {
                "status": "success",
                "message": "Text-based diagnosis coming soon"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/weather-forecast")
async def get_weather_forecast(region: str, language: str = "en"):
    try:
        forecast = weather_predictor.get_weekly_forecast(region)
        
        # Translate if needed
        if language != "en":
            forecast = [
                translator.translate_weather_forecast(f, language)
                for f in forecast
            ]
            
        return {
            "status": "success",
            "forecast": forecast
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/market-prices")
async def get_market_prices(crop: str, region: str, language: str = "en"):
    try:
        insights = market_analyzer.get_market_insights(crop, region)
        
        # Translate if needed
        if language != "en":
            insights = translator.translate_market_insights(insights, language)
            
        return {
            "status": "success",
            "insights": insights
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-sms")
async def send_sms(query: SMSQuery):
    try:
        result = sms_service.send_sms(query.phone_number, query.message)
        return {
            "status": "success",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ussd")
async def handle_ussd(session_id: str, phone_number: str, 
                     ussd_code: str, text: str):
    try:
        result = sms_service.handle_ussd_request(
            session_id, phone_number, ussd_code, text
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/supported-languages")
async def get_supported_languages():
    return {
        "status": "success",
        "languages": translator.supported_languages
    }

@router.get("/supported-crops")
async def get_supported_crops():
    return {
        "status": "success",
        "crops": market_analyzer.crops
    }

@router.get("/supported-regions")
async def get_supported_regions():
    return {
        "status": "success",
        "regions": weather_predictor.regions
    } 