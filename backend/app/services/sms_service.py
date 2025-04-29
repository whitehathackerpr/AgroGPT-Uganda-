from typing import Dict, Optional
import os
import requests
from datetime import datetime
import json

class SMSService:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.smsprovider.com/v1"  # Replace with actual SMS provider URL
        
    def send_sms(self, phone_number: str, message: str) -> Dict:
        """Send SMS to a phone number"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "to": phone_number,
            "message": message,
            "from": "AgroGPT"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/sms/send",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return {
                "status": "success",
                "message_id": response.json().get("message_id"),
                "timestamp": datetime.now().isoformat()
            }
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def handle_ussd_request(self, session_id: str, phone_number: str, 
                          ussd_code: str, text: str) -> Dict:
        """Handle USSD requests from farmers"""
        # Parse USSD input
        input_text = text.split("*")[-1] if "*" in text else text
        
        # Process different USSD menu options
        if input_text == "":
            # Main menu
            return self._generate_ussd_response(
                "Welcome to AgroGPT\n1. Disease Diagnosis\n2. Weather Info\n3. Market Prices\n4. Farming Tips"
            )
        elif input_text == "1":
            # Disease diagnosis menu
            return self._generate_ussd_response(
                "Disease Diagnosis\n1. Maize\n2. Beans\n3. Coffee\n4. Bananas\n5. Cassava"
            )
        elif input_text == "2":
            # Weather information menu
            return self._generate_ussd_response(
                "Weather Information\n1. Central\n2. Eastern\n3. Northern\n4. Western"
            )
        elif input_text == "3":
            # Market prices menu
            return self._generate_ussd_response(
                "Market Prices\n1. Maize\n2. Beans\n3. Coffee\n4. Bananas\n5. Cassava"
            )
        else:
            return self._generate_ussd_response(
                "Invalid option. Please try again."
            )

    def _generate_ussd_response(self, message: str) -> Dict:
        """Generate USSD response format"""
        return {
            "response": message,
            "continue_session": True
        }

    def send_bulk_sms(self, phone_numbers: list, message: str) -> Dict:
        """Send SMS to multiple phone numbers"""
        results = []
        for phone_number in phone_numbers:
            result = self.send_sms(phone_number, message)
            results.append({
                "phone_number": phone_number,
                "status": result["status"],
                "message_id": result.get("message_id"),
                "timestamp": result["timestamp"]
            })
        return {
            "status": "completed",
            "results": results,
            "total_sent": len(results)
        }

    def schedule_sms(self, phone_number: str, message: str, 
                    schedule_time: datetime) -> Dict:
        """Schedule SMS for future delivery"""
        # Implementation would depend on SMS provider's API
        return {
            "status": "scheduled",
            "phone_number": phone_number,
            "scheduled_time": schedule_time.isoformat(),
            "message_id": "scheduled_" + datetime.now().strftime("%Y%m%d%H%M%S")
        }

class SMSServiceFactory:
    @staticmethod
    def create_sms_service() -> SMSService:
        api_key = os.getenv("SMS_API_KEY")
        api_secret = os.getenv("SMS_API_SECRET")
        
        if not api_key or not api_secret:
            raise ValueError("SMS API credentials not found in environment variables")
            
        return SMSService(api_key, api_secret) 