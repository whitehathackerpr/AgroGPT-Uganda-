from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, List
from ..services.weather_service import WeatherService
from .auth import get_current_user
from ..models.user import User

router = APIRouter()

@router.get("/weather/current/{location}")
async def get_current_weather(
    location: str,
    current_user: User = Depends(get_current_user)
) -> Dict:
    """Get current weather data for a specific location"""
    return await WeatherService.get_current_weather(location)

@router.get("/weather/forecast/{location}")
async def get_weather_forecast(
    location: str,
    days: int = 7,
    current_user: User = Depends(get_current_user)
) -> List[Dict]:
    """Get weather forecast for a specific location"""
    return await WeatherService.get_forecast(location, days)

@router.get("/weather/alerts/{location}")
async def get_weather_alerts(
    location: str,
    current_user: User = Depends(get_current_user)
) -> List[Dict]:
    """Get active weather alerts for a specific location"""
    return await WeatherService.get_alerts(location)

@router.get("/weather/agricultural-metrics/{location}")
async def get_agricultural_metrics(
    location: str,
    current_user: User = Depends(get_current_user)
) -> Dict:
    """Get agricultural relevant weather metrics (rainfall, soil moisture, etc.)"""
    return await WeatherService.get_agricultural_metrics(location) 