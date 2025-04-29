import httpx
from typing import Dict, List
from ..utils.config import get_settings

settings = get_settings()

class WeatherService:
    WEATHER_API_KEY = settings.WEATHER_API_KEY
    WEATHER_API_BASE_URL = "https://api.weatherapi.com/v1"

    @staticmethod
    async def get_current_weather(location: str) -> Dict:
        """Get current weather data for a location"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{WeatherService.WEATHER_API_BASE_URL}/current.json",
                params={
                    "key": WeatherService.WEATHER_API_KEY,
                    "q": location,
                    "aqi": "yes"  # Include air quality data
                }
            )
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def get_forecast(location: str, days: int = 7) -> List[Dict]:
        """Get weather forecast for a location"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{WeatherService.WEATHER_API_BASE_URL}/forecast.json",
                params={
                    "key": WeatherService.WEATHER_API_KEY,
                    "q": location,
                    "days": days,
                    "aqi": "yes"
                }
            )
            response.raise_for_status()
            return response.json()["forecast"]["forecastday"]

    @staticmethod
    async def get_alerts(location: str) -> List[Dict]:
        """Get weather alerts for a location"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{WeatherService.WEATHER_API_BASE_URL}/alerts.json",
                params={
                    "key": WeatherService.WEATHER_API_KEY,
                    "q": location
                }
            )
            response.raise_for_status()
            return response.json().get("alerts", [])

    @staticmethod
    async def get_agricultural_metrics(location: str) -> Dict:
        """Get agricultural weather metrics"""
        forecast = await WeatherService.get_forecast(location, days=1)
        current = await WeatherService.get_current_weather(location)
        
        return {
            "rainfall_mm": forecast[0]["day"]["totalprecip_mm"],
            "soil_moisture": None,  # Would require additional API or sensor data
            "temperature_c": current["current"]["temp_c"],
            "humidity": current["current"]["humidity"],
            "wind_kph": current["current"]["wind_kph"],
            "uv_index": current["current"]["uv"]
        } 