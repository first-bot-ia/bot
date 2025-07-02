"""
Cliente HTTP para comunicación con API Gateway
Implementa comunicación saliente del bot hacia otras plataformas
"""
import requests
import json
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ApiGatewayClient:
    """
    Cliente especializado para comunicación con API Gateway
    Maneja todos los requests salientes del bot hacia otras plataformas
    """
    
    def __init__(self, api_gateway_url: str, timeout: int = 10):
        self.base_url = api_gateway_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        
        # Headers estándar para todas las requests
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'WhatsApp-Bot-Microservice/1.0',
            'X-Service-Name': 'whatsapp-bot'
        })
    
    def notify_user_response(self, phone: str, message: str, media_url: Optional[str] = None) -> Tuple[bool, Dict[str, Any]]:
        """
        Notifica al API Gateway que un usuario respondió via WhatsApp
        
        Args:
            phone: Número de teléfono del usuario (formato +51999123456)
            message: Mensaje recibido del usuario
            media_url: URL de archivo multimedia si existe
            
        Returns:
            Tuple[bool, Dict]: (success, response_data)
        """
        try:
            payload = {
                'from': phone,
                'body': message,
                'timestamp': datetime.now().isoformat(),
                'source': 'whatsapp',
                'service': 'bot'
            }
            
            if media_url:
                payload['media_url'] = media_url
            
            logger.info(f"Notificando respuesta de usuario {phone} al API Gateway")
            
            response = self.session.post(
                f"{self.base_url}/webhook/whatsapp",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                logger.info(f"✅ Notificación exitosa para {phone}")
                return True, response.json()
            else:
                logger.error(f"❌ Error {response.status_code} notificando {phone}: {response.text}")
                return False, {'error': f'HTTP {response.status_code}', 'detail': response.text}
                
        except requests.exceptions.Timeout:
            logger.error(f"⏱️ Timeout notificando {phone} al API Gateway")
            return False, {'error': 'timeout', 'detail': 'API Gateway no respondió'}
            
        except requests.exceptions.ConnectionError:
            logger.error(f"🔌 Error de conexión notificando {phone} al API Gateway")
            return False, {'error': 'connection_error', 'detail': 'No se pudo conectar al API Gateway'}
            
        except Exception as e:
            logger.error(f"💥 Error inesperado notificando {phone}: {str(e)}")
            return False, {'error': 'unexpected_error', 'detail': str(e)}
    
    def get_conversation_assignment(self, phone: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Obtiene la asignación de conversación para un usuario
        
        Args:
            phone: Número de teléfono del usuario
            
        Returns:
            Tuple[bool, Dict]: (success, assignment_data)
        """
        try:
            logger.info(f"Obteniendo asignación de conversación para {phone}")
            
            response = self.session.get(
                f"{self.base_url}/conversations/assignment/{phone}",
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                assignment_data = response.json()
                logger.info(f"✅ Asignación obtenida para {phone}: {assignment_data.get('advisor_id', 'sin-asesor')}")
                return True, assignment_data
            elif response.status_code == 404:
                logger.info(f"📭 No hay asignación para {phone}")
                return False, {'error': 'not_found', 'detail': 'Usuario sin asignación'}
            else:
                logger.error(f"❌ Error {response.status_code} obteniendo asignación {phone}: {response.text}")
                return False, {'error': f'HTTP {response.status_code}', 'detail': response.text}
                
        except requests.exceptions.Timeout:
            logger.error(f"⏱️ Timeout obteniendo asignación para {phone}")
            return False, {'error': 'timeout', 'detail': 'API Gateway no respondió'}
            
        except Exception as e:
            logger.error(f"💥 Error obteniendo asignación para {phone}: {str(e)}")
            return False, {'error': 'unexpected_error', 'detail': str(e)}
    
    def notify_message_sent(self, phone: str, message: str, twilio_sid: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Notifica al API Gateway que se envió un mensaje via Twilio
        
        Args:
            phone: Número destinatario
            message: Mensaje enviado
            twilio_sid: ID del mensaje en Twilio
            
        Returns:
            Tuple[bool, Dict]: (success, response_data)
        """
        try:
            payload = {
                'to': phone,
                'body': message,
                'twilio_sid': twilio_sid,
                'timestamp': datetime.now().isoformat(),
                'status': 'sent',
                'service': 'bot'
            }
            
            logger.info(f"Notificando mensaje enviado a {phone} (SID: {twilio_sid})")
            
            response = self.session.post(
                f"{self.base_url}/webhook/message-sent",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                logger.info(f"✅ Notificación de envío exitosa para {phone}")
                return True, response.json()
            else:
                logger.warning(f"⚠️ Error {response.status_code} notificando envío: {response.text}")
                return False, {'error': f'HTTP {response.status_code}', 'detail': response.text}
                
        except Exception as e:
            logger.error(f"💥 Error notificando envío para {phone}: {str(e)}")
            return False, {'error': 'unexpected_error', 'detail': str(e)}
    
    def health_check(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Verifica conectividad con API Gateway
        
        Returns:
            Tuple[bool, Dict]: (success, health_data)
        """
        try:
            response = self.session.get(
                f"{self.base_url}/health",
                timeout=5  # Timeout más corto para health check
            )
            
            if response.status_code == 200:
                health_data = response.json()
                logger.info("✅ API Gateway saludable")
                return True, health_data
            else:
                logger.warning(f"⚠️ API Gateway respondió {response.status_code}")
                return False, {'error': f'HTTP {response.status_code}', 'detail': response.text}
                
        except requests.exceptions.Timeout:
            logger.error("⏱️ Timeout verificando salud del API Gateway")
            return False, {'error': 'timeout', 'detail': 'API Gateway no respondió'}
            
        except Exception as e:
            logger.error(f"💥 Error verificando salud del API Gateway: {str(e)}")
            return False, {'error': 'connection_error', 'detail': str(e)}
    
    def close(self):
        """Cierra la sesión HTTP"""
        if self.session:
            self.session.close()
            logger.info("🔌 Sesión HTTP cerrada") 