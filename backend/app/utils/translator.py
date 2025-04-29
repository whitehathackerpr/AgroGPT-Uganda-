from typing import Dict, Optional
import json
import os
from pathlib import Path

class Translator:
    def __init__(self, translations_path: str):
        self.translations = self._load_translations(translations_path)
        self.supported_languages = {
            "en": "English",
            "lg": "Luganda",
            "nyn": "Runyankole",
            "ach": "Acholi"
        }

    def _load_translations(self, translations_path: str) -> Dict:
        """Load translation files"""
        translations = {}
        path = Path(translations_path)
        
        for lang in self.supported_languages.keys():
            file_path = path / f"{lang}.json"
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    translations[lang] = json.load(f)
            else:
                translations[lang] = {}
                
        return translations

    def translate(self, text: str, target_lang: str, 
                 source_lang: str = "en") -> str:
        """Translate text to target language"""
        if target_lang not in self.supported_languages:
            raise ValueError(f"Unsupported language: {target_lang}")
            
        if target_lang == source_lang:
            return text
            
        # Simple word-for-word translation
        # In a real implementation, this would use a proper translation API
        translation = self.translations[target_lang].get(text, text)
        return translation

    def translate_disease_info(self, disease_info: Dict, 
                             target_lang: str) -> Dict:
        """Translate disease information to target language"""
        translated_info = {}
        for key, value in disease_info.items():
            if isinstance(value, str):
                translated_info[key] = self.translate(value, target_lang)
            else:
                translated_info[key] = value
        return translated_info

    def translate_weather_forecast(self, forecast: Dict, 
                                 target_lang: str) -> Dict:
        """Translate weather forecast to target language"""
        translated_forecast = forecast.copy()
        
        # Translate weather descriptions and units
        if "description" in forecast:
            translated_forecast["description"] = self.translate(
                forecast["description"], target_lang
            )
            
        # Translate units
        if "unit" in forecast:
            translated_forecast["unit"] = self.translate(
                forecast["unit"], target_lang
            )
            
        return translated_forecast

    def translate_market_insights(self, insights: Dict, 
                                target_lang: str) -> Dict:
        """Translate market insights to target language"""
        translated_insights = insights.copy()
        
        # Translate recommendations and descriptions
        if "recommendation" in insights:
            translated_insights["recommendation"] = self.translate(
                insights["recommendation"], target_lang
            )
            
        # Translate price trend description
        if "trend" in insights:
            translated_insights["trend"] = self.translate(
                insights["trend"], target_lang
            )
            
        return translated_insights

class TranslatorFactory:
    @staticmethod
    def create_translator() -> Translator:
        translations_path = os.getenv(
            "TRANSLATIONS_PATH", 
            "./app/translations"
        )
        return Translator(translations_path) 