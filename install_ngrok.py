#!/usr/bin/env python3
"""
🚀 Instalador automático de ngrok para Windows
Descarga e instala ngrok para exponer el webhook al internet
"""

import os
import sys
import requests
import zipfile
import shutil
from pathlib import Path

def download_ngrok():
    """Descarga ngrok para Windows"""
    print("📥 Descargando ngrok para Windows...")
    
    # URL de descarga para Windows 64-bit
    ngrok_url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
    
    try:
        # Descargar el archivo
        response = requests.get(ngrok_url, stream=True)
        response.raise_for_status()
        
        # Guardar el archivo zip
        zip_path = "ngrok.zip"
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("✅ Descarga completada")
        return zip_path
        
    except Exception as e:
        print(f"❌ Error descargando ngrok: {e}")
        return None

def extract_ngrok(zip_path):
    """Extrae ngrok del zip"""
    print("📦 Extrayendo ngrok...")
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # Limpiar el zip
        os.remove(zip_path)
        
        print("✅ Extracción completada")
        return True
        
    except Exception as e:
        print(f"❌ Error extrayendo ngrok: {e}")
        return False

def add_to_path():
    """Añade ngrok al PATH del sistema"""
    current_dir = os.getcwd()
    ngrok_path = os.path.join(current_dir, "ngrok.exe")
    
    if os.path.exists(ngrok_path):
        print(f"✅ ngrok instalado en: {ngrok_path}")
        print("\n🔧 Para usar ngrok globalmente, añade esta carpeta a tu PATH:")
        print(f"   {current_dir}")
        print("\n📱 Para probar la instalación, ejecuta:")
        print(f"   {ngrok_path} --version")
        return True
    else:
        print("❌ No se pudo encontrar ngrok.exe")
        return False

def test_ngrok():
    """Prueba si ngrok funciona"""
    ngrok_path = "./ngrok.exe"
    
    try:
        import subprocess
        result = subprocess.run([ngrok_path, "--version"], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print(f"✅ ngrok funciona correctamente: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Error ejecutando ngrok: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando ngrok: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Instalador de ngrok para Twilio Webhook")
    print("=" * 50)
    
    # Verificar si ya existe
    if os.path.exists("ngrok.exe"):
        print("✅ ngrok ya está instalado")
        if test_ngrok():
            print("\n🎉 Instalación verificada correctamente")
            return
    
    # Descargar ngrok
    zip_path = download_ngrok()
    if not zip_path:
        return
    
    # Extraer ngrok
    if not extract_ngrok(zip_path):
        return
    
    # Verificar instalación
    if add_to_path() and test_ngrok():
        print("\n🎉 ¡ngrok instalado correctamente!")
        print("\n📝 Próximos pasos:")
        print("1. Ejecuta: python run_spam_bot.py")
        print("2. En otra terminal: ./ngrok.exe http 5000")
        print("3. Copia la URL de ngrok a Twilio Console")
    else:
        print("\n❌ Hubo un problema con la instalación")

if __name__ == "__main__":
    main() 