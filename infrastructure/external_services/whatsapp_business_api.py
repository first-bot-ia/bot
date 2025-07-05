import os
import requests
from typing import Optional, Dict, Any

class WhatsAppBusinessAPI:
    def __init__(self, api_token: str, number_id: str):
        self.api_token = api_token
        self.number_id = number_id
        self.base_url = f"https://graph.facebook.com/v19.0/{self.number_id}"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def send_message(self, phone_number: str, message: str) -> Dict[str, Any]:
        """
        Envía un mensaje de texto a WhatsApp Business API
        Retorna un diccionario con success y message_id o error
        """
        try:
            url = f"{self.base_url}/messages"
            payload = {
                "messaging_product": "whatsapp",
                "to": phone_number,
                "type": "text",
                "text": {"body": message}
            }
            
            response = requests.post(url, headers=self.headers, json=payload)
            response_data = response.json()
            
            if response.status_code == 200 and "messages" in response_data:
                return {
                    "success": True,
                    "message_id": response_data["messages"][0]["id"],
                    "response": response_data
                }
            else:
                return {
                    "success": False,
                    "error": response_data.get("error", {}).get("message", "Unknown error"),
                    "status_code": response.status_code,
                    "response": response_data
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def send_template_message(self, phone_number: str, template_name: str, parameters: Optional[list] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": "es"},
                "components": [
                    {"type": "body", "parameters": parameters or []}
                ]
            }
        }
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()

    @staticmethod
    def parse_webhook(request_json: dict) -> Optional[Dict[str, Any]]:
        """
        Extrae el mensaje entrante del formato de webhook de Meta
        Retorna los campos esperados por el bot
        """
        try:
            entry = request_json.get("entry", [])[0]
            change = entry.get("changes", [])[0]
            value = change.get("value", {})
            messages = value.get("messages", [])
            
            if messages:
                msg = messages[0]
                # Solo procesamos mensajes de texto
                if msg.get("type") == "text":
                    return {
                        "from": msg["from"],
                        "message": msg["text"]["body"],  # Campo esperado por el bot
                        "message_id": msg.get("id"),
                        "timestamp": msg.get("timestamp"),
                        "type": msg.get("type"),
                        "raw": msg
                    }
        except Exception as e:
            print(f"Error parsing webhook: {e}")
            return None
        return None 