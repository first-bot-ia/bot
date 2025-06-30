#!/usr/bin/env python3
"""
📦 Instalador de Dependencias - Bot de Spam
Verifica e instala las dependencias necesarias
"""

import subprocess
import sys
import os

def install_package(package):
    """Instalar un paquete de Python"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_package(package):
    """Verificar si un paquete está instalado"""
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def main():
    """Función principal de instalación"""
    print("📦 INSTALADOR DE DEPENDENCIAS - BOT DE SPAM")
    print("=" * 50)
    
    # Lista de dependencias necesarias
    dependencies = [
        ("twilio", "twilio"),
        ("flask", "flask"),
        ("flask_cors", "flask-cors"),
        ("dotenv", "python-dotenv"),
        ("sqlite3", None)  # sqlite3 viene incluido con Python
    ]
    
    print("\n🔍 Verificando dependencias...")
    
    missing_packages = []
    
    for module_name, pip_name in dependencies:
        if module_name == "sqlite3":
            # sqlite3 viene incluido con Python
            print(f"✅ {module_name}: Incluido con Python")
            continue
            
        if check_package(module_name):
            print(f"✅ {module_name}: Instalado")
        else:
            print(f"❌ {module_name}: No encontrado")
            if pip_name:
                missing_packages.append(pip_name)
    
    if not missing_packages:
        print("\n🎉 ¡Todas las dependencias están instaladas!")
        print("\n🚀 COMANDOS DISPONIBLES:")
        print("  python test_spam_bot_simple.py  - Prueba básica")
        print("  python run_spam_bot.py         - Menú principal")
        return
    
    print(f"\n📥 Instalando {len(missing_packages)} dependencias faltantes...")
    
    for package in missing_packages:
        print(f"\n📦 Instalando {package}...")
        if install_package(package):
            print(f"✅ {package} instalado correctamente")
        else:
            print(f"❌ Error instalando {package}")
            print(f"💡 Intenta manualmente: pip install {package}")
    
    print("\n🔄 Verificando instalación final...")
    
    all_ok = True
    for module_name, _ in dependencies:
        if module_name == "sqlite3":
            continue
        if not check_package(module_name):
            print(f"❌ {module_name} sigue sin estar disponible")
            all_ok = False
    
    if all_ok:
        print("\n🎉 ¡Instalación completada exitosamente!")
        
        # Crear archivo requirements.txt si no existe
        if not os.path.exists("requirements_spam.txt"):
            with open("requirements_spam.txt", "w") as f:
                f.write("twilio>=8.0.0\n")
                f.write("flask>=2.0.0\n")
                f.write("flask-cors>=4.0.0\n")
                f.write("python-dotenv>=1.0.0\n")
            print("📝 Archivo requirements_spam.txt creado")
        
        print("\n🚀 COMANDOS DISPONIBLES:")
        print("  python test_spam_bot_simple.py  - Prueba básica")
        print("  python run_spam_bot.py         - Menú principal")
        print("\n📖 Lee README_BOT_SPAM.md para instrucciones completas")
        
    else:
        print("\n⚠️ Algunas dependencias no se pudieron instalar")
        print("💡 Intenta instalar manualmente:")
        for package in missing_packages:
            print(f"  pip install {package}")

if __name__ == "__main__":
    main() 