"""
Cliente para comunicación con Backend Node.js
Implementa el patrón descrito en la documentación de integración
"""
import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class AlesseBackendClient:
    """
    Cliente HTTP para comunicarse con el Backend Node.js
    Implementa endpoint /internal/messages/webhook según documentación
    """
    
    def __init__(self, backend_url: str = "http://localhost:9000"):
        self.backend_url = backend_url
        self.webhook_endpoint = f"{backend_url}/internal/messages/webhook"
        self.timeout = 10
    
    def send_message_to_backend(
        self,
        phone: str,
        message: str,
        message_id: Optional[str] = None,
        contact_name: Optional[str] = None,
        message_type: str = "text"
    ) -> Dict[str, Any]:
        """
        Envía un mensaje entrante de WhatsApp al Backend Node.js
        
        Args:
            phone: Número de teléfono con código de país (ej: "573001234567")
            message: Contenido del mensaje
            message_id: ID único del mensaje de WhatsApp (opcional)
            contact_name: Nombre del contacto (opcional)
            message_type: Tipo de mensaje (text, image, document, etc.)
        
        Returns:
            dict: Respuesta del Backend con información del mensaje creado
        """
        
        payload = {
            "phone": phone,
            "message": message,
            "timestamp": datetime.now().isoformat() + "Z",
            "type": message_type
        }
        
        # Agregar campos opcionales si están disponibles
        if message_id:
            payload["messageId"] = message_id
        if contact_name:
            payload["contactName"] = contact_name
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            logger.info(f"📤 Enviando mensaje al Backend: {phone} -> {message[:50]}...")
            
            response = requests.post(
                self.webhook_endpoint,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Mensaje enviado al Backend: ID {result['data']['messageId']}")
                return result
            else:
                logger.error(f"❌ Error enviando al Backend: {response.status_code}")
                logger.error(f"Respuesta: {response.text}")
                return {
                    "success": False, 
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error de conexión con Backend: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def health_check(self) -> tuple[bool, Dict[str, Any]]:
        """
        Verifica que el Backend esté funcionando
        
        Returns:
            tuple: (is_healthy, health_data)
        """
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            return False, {"error": str(e)}
    
    def get_pending_conversations(self) -> Dict[str, Any]:
        """
        Obtiene conversaciones pendientes del Backend
        """
        try:
            response = requests.get(
                f"{self.backend_url}/internal/conversations/pending",
                timeout=self.timeout
            )
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_available_advisors(self) -> Dict[str, Any]:
        """
        Obtiene asesores disponibles del Backend
        """
        try:
            response = requests.get(
                f"{self.backend_url}/internal/advisors/available",
                timeout=self.timeout
            )
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)} 