"""
Controlador interno para comunicación con Backend
Endpoints especializados para recibir comandos de otras plataformas
"""
from flask import Flask, request, jsonify, Blueprint
from typing import Dict, Any, List
import logging
from datetime import datetime

from infrastructure.external_services.twilio_service import TwilioWhatsAppService
from infrastructure.external_services.api_gateway_client import ApiGatewayClient

logger = logging.getLogger(__name__)


class InternalController:
    """
    Controlador interno para endpoints que no son públicos
    Maneja comunicación entrante desde Backend via API Gateway
    """
    
    def __init__(self, twilio_service: TwilioWhatsAppService, api_gateway_client: ApiGatewayClient):
        self.twilio_service = twilio_service
        self.api_gateway_client = api_gateway_client
        self.blueprint = Blueprint('internal', __name__, url_prefix='/internal')
        self._register_routes()
    
    def _register_routes(self):
        """Registra rutas internas del microservicio"""
        
        @self.blueprint.route('/send-message-to-user', methods=['POST'])
        def send_message_to_user():
            """
            Endpoint para que el Backend envíe mensajes a usuarios via WhatsApp
            Llamado por: Backend -> API Gateway -> Bot
            """
            try:
                data = request.get_json()
                
                if not data:
                    return jsonify({
                        'success': False,
                        'error': 'no_data',
                        'message': 'JSON data requerido'
                    }), 400
                
                # Validar campos requeridos
                phone = data.get('phone')
                message = data.get('message')
                
                if not phone or not message:
                    return jsonify({
                        'success': False,
                        'error': 'missing_fields',
                        'message': 'phone y message son requeridos'
                    }), 400
                
                # Campos opcionales
                media_url = data.get('media_url')
                advisor_id = data.get('advisor_id')
                conversation_id = data.get('conversation_id')
                
                logger.info(f"📨 Enviando mensaje a {phone} desde asesor {advisor_id}")
                
                # Enviar mensaje via Twilio
                success, result = self.twilio_service.send_message_direct(
                    phone, message, media_url
                )
                
                if success:
                    # Notificar al API Gateway que se envió el mensaje
                    self.api_gateway_client.notify_message_sent(phone, message, result)
                    
                    response_data = {
                        'success': True,
                        'twilio_sid': result,
                        'phone': phone,
                        'message': message,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    if advisor_id:
                        response_data['advisor_id'] = advisor_id
                    if conversation_id:
                        response_data['conversation_id'] = conversation_id
                    
                    logger.info(f"✅ Mensaje enviado exitosamente a {phone} (SID: {result})")
                    return jsonify(response_data), 200
                else:
                    logger.error(f"❌ Error enviando mensaje a {phone}: {result}")
                    return jsonify({
                        'success': False,
                        'error': 'twilio_error',
                        'message': result,
                        'phone': phone
                    }), 500
                    
            except Exception as e:
                logger.error(f"💥 Error inesperado en send_message_to_user: {str(e)}")
                return jsonify({
                    'success': False,
                    'error': 'internal_error',
                    'message': str(e)
                }), 500
        
        @self.blueprint.route('/health/detailed', methods=['GET'])
        def detailed_health_check():
            """
            Health check detallado para el Backend
            Incluye estado de Twilio y API Gateway
            """
            try:
                # Verificar Twilio
                twilio_ok, twilio_msg = self.twilio_service.test_connection()
                
                # Verificar API Gateway
                gateway_ok, gateway_data = self.api_gateway_client.health_check()
                
                overall_health = twilio_ok and gateway_ok
                
                return jsonify({
                    'service': 'whatsapp-bot-internal',
                    'status': 'healthy' if overall_health else 'degraded',
                    'components': {
                        'twilio': {
                            'status': 'ok' if twilio_ok else 'error',
                            'message': twilio_msg
                        },
                        'api_gateway': {
                            'status': 'ok' if gateway_ok else 'error',
                            'data': gateway_data
                        }
                    },
                    'timestamp': datetime.now().isoformat()
                }), 200 if overall_health else 503
                
            except Exception as e:
                logger.error(f"💥 Error en health check detallado: {str(e)}")
                return jsonify({
                    'service': 'whatsapp-bot-internal',
                    'status': 'unhealthy',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500
    
    def get_blueprint(self) -> Blueprint:
        """Retorna el blueprint para registrar en Flask"""
        return self.blueprint 