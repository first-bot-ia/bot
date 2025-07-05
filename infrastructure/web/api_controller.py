"""
Microservicio WhatsApp - Especializado en Twilio Operations
Adaptador puro sin business logic
"""
from flask import Flask, request, jsonify
from typing import Dict, Any, List
import requests
import time
import os
import logging
from datetime import datetime

from config.settings import AppConfig
from infrastructure.external_services.whatsapp_business_api import WhatsAppBusinessAPI
from infrastructure.external_services.api_gateway_client import ApiGatewayClient
from infrastructure.external_services.backend_client import AlesseBackendClient

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhatsAppBotAPI:
    """
    Microservicio especializado en WhatsApp/Twilio
    Solo operaciones de envío y adaptación de webhooks
    """
    
    def __init__(self, config: AppConfig):
        self.config = config
        self.app = Flask(__name__)
        
        # Solo servicios especializados
        self.whatsapp_service = WhatsAppBusinessAPI(
            api_token=config.whatsapp.api_token,
            number_id=config.whatsapp.number_id
        )
        self.api_gateway_client = ApiGatewayClient(config.web.api_gateway_url)
        self.backend_client = AlesseBackendClient(config.web.backend_url)
        
        # Registrar rutas especializadas
        self._register_routes()
    
    def _register_routes(self):
        """Registra todas las rutas del bot"""
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check del bot"""
            try:
                return jsonify({
                    'service': 'whatsapp-bot',
                    'status': 'healthy',
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Health check failed: {str(e)}")
                return jsonify({
                    'service': 'whatsapp-bot',
                    'status': 'unhealthy',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500
        
        @self.app.route('/send/message', methods=['POST'])
        def send_message():
            """Envía un mensaje individual de WhatsApp"""
            try:
                data = request.get_json()
                phone = data.get('phone')
                message = data.get('message')
                
                if not phone or not message:
                    return jsonify({"error": "Phone and message required"}), 400
                
                # Validar que el mensaje sea solo texto
                if not isinstance(message, str) or len(message.strip()) == 0:
                    return jsonify({"error": "Message must be non-empty text"}), 400
                
                # Enviar mensaje
                result = self.whatsapp_service.send_message(phone, message)
                
                if result.get('success'):
                    return jsonify({
                        "success": True,
                        "message": "Message sent successfully",
                        "message_id": result.get('message_id')
                    })
                else:
                    return jsonify({
                        "success": False,
                        "error": result.get('error', 'Unknown error')
                    }), 500
                    
            except Exception as e:
                logger.error(f"Error sending message: {str(e)}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/campaigns/send', methods=['POST'])
        def send_campaign():
            """Envía campaña masiva a todos los contactos"""
            try:
                data = request.get_json()
                message = data.get('message')
                campaign_id = data.get('campaign_id')
                
                if not message or not campaign_id:
                    return jsonify({"error": "Message and campaign_id required"}), 400
                
                # Validar que el mensaje sea solo texto
                if not isinstance(message, str) or len(message.strip()) == 0:
                    return jsonify({"error": "Message must be non-empty text"}), 400
                
                logger.info(f"Starting campaign {campaign_id} with message: {message[:50]}...")
                
                # Obtener contactos del backend
                contacts_response = self.backend_client.get_campaign_contacts(campaign_id)
                
                if not contacts_response.get('success'):
                    return jsonify({
                        "success": False,
                        "error": "Failed to get contacts from backend"
                    }), 500
                
                contacts = contacts_response.get('contacts', [])
                
                if not contacts:
                    return jsonify({
                        "success": False,
                        "error": "No contacts found for campaign"
                    }), 400
                
                # Enviar mensajes uno por uno
                sent_count = 0
                failed_count = 0
                failed_contacts = []
                
                for contact in contacts:
                    try:
                        phone = contact.get('phone')
                        if not phone:
                            failed_count += 1
                            failed_contacts.append({"contact": contact, "error": "No phone number"})
                            continue
                        
                        # Personalizar mensaje con nombre si existe
                        personalized_message = message
                        if contact.get('name'):
                            personalized_message = f"Hola {contact['name']}, {message}"
                        
                        # Enviar mensaje
                        result = self.whatsapp_service.send_message(phone, personalized_message)
                        
                        if result.get('success'):
                            sent_count += 1
                            logger.info(f"Message sent to {phone}")
                        else:
                            failed_count += 1
                            failed_contacts.append({
                                "contact": contact,
                                "error": result.get('error', 'Unknown error')
                            })
                            logger.error(f"Failed to send message to {phone}: {result.get('error')}")
                        
                        # Delay entre mensajes para evitar rate limiting
                        time.sleep(1)
                        
                    except Exception as e:
                        failed_count += 1
                        failed_contacts.append({
                            "contact": contact,
                            "error": str(e)
                        })
                        logger.error(f"Error sending to contact {contact}: {str(e)}")
                
                # Actualizar estado de campaña en backend
                self.backend_client.update_campaign_status(campaign_id, {
                    'sent_count': sent_count,
                    'failed_count': failed_count,
                    'status': 'completed' if failed_count == 0 else 'completed_with_errors'
                })
                
                return jsonify({
                    "success": True,
                    "campaign_id": campaign_id,
                    "total_contacts": len(contacts),
                    "sent_count": sent_count,
                    "failed_count": failed_count,
                    "failed_contacts": failed_contacts[:5]  # Solo primeros 5 errores
                })
                
            except Exception as e:
                logger.error(f"Error in campaign: {str(e)}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/campaigns/<campaign_id>/status', methods=['GET'])
        def get_campaign_status(campaign_id):
            """Obtiene el estado de una campaña"""
            try:
                # Obtener estado del backend
                status_response = self.backend_client.get_campaign_status(campaign_id)
                
                if status_response.get('success'):
                    return jsonify(status_response)
                else:
                    return jsonify({
                        "success": False,
                        "error": "Campaign not found"
                    }), 404
                    
            except Exception as e:
                logger.error(f"Error getting campaign status: {str(e)}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/webhook/whatsapp', methods=['GET', 'POST'])
        def whatsapp_webhook():
            """Webhook para recibir mensajes de WhatsApp"""
            try:
                if request.method == 'GET':
                    # Verificación del webhook
                    mode = request.args.get('hub.mode')
                    token = request.args.get('hub.verify_token')
                    challenge = request.args.get('hub.challenge')
                    
                    logger.info(f"Webhook verification attempt - mode: {mode}, token: {token}, expected: {self.config.whatsapp.verify_token}")
                    
                    if mode == 'subscribe' and token == self.config.whatsapp.verify_token:
                        logger.info("Webhook verified successfully")
                        return str(challenge) if challenge else "", 200
                    else:
                        logger.warning(f"Webhook verification failed - mode: {mode}, token: {token}")
                        return 'Verification failed', 403
                
                elif request.method == 'POST':
                    # Procesar mensaje entrante
                    data = request.get_json()
                    
                    if not data:
                        return jsonify({"error": "No data received"}), 400
                    
                    # Parsear webhook usando WhatsApp Business API
                    parsed_data = self.whatsapp_service.parse_webhook(data)
                    
                    if not parsed_data:
                        logger.info("No processable message in webhook")
                        return jsonify({"status": "no_message"}), 200
                    
                    # Extraer información del mensaje
                    from_number = parsed_data.get('from')
                    message_text = parsed_data.get('message')
                    message_id = parsed_data.get('message_id')
                    timestamp = parsed_data.get('timestamp')
                    
                    if not from_number or not message_text:
                        logger.warning("Invalid message data received")
                        return jsonify({"status": "invalid_data"}), 200
                    
                    logger.info(f"Received message from {from_number}: {message_text[:50]}...")
                    
                    # Crear conversación en el backend
                    conversation_data = {
                        'contactPhone': from_number,
                        'initialMessage': message_text,
                        'source': 'whatsapp',
                        'timestamp': timestamp or datetime.now().isoformat(),
                        'messageId': message_id
                    }
                    
                    # Crear o actualizar conversación
                    conversation_response = self.backend_client.create_conversation(conversation_data)
                    
                    if conversation_response.get('success'):
                        logger.info(f"Conversation created/updated for {from_number}")
                    else:
                        logger.error(f"Failed to create conversation: {conversation_response.get('error')}")
                    
                    return jsonify({"status": "processed"}), 200
                    
            except Exception as e:
                logger.error(f"Error in webhook: {str(e)}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/conversations/<conversation_id>/reply', methods=['POST'])
        def reply_to_conversation(conversation_id):
            """Envía respuesta a una conversación específica"""
            try:
                data = request.get_json()
                message = data.get('message')
                
                if not message:
                    return jsonify({"error": "Message required"}), 400
                
                # Validar que el mensaje sea solo texto
                if not isinstance(message, str) or len(message.strip()) == 0:
                    return jsonify({"error": "Message must be non-empty text"}), 400
                
                logger.info(f"Replying to conversation {conversation_id}: {message[:50]}...")
                
                # Obtener datos de la conversación del backend
                conversation_response = self.backend_client.get_conversation_details(conversation_id)
                
                if not conversation_response.get('success'):
                    return jsonify({
                        "success": False,
                        "error": "Conversation not found"
                    }), 404
                
                conversation = conversation_response.get('conversation')
                contact_phone = conversation.get('contactPhone')
                
                if not contact_phone:
                    return jsonify({
                        "success": False,
                        "error": "Contact phone not found in conversation"
                    }), 400
                
                # Enviar mensaje a WhatsApp
                result = self.whatsapp_service.send_message(contact_phone, message)
                
                if result.get('success'):
                    # Guardar mensaje en el backend
                    message_data = {
                        'conversationId': conversation_id,
                        'content': message,
                        'direction': 'outbound',
                        'timestamp': datetime.now().isoformat(),
                        'messageId': result.get('message_id')
                    }
                    
                    self.backend_client.save_message(message_data)
                    
                    logger.info(f"Reply sent successfully to {contact_phone}")
                    
                    return jsonify({
                        "success": True,
                        "message": "Reply sent successfully",
                        "message_id": result.get('message_id'),
                        "conversation_id": conversation_id
                    })
                else:
                    return jsonify({
                        "success": False,
                        "error": result.get('error', 'Failed to send message')
                    }), 500
                    
            except Exception as e:
                logger.error(f"Error replying to conversation: {str(e)}")
                return jsonify({"error": str(e)}), 500
    
    def run(self):
        """Ejecuta el microservicio"""
        self.app.run(
            host='0.0.0.0',
            port=self.config.web.port,
            debug=False  # Microservicio siempre en modo producción
        )