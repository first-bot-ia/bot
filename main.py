#!/usr/bin/env python3
"""
Punto de entrada principal de la aplicación Bot de Spam WhatsApp
Implementación con Domain-Driven Design (DDD)
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
    """Función principal de la aplicación"""
    try:
        from config.settings import AppConfig
        
        # Cargar configuración
        config = AppConfig.from_env()
        
        print("🚀 Iniciando Bot de Spam WhatsApp con DDD")
        print("=" * 50)
        print(f"📱 Twilio: {config.twilio.whatsapp_number}")
        print(f"🗄️ Base de datos: PostgreSQL")
        print(f"🌐 Puerto web: {config.web.port}")
        print(f"🔧 Debug: {config.web.debug}")
        print("=" * 50)
        
        # Inicializar arquitectura DDD
        from infrastructure.web.api_controller import WhatsAppBotAPI
        
        print("🏗️ Inicializando arquitectura DDD...")
        
        # Configurar datos iniciales si es necesario
        from setup_initial_data import setup_initial_data
        setup_initial_data()
        
        # Crear controlador principal con dependencias inyectadas
        api_controller = WhatsAppBotAPI(config)
        
        print("✅ Iniciando servidor web con DDD...")
        
        # Ejecutar servidor
        api_controller.run()
        
    except Exception as e:
        print(f"❌ Error iniciando aplicación: {e}")
        logging.error(f"Error en main: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main() 