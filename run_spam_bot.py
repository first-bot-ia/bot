#!/usr/bin/env python3
"""
🚀 Script Principal - Bot de Spam Masivo con Twilio Sandbox
Ejecuta el servidor web completo para gestionar envíos masivos
"""

import os
import sys
import subprocess
import threading
import time
from pathlib import Path

def check_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    try:
        import twilio
        import flask
        import flask_cors
        import dotenv
        print("✅ Todas las dependencias están instaladas")
        return True
    except ImportError as e:
        print(f"❌ Dependencia faltante: {e}")
        print("💡 Ejecuta: pip install -r requirements_spam.txt")
        return False

def check_environment():
    """Verifica que las variables de entorno estén configuradas"""
    try:
        from dotenv import load_dotenv
        load_dotenv('.environment')
        
        required_vars = [
            'TWILIO_ACCOUNT_SID',
            'TWILIO_AUTH_TOKEN',
            'TWILIO_WHATSAPP_NUMBER'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var) or os.getenv(var) == 'your_account_sid_here':
                missing_vars.append(var)
        
        if missing_vars:
            print("❌ Variables de entorno faltantes o mal configuradas:")
            for var in missing_vars:
                print(f"   - {var}")
            print("\n📝 Instrucciones:")
            print("1. Ve a https://console.twilio.com/")
            print("2. Copia tu Account SID y Auth Token")
            print("3. Edita el archivo .environment")
            print("4. Ve a WhatsApp Sandbox: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn")
            return False
        
        print("✅ Variables de entorno configuradas correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error verificando entorno: {e}")
        return False

def test_twilio_connection():
    """Prueba la conexión con Twilio"""
    try:
        from spam_bot_service_pg import spam_service
        result = spam_service.test_conexion()
        
        if result['success']:
            print("✅ Conexión con Twilio exitosa")
            print(f"   - Cuenta: {result.get('account_name', 'N/A')}")
            print(f"   - Estado: {result.get('status', 'N/A')}")
            return True
        else:
            print(f"❌ Error conectando con Twilio: {result['message']}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando conexión: {e}")
        return False

def check_ngrok():
    """Verifica si ngrok está disponible"""
    if os.path.exists("ngrok.exe"):
        print("✅ ngrok está instalado localmente")
        return True
    
    # Buscar ngrok en PATH
    try:
        subprocess.run(["ngrok", "--version"], capture_output=True, check=True)
        print("✅ ngrok está disponible en PATH")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️ ngrok no encontrado")
        print("💡 Ejecuta: python install_ngrok.py")
        return False

def start_webhook_server():
    """Inicia el servidor de webhooks"""
    try:
        from webhook_server import app
        print("🌐 Iniciando servidor de webhooks en puerto 5000...")
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,  # Sin debug para evitar restart automático
            use_reloader=False
        )
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")

def start_web_interface():
    """Inicia la interfaz web"""
    try:
        from spam_bot_web import app
        print("🎨 Iniciando interfaz web en puerto 5001...")
        app.run(
            host='0.0.0.0',
            port=5001,
            debug=False,
            use_reloader=False
        )
    except Exception as e:
        print(f"❌ Error iniciando interfaz web: {e}")

def get_ngrok_url():
    """Obtiene la URL de ngrok si está disponible"""
    try:
        import requests
        response = requests.get("http://localhost:4040/api/tunnels", timeout=2)
        data = response.json()
        
        for tunnel in data.get('tunnels', []):
            if tunnel.get('config', {}).get('addr') == 'http://localhost:5000':
                return tunnel['public_url']
        return None
    except:
        return None

def main():
    """Función principal"""
    print("🚀 Bot de Spam Masivo - Twilio Sandbox")
    print("=" * 50)
    
    # Verificar dependencias
    if not check_dependencies():
        return
    
    # Verificar configuración
    if not check_environment():
        return
    
    # Probar conexión con Twilio
    if not test_twilio_connection():
        return
    
    # Verificar ngrok
    ngrok_available = check_ngrok()
    
    print("\n" + "=" * 50)
    print("🎉 ¡Sistema listo para iniciar!")
    print("=" * 50)
    
    # Mostrar URLs importantes
    print("\n📍 URLs del sistema:")
    print("   - Webhook: http://localhost:5000/whatsapp/webhook")
    print("   - Interfaz web: http://localhost:5001")
    print("   - Estado: http://localhost:5000/test")
    
    if ngrok_available:
        print("\n📱 Para exponer al internet:")
        print("   1. Ejecuta en otra terminal: ./ngrok.exe http 5000")
        print("   2. Copia la URL de ngrok")
        print("   3. Ve a Twilio Console > WhatsApp Sandbox")
        print("   4. Pega la URL + '/whatsapp/webhook' en 'When a message comes in'")
    
    print("\n🎯 Instrucciones de uso:")
    print("   1. Abre http://localhost:5001 en tu navegador")
    print("   2. Ve a la pestaña 'Clientes' para agregar números")
    print("   3. En 'Enviar Spam' selecciona un template")
    print("   4. ¡Envía mensajes masivos!")
    
    print("\n⚠️ IMPORTANTE:")
    print("   - Los números deben unirse al sandbox primero")
    print("   - Envía 'join [tu-keyword]' al +1 415 523 8886")
    print("   - Solo funciona con números que se unieron al sandbox")
    
    print("\n🚀 Iniciando servidores...")
    
    # Iniciar servidor de webhooks en un hilo separado
    webhook_thread = threading.Thread(target=start_webhook_server, daemon=True)
    webhook_thread.start()
    
    # Esperar un poco para que el servidor se inicie
    time.sleep(2)
    
    # Mostrar URL de ngrok si está disponible
    ngrok_url = get_ngrok_url()
    if ngrok_url:
        print(f"\n🌐 ngrok URL disponible: {ngrok_url}")
        print(f"   Webhook URL para Twilio: {ngrok_url}/whatsapp/webhook")
    
    # Iniciar interfaz web (principal)
    print("\n🎨 Iniciando interfaz web...")
    try:
        start_web_interface()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Cerrando sistema!")
        print("¡Gracias por usar el Bot de Spam Masivo!")

if __name__ == "__main__":
    main() 