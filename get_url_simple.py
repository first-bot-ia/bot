#!/usr/bin/env python3
"""
🔥 DETECTOR AUTOMÁTICO DE URL DE NGROK
Script súper simple que detecta tu URL de ngrok y te la da lista para copiar
"""

import requests
import time
import webbrowser
import os
import json

def detect_ngrok_url():
    """Detecta automáticamente la URL de ngrok"""
    try:
        print("🔍 Buscando túnel de ngrok...")
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
        
        return webhook_url
        
    except requests.exceptions.RequestException as e:
        print("❌ Error conectando con ngrok")
        print(f"💡 Error: {e}")
        print("🔧 Asegúrate de que ngrok esté ejecutándose en puerto 4040")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None

def open_twilio_console():
    """Abre Twilio Console automáticamente"""
    print("\n🔗 ¿Abrir Twilio Console en el navegador? (s/n): ", end="")
    response = input().strip().lower()
    if response in ['s', 'si', 'y', 'yes', '']:
        webbrowser.open("https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn")
        print("✅ Twilio Console abierto")

def show_manual_instructions():
    """Muestra instrucciones manuales"""
    print("\n📋 INSTRUCCIONES PARA INICIAR NGROK:")
    print("=" * 50)
    print()
    print("🔸 OPCIÓN 1 - Descarga Manual:")
    print("   1. Ve a: https://ngrok.com/download")
    print("   2. Descarga 'Windows (64-bit)'")
    print("   3. Extrae 'ngrok.exe' en esta carpeta")
    print("   4. Ejecuta: ./ngrok.exe http 5000")
    print()
    print("🔸 OPCIÓN 2 - Instalación rápida:")
    print("   1. Ve a: https://ngrok.com/download")
    print("   2. Crea cuenta gratis")
    print("   3. Sigue las instrucciones de instalación")
    print("   4. Ejecuta: ngrok http 5000")
    print()
    print("💡 Después ejecuta este script de nuevo para obtener la URL")

def main():
    """Función principal"""
    print("🔥 DETECTOR AUTOMÁTICO DE URL DE NGROK")
    print("=" * 50)
    
    # Verificar que el servidor esté funcionando
    try:
        response = requests.get("http://localhost:5000/test", timeout=2)
        if response.status_code == 200:
            print("✅ Servidor webhook funcionando en puerto 5000")
        else:
            print("⚠️ Servidor webhook no responde correctamente")
    except:
        print("❌ EJECUTA PRIMERO: python run_spam_bot.py")
        print("   (En otra terminal)")
        return
    
    # Detectar URL de ngrok
    webhook_url = detect_ngrok_url()
    
    if webhook_url:
        # URL encontrada
        open_twilio_console()
        
        print("\n📊 Monitoreo continuo...")
        print("💡 Presiona Ctrl+C para salir")
        
        try:
            while True:
                time.sleep(10)
                # Verificar que ngrok sigue activo
                try:
                    requests.get("http://localhost:4040/api/tunnels", timeout=1)
                    print(".", end="", flush=True)
                except:
                    print("\n⚠️ ngrok se desconectó")
                    break
        except KeyboardInterrupt:
            print("\n👋 ¡Monitor detenido!")
    
    else:
        # No se encontró URL
        print("\n❌ No se detectó ngrok ejecutándose")
        show_manual_instructions()
        
        print("\n🔗 ¿Quieres abrir la página de descarga? (s/n): ", end="")
        response = input().strip().lower()
        if response in ['s', 'si', 'y', 'yes']:
            webbrowser.open("https://ngrok.com/download")
            print("✅ Página de descarga abierta")

if __name__ == "__main__":
    main() 