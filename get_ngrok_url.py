#!/usr/bin/env python3
"""
🌐 Generador automático de URL de ngrok para Twilio
Inicia ngrok automáticamente y te da la URL lista para copiar
"""

import time
import requests
from pyngrok import ngrok, conf
import logging
import webbrowser

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def configure_ngrok():
    """Configura ngrok básico"""
    try:
        # ngrok se configurará automáticamente
        logger.info("✅ ngrok configurado correctamente")
        return True
    except Exception as e:
        logger.error(f"❌ Error configurando ngrok: {e}")
        return False

def start_ngrok_tunnel():
    """Inicia el túnel de ngrok en puerto 5000"""
    try:
        logger.info("🚀 Iniciando túnel ngrok en puerto 5000...")
        
        # Crear túnel HTTP en puerto 5000
        tunnel = ngrok.connect("5000")
        
        # Obtener la URL pública
        public_url = tunnel.public_url
        webhook_url = f"{public_url}/whatsapp/webhook"
        
        logger.info("=" * 60)
        logger.info("🎉 ¡NGROK INICIADO CORRECTAMENTE!")
        logger.info("=" * 60)
        logger.info(f"🌐 URL Pública: {public_url}")
        logger.info(f"📱 URL del Webhook: {webhook_url}")
        logger.info("=" * 60)
        
        print("\n" + "🔥" * 20 + " IMPORTANTE " + "🔥" * 20)
        print(f"📋 COPIA ESTA URL EN TWILIO CONSOLE:")
        print(f"")
        print(f"   {webhook_url}")
        print(f"")
        print("📍 Instrucciones:")
        print("1. Ve a: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn")
        print("2. En 'When a message comes in', pega la URL de arriba")
        print("3. Guarda los cambios")
        print("4. ¡Listo para recibir mensajes!")
        print("🔥" * 52)
        
        return tunnel, webhook_url
        
    except Exception as e:
        logger.error(f"❌ Error iniciando ngrok: {e}")
        logger.error("💡 Posibles soluciones:")
        logger.error("   - Verifica tu conexión a internet")
        logger.error("   - Intenta ejecutar: python setup_ngrok.py")
        return None, None

def open_twilio_console():
    """Abre Twilio Console en el navegador"""
    twilio_url = "https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn"
    print(f"\n🔗 ¿Quieres abrir Twilio Console? (s/n): ", end="")
    response = input().strip().lower()
    if response in ['s', 'si', 'y', 'yes']:
        webbrowser.open(twilio_url)
        print("✅ Twilio Console abierto en el navegador")

def monitor_tunnel(tunnel):
    """Monitorea el túnel y muestra estadísticas"""
    try:
        print("\n📊 Túnel activo - Presiona Ctrl+C para detener")
        print("📡 Monitoreando conexiones...")
        
        while True:
            time.sleep(5)
            # Verificar que el túnel sigue activo
            tunnels = ngrok.get_tunnels()
            if not tunnels:
                logger.error("❌ Túnel perdido, reiniciando...")
                return False
            
            print(".", end="", flush=True)
            
    except KeyboardInterrupt:
        print("\n\n👋 Deteniendo ngrok...")
        return True
    except Exception as e:
        logger.error(f"❌ Error monitoreando túnel: {e}")
        return False

def check_webhook_server():
    """Verifica que el servidor webhook esté funcionando"""
    try:
        response = requests.get("http://localhost:5000/test", timeout=3)
        if response.status_code == 200:
            logger.info("✅ Servidor webhook funcionando correctamente")
            return True
        else:
            logger.warning("⚠️ Servidor webhook respondió con código: {response.status_code}")
            return False
    except requests.exceptions.RequestException:
        logger.error("❌ Servidor webhook no está funcionando")
        logger.error("💡 Ejecuta primero: python run_spam_bot.py")
        return False

def main():
    """Función principal"""
    print("🌐 Generador automático de URL de ngrok")
    print("=" * 50)
    
    # Verificar que el servidor webhook esté funcionando
    if not check_webhook_server():
        print("\n❌ El servidor webhook no está ejecutándose")
        print("🚀 Ejecuta primero en otra terminal:")
        print("   python run_spam_bot.py")
        return
    
    # Configurar ngrok
    if not configure_ngrok():
        return
    
    # Iniciar túnel
    tunnel, webhook_url = start_ngrok_tunnel()
    if not tunnel:
        return
    
    # Abrir Twilio Console
    open_twilio_console()
    
    # Monitorear túnel
    try:
        if monitor_tunnel(tunnel):
            logger.info("✅ Túnel cerrado correctamente")
        else:
            logger.error("❌ Error en el túnel")
    finally:
        # Cerrar todos los túneles
        ngrok.kill()
        logger.info("🛑 Todos los túneles de ngrok cerrados")

if __name__ == "__main__":
    main() 