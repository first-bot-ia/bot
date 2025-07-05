"""
Microservicio WhatsApp - Especializado en Twilio Operations
Adaptador puro sin business logic
"""
from flask import Flask, request, jsonify
from typing import Dict, Any
import requests
import time
import os
from datetime import datetime

from config.settings import AppConfig
from infrastructure.external_services.twilio_service import TwilioWhatsAppService
from infrastructure.external_services.api_gateway_client import ApiGatewayClient
from infrastructure.external_services.backend_client import AlesseBackendClient
from infrastructure.web.internal_controller import InternalController


class WhatsAppBotAPI:
    """
    Microservicio especializado en WhatsApp/Twilio
    Solo operaciones de envío y adaptación de webhooks
    """
    
    def __init__(self, config: AppConfig):
        self.config = config
        self.app = Flask(__name__)
        
        # Solo servicios especializados
        self.twilio_service = TwilioWhatsAppService(config.twilio)
        self.api_gateway_client = ApiGatewayClient(config.web.api_gateway_url)
        self.backend_client = AlesseBackendClient(config.web.backend_url)
        
        # Controlador interno para comunicación con Backend
        self.internal_controller = InternalController(
            self.twilio_service, 
            self.api_gateway_client,
            self.backend_client
        )
        
        # Registrar rutas especializadas
        self._register_routes()
        
        # Registrar rutas internas
        self.app.register_blueprint(self.internal_controller.get_blueprint())
    
    def _register_routes(self):
        """Registra rutas especializadas del microservicio"""
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check para microservicio"""
            try:
                # Solo verificar servicios core
                twilio_ok, twilio_msg = self.twilio_service.test_connection()
                
                return jsonify({
                    'service': 'whatsapp-microservice',
                    'status': 'healthy' if twilio_ok else 'degraded',
                    'twilio': {
                        'status': 'ok' if twilio_ok else 'error',
                        'message': twilio_msg
                    },
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({
                    'service': 'whatsapp-microservice',
                    'status': 'unhealthy',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500
        
        @self.app.route('/whatsapp/webhook', methods=['POST'])
        def whatsapp_webhook():
            """Webhook adapter - Forward to API Gateway AND Backend"""
            try:
                webhook_data = request.get_json()
                
                # Extraer datos del webhook de Twilio
                phone_raw = webhook_data.get('From', '')
                phone = phone_raw.replace('whatsapp:', '') if phone_raw else ''
                message = webhook_data.get('Body', '')
                message_id = webhook_data.get('MessageSid')
                
                if not phone or not message:
                    return jsonify({'success': False, 'error': 'Phone or message missing'}), 400
                
                # 1. Forward al API Gateway (funcionalidad existente)
                media_url = webhook_data.get('MediaUrl0')
                success, response_data = self.api_gateway_client.notify_user_response(
                    phone, message, media_url
                )
                
                # 2. NUEVO: Forward al Backend Node.js
                backend_response = self.backend_client.send_message_to_backend(
                    phone=phone,
                    message=message,
                    message_id=message_id,
                    message_type="text"
                )
                
                return jsonify({
                    'success': True,
                    'api_gateway_response': response_data,
                    'backend_response': backend_response
                }), 200
                
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/execute/campaign', methods=['POST'])
        def execute_campaign():
            """Execute campaign - Only Twilio sending"""
            try:
                data = request.get_json()
                
                # Recibir datos ya procesados del Gateway
                phone_numbers = data.get('phone_numbers', [])
                message_content = data.get('message_content', '')
                media_url = data.get('media_url')
                delay_seconds = data.get('delay_seconds', 3)
                
                if not phone_numbers or not message_content:
                    return jsonify({
                        'success': False,
                        'error': 'phone_numbers and message_content required'
                    }), 400
                
                # Solo ejecutar envío via Twilio (sin business logic)
                results = self._execute_twilio_bulk_send(
                    phone_numbers, message_content, media_url, delay_seconds
                )
                
                return jsonify({
                    'success': True,
                    'results': results
                })
                
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/send/message', methods=['POST'])
        def send_single_message():
            """Send single message - Direct Twilio operation"""
            try:
                data = request.get_json()
                
                phone = data.get('phone')
                message = data.get('message')
                media_url = data.get('media_url')
                
                if not phone or not message:
                    return jsonify({
                        'success': False,
                        'error': 'phone and message required'
                    }), 400
                
                # Envío directo via Twilio
                success, result = self.twilio_service.send_message_direct(
                    phone, message, media_url
                )
                
                return jsonify({
                    'success': success,
                    'message_sid': result if success else None,
                    'error': result if not success else None
                })
                
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/send-message-to-user', methods=['POST'])
        def send_message_to_user():
            """
            Endpoint para que el Backend Node.js envíe mensajes a usuarios via WhatsApp
            Especificación según documentación de integración
            """
            try:
                data = request.get_json()
                
                if not data:
                    return jsonify({
                        'success': False,
                        'error': 'JSON data requerido'
                    }), 400
                
                # Validar campos requeridos según documentación
                phone = data.get('phone')
                message = data.get('message')
                
                if not phone or not message:
                    return jsonify({
                        'success': False,
                        'error': 'phone y message son requeridos'
                    }), 400
                
                # Campos opcionales
                conversation_id = data.get('conversationId')
                advisor_id = data.get('advisorId')
                
                # Enviar mensaje via Twilio (ya validamos que no sean None arriba)
                success, result = self.twilio_service.send_message_direct(
                    str(phone), str(message)
                )
                
                if success:
                    return jsonify({
                        'success': True,
                        'message': 'Mensaje enviado exitosamente',
                        'data': {
                            'phone': phone,
                            'conversationId': conversation_id,
                            'whatsappMessageId': result,
                            'status': 'sent'
                        }
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Error enviando mensaje via WhatsApp',
                        'details': result
                    }), 500
                    
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': 'Error interno del Bot',
                    'details': str(e)
                }), 500
    
    def _normalize_twilio_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normaliza datos del webhook de Twilio para el API Gateway"""
        return {
            'from': webhook_data.get('From'),
            'body': webhook_data.get('Body'),
            'timestamp': datetime.now().isoformat(),
            'twilio_sid': webhook_data.get('MessageSid'),
            'account_sid': webhook_data.get('AccountSid'),
            'num_media': webhook_data.get('NumMedia', '0'),
            'media_url_0': webhook_data.get('MediaUrl0') if webhook_data.get('NumMedia', '0') != '0' else None
        }
    
    def _execute_twilio_bulk_send(self, phone_numbers: list, message_content: str, 
                                 media_url: str = None, delay_seconds: int = 3) -> Dict[str, int]:
        """Ejecuta envío masivo solo via Twilio"""
        results = {'sent': 0, 'failed': 0, 'errors': []}
        
        for phone in phone_numbers:
            try:
                success, result = self.twilio_service.send_message_direct(
                    phone, message_content, media_url
                )
                
                if success:
                    results['sent'] += 1
                else:
                    results['failed'] += 1
                    results['errors'].append(f"{phone}: {result}")
                    
            except Exception as e:
                results['failed'] += 1
                results['errors'].append(f"{phone}: {str(e)}")
            
            # Delay entre envíos
            if delay_seconds > 0:
                time.sleep(delay_seconds)
        
        return results
    
    def run(self):
        """Ejecuta el microservicio"""
        self.app.run(
            host='0.0.0.0',
            port=self.config.web.port,
            debug=False  # Microservicio siempre en modo producción
        )