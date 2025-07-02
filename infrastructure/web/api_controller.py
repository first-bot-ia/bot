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
        
        # Controlador interno para comunicación con Backend
        self.internal_controller = InternalController(
            self.twilio_service, 
            self.api_gateway_client
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
            """Webhook adapter - Forward to API Gateway"""
            try:
                webhook_data = request.get_json()
                
                # Solo normalizar datos de Twilio
                normalized_data = self._normalize_twilio_webhook(webhook_data)
                
                # Forward al API Gateway usando el cliente
                phone = webhook_data.get('From') or ''
                message = webhook_data.get('Body') or ''
                media_url = webhook_data.get('MediaUrl0')
                
                success, response_data = self.api_gateway_client.notify_user_response(
                    phone, message, media_url
                )
                
                return jsonify({'success': True}), 200
                
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