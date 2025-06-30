#!/usr/bin/env python3
"""
🔍 Monitor para detectar URL de ngrok
Ejecuta este script DESPUÉS de iniciar ngrok
"""

import requests
import time
import sys

def check_ngrok():
    """Verifica si ngrok está corriendo y obtiene el URL"""
    try:
        response = requests.get("http://localhost:4040/api/tunnels", timeout=2)
        tunnels = response.json()
        
        https_url = None
        for tunnel in tunnels.get('tunnels', []):
            if tunnel.get('proto') == 'https':
                https_url = tunnel.get('public_url')
                break
        
        if https_url:
            print("🎉 ¡NGROK DETECTADO!")
            print("=" * 50)
            print(f"🌐 Tu URL público: {https_url}")
            print()
            print("📋 COPIAR Y PEGAR EN TWILIO CONSOLE:")
            print("-" * 50)
            print("Webhook URL (When a message comes in):")
            print(f"   {https_url}/whatsapp/webhook")
            print()
            print("Status Callback URL:")
            print(f"   {https_url}/webhook/status")
            print()
            print("✅ ¡URLs listos para Twilio!")
            return True
        else:
            print("⚠️ Ngrok corriendo pero sin túnel HTTPS")
            return False
            
    except requests.exceptions.RequestException:
        print("❌ Ngrok no está corriendo en localhost:4040")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🔍 MONITOR DE NGROK")
    print("Esperando que inicies ngrok...")
    print("Presiona Ctrl+C para salir")
    print()
    
    try:
        while True:
            if check_ngrok():
                break
            else:
                print("⏳ Esperando ngrok... (verifica cada 3 segundos)")
                time.sleep(3)
    
    except KeyboardInterrupt:
        print("\n👋 Monitor detenido")
        sys.exit(0)

if __name__ == "__main__":
    main() 