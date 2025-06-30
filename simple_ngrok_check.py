#!/usr/bin/env python3
import requests
import json

try:
    # Obtener información de túneles de ngrok
    response = requests.get("http://localhost:4040/api/tunnels")
    data = response.json()
    
    print("🌐 NGROK TUNNEL INFORMATION")
    print("=" * 50)
    
    if data.get('tunnels'):
        for tunnel in data['tunnels']:
            public_url = tunnel.get('public_url', '')
            proto = tunnel.get('proto', '')
            config = tunnel.get('config', {})
            addr = config.get('addr', '')
            
            print(f"📡 Protocolo: {proto}")
            print(f"🔗 URL Pública: {public_url}")
            print(f"🏠 Local: {addr}")
            
            if proto == 'https':
                webhook_url = f"{public_url}/whatsapp/webhook"
                print(f"")
                print("🔥 COPIA ESTA URL PARA TWILIO:")
                print(f"   {webhook_url}")
                print(f"")
                print("📋 INSTRUCCIONES:")
                print("1. Ve a: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn")
                print("2. En 'When a message comes in', pega la URL de arriba")
                print("3. Guarda los cambios")
                print("4. ¡Listo!")
            
            print("-" * 50)
    else:
        print("❌ No se encontraron túneles activos")
        print("💡 Asegúrate de que ngrok esté ejecutándose")

except requests.exceptions.RequestException as e:
    print("❌ Error conectando con ngrok")
    print(f"💡 Error: {e}")
    print("🔧 Asegúrate de que ngrok esté ejecutándose en puerto 4040")
except Exception as e:
    print(f"❌ Error inesperado: {e}") 