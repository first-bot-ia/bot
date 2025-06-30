#!/usr/bin/env python3
"""
Configuración de ngrok para el webhook de Twilio
"""
import subprocess
import time
import requests
import json

def get_ngrok_url():
    """Obtiene la URL pública de ngrok"""
    try:
        print("🔍 Obteniendo URL pública de ngrok...")
        
        # Esperar un poco para que ngrok se inicie
        time.sleep(2)
        
        # Consultar API local de ngrok
        response = requests.get('http://localhost:4040/api/tunnels')
        
        if response.status_code == 200:
            tunnels = response.json()
            
            for tunnel in tunnels.get('tunnels', []):
                if tunnel.get('proto') == 'https':
                    public_url = tunnel.get('public_url')
                    print(f"✅ URL pública encontrada: {public_url}")
                    return public_url
            
            print("❌ No se encontró túnel HTTPS")
            return None
        else:
            print(f"❌ Error consultando ngrok API: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error obteniendo URL: {e}")
        return None

def update_webhook_url(ngrok_url):
    """Actualiza el webhook URL en las variables de entorno"""
    try:
        webhook_url = f"{ngrok_url}/whatsapp/webhook"
        
        print(f"🔧 URL del webhook: {webhook_url}")
        print("\n📋 CONFIGURACIÓN EN TWILIO CONSOLE:")
        print("=" * 50)
        print("1. Ve a: https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox")
        print("2. En 'When a message comes in':")
        print(f"   URL: {webhook_url}")
        print("   HTTP: POST")
        print("3. Guarda los cambios")
        print("=" * 50)
        
        # Actualizar archivo .environment
        with open('.environment', 'r') as f:
            content = f.read()
        
        # Reemplazar webhook URL
        import re
        new_content = re.sub(
            r'WEBHOOK_URL=.*',
            f'WEBHOOK_URL={webhook_url}',
            content
        )
        
        with open('.environment', 'w') as f:
            f.write(new_content)
        
        print(f"✅ Archivo .environment actualizado con webhook URL")
        
    except Exception as e:
        print(f"❌ Error actualizando webhook: {e}")

def main():
    """Función principal"""
    print("🚀 Configurador de ngrok para Twilio")
    print("=" * 40)
    
    print("📋 INSTRUCCIONES:")
    print("1. Abre otra terminal")
    print("2. Ejecuta: ngrok http 5000")
    print("3. Deja ngrok corriendo")
    print("4. Vuelve aquí y presiona ENTER")
    print("=" * 40)
    
    input("Presiona ENTER cuando ngrok esté ejecutándose...")
    
    # Obtener URL de ngrok
    ngrok_url = get_ngrok_url()
    
    if ngrok_url:
        update_webhook_url(ngrok_url)
        print("\n🎉 ¡Configuración completada!")
        print(f"🌐 Tu aplicación está disponible en: {ngrok_url}")
        print("📱 Configura el webhook en Twilio Console con las instrucciones mostradas")
    else:
        print("\n❌ No se pudo obtener la URL de ngrok")
        print("🔧 Verifica que ngrok esté ejecutándose con: ngrok http 5000")

if __name__ == "__main__":
    main() 