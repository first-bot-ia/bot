#!/usr/bin/env python3
"""
🌐 Servidor de Webhooks para WhatsApp
Recibe mensajes entrantes de Twilio WhatsApp
"""

from flask import Flask, request, Response
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    """Página de inicio"""
    return """
    <h1>🤖 Servidor de Webhooks - Alesse Connect</h1>
    <p>✅ Servidor activo y listo para recibir webhooks de Twilio</p>
    <p>📱 Endpoint para WhatsApp: <code>/whatsapp/webhook</code></p>
    <p>🕐 Hora actual: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
    """

@app.route("/whatsapp/webhook", methods=['POST', 'GET'])
def whatsapp_webhook():
    """Recibe webhooks de WhatsApp desde Twilio"""
    
    # Log de la petición recibida
    logger.info("📨 Webhook recibido de WhatsApp")
    logger.info(f"Método: {request.method}")
    logger.info(f"Headers: {dict(request.headers)}")
    
    if request.method == 'POST':
        # Obtener datos del mensaje
        from_number = request.form.get('From', '')
        to_number = request.form.get('To', '')
        message_body = request.form.get('Body', '')
        message_sid = request.form.get('MessageSid', '')
        
        logger.info(f"👤 De: {from_number}")
        logger.info(f"📱 Para: {to_number}")
        logger.info(f"💬 Mensaje: {message_body}")
        logger.info(f"🆔 SID: {message_sid}")
        
        # Respuesta automática simple
        twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>¡Hola! Recibí tu mensaje: "{message_body}". Este es un bot automático de Alesse Seguros 🤖</Message>
</Response>"""
        
        logger.info("📤 Enviando respuesta automática")
        return Response(twiml_response, mimetype='text/xml')
    
    else:
        # Para verificación de webhook (GET)
        return Response("✅ Webhook endpoint activo para WhatsApp", mimetype='text/plain')

@app.route("/webhook/status", methods=['POST'])
def status_webhook():
    """Recibe actualizaciones de estado de mensajes"""
    
    logger.info("📊 Actualización de estado recibida")
    
    message_sid = request.form.get('MessageSid', '')
    message_status = request.form.get('MessageStatus', '')
    to_number = request.form.get('To', '')
    
    logger.info(f"🆔 SID: {message_sid}")
    logger.info(f"📊 Estado: {message_status}")
    logger.info(f"📱 Para: {to_number}")
    
    return "OK"

@app.route("/test", methods=['GET', 'POST'])
def test_endpoint():
    """Endpoint de prueba"""
    return {
        "status": "✅ Activo",
        "timestamp": datetime.now().isoformat(),
        "method": request.method,
        "headers": dict(request.headers),
        "data": request.get_json() if request.is_json else dict(request.form)
    }

if __name__ == "__main__":
    print("🌐 Iniciando servidor de webhooks...")
    print("📍 Endpoints disponibles:")
    print("   - GET  / : Página de inicio")
    print("   - POST /whatsapp/webhook : Webhook principal")
    print("   - POST /webhook/status : Estado de mensajes")
    print("   - GET  /test : Endpoint de prueba")
    print()
    print("🚀 Servidor ejecutándose en http://localhost:5000")
    print("📱 Usa ngrok para exponer al internet")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    ) 