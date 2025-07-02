#!/usr/bin/env python3
"""
WhatsApp Microservice - Especializado en Twilio Operations
Arquitectura de Microservicio Puro
"""
import os
import sys
import logging
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('.environment')

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def main():
    """Función principal del microservicio"""
    try:
        from config.settings import AppConfig
        
        # Cargar configuración
        config = AppConfig.from_env()
        
        print("🚀 Iniciando WhatsApp Microservice")
        print("=" * 50)
        print(f"📱 Twilio: {config.twilio.whatsapp_number}")
        print(f"🌐 Puerto: {config.web.port}")
        print(f"🔗 API Gateway: {config.web.api_gateway_url}")
        print(f"🤖 Modo: Microservicio Especializado")
        print("=" * 50)
        
        # Inicializar solo servicios esenciales
        from infrastructure.web.api_controller import WhatsAppBotAPI
        
        print("🏗️ Inicializando microservicio especializado...")
        
        # Crear controlador principal
        api_controller = WhatsAppBotAPI(config)
        
        print("✅ WhatsApp Microservice iniciado...")
        print("🎯 Especializaciones activas:")
        print("   • Envío directo via Twilio")
        print("   • Webhook adapter para API Gateway")
        print("   • Campañas masivas optimizadas")
        print("   • Health checks especializados")
        print("-" * 50)
        
        # Ejecutar microservicio
        api_controller.run()
        
    except Exception as e:
        print(f"❌ Error iniciando microservicio: {e}")
        logging.error(f"Error en main: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main() 