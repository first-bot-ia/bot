#!/usr/bin/env python3
"""
🚀 Configurador simple de ngrok
Instrucciones para instalar y configurar ngrok
"""

import os
import subprocess
import webbrowser

def check_ngrok():
    """Verifica si ngrok está instalado"""
    # Verificar si está en el directorio actual
    if os.path.exists("ngrok.exe"):
        print("✅ ngrok.exe encontrado en el directorio actual")
        return True
    
    # Verificar si está en PATH
    try:
        result = subprocess.run(["ngrok", "--version"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ ngrok está disponible en PATH")
            print(f"   Versión: {result.stdout.strip()}")
            return True
    except:
        pass
    
    return False

def show_manual_instructions():
    """Muestra instrucciones manuales para instalar ngrok"""
    print("\n📋 INSTALACIÓN MANUAL DE NGROK:")
    print("=" * 50)
    print("1. Ve a: https://ngrok.com/download")
    print("2. Descarga la versión para Windows")
    print("3. Extrae ngrok.exe en esta carpeta:")
    print(f"   {os.getcwd()}")
    print("4. Vuelve a ejecutar este script")
    
    print("\n🔗 ¿Quieres abrir la página de descarga? (s/n): ", end="")
    response = input().strip().lower()
    if response in ['s', 'si', 'y', 'yes']:
        webbrowser.open("https://ngrok.com/download")
        print("✅ Página de descarga abierta en el navegador")

def start_ngrok():
    """Inicia ngrok en puerto 5000"""
    ngrok_cmd = None
    
    if os.path.exists("ngrok.exe"):
        ngrok_cmd = "./ngrok.exe"
    else:
        ngrok_cmd = "ngrok"
    
    print(f"\n🚀 Iniciando ngrok en puerto 5000...")
    print("⚠️ IMPORTANTE: Deja esta ventana abierta")
    print("💡 Para detener, presiona Ctrl+C")
    print("🌐 La URL se mostrará en unos segundos...")
    
    try:
        subprocess.run([ngrok_cmd, "http", "5000"])
    except KeyboardInterrupt:
        print("\n👋 ngrok detenido")
    except Exception as e:
        print(f"\n❌ Error ejecutando ngrok: {e}")
        print("💡 Asegúrate de que ngrok.exe esté en esta carpeta")

def main():
    """Función principal"""
    print("🚀 Configurador de ngrok para Twilio WhatsApp")
    print("=" * 50)
    
    if check_ngrok():
        print("\n🎉 ¡ngrok está listo!")
        print("\n¿Qué quieres hacer?")
        print("1. Iniciar ngrok ahora")
        print("2. Solo mostrar instrucciones")
        print("3. Salir")
        
        choice = input("\nElige una opción (1-3): ").strip()
        
        if choice == "1":
            start_ngrok()
        elif choice == "2":
            show_ngrok_instructions()
        else:
            print("👋 ¡Hasta luego!")
    else:
        print("\n❌ ngrok no encontrado")
        show_manual_instructions()

def show_ngrok_instructions():
    """Muestra instrucciones de uso de ngrok"""
    print("\n📋 INSTRUCCIONES DE USO:")
    print("=" * 30)
    print("1. Ejecuta el bot:")
    print("   python run_spam_bot.py")
    print("\n2. En OTRA terminal, ejecuta ngrok:")
    print("   python setup_ngrok.py")
    print("   (elige opción 1)")
    print("\n3. Copia la URL que muestra ngrok (algo como:")
    print("   https://abc123.ngrok.io")
    print("\n4. Ve a Twilio Console:")
    print("   https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn")
    print("\n5. En 'When a message comes in', pega:")
    print("   https://abc123.ngrok.io/whatsapp/webhook")
    print("\n6. ¡Listo! Ya puedes enviar mensajes masivos")

if __name__ == "__main__":
    main() 