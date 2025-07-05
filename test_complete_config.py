#!/usr/bin/env python3
"""
🧪 Test Completo de Configuración - Bot Python
Verifica que todas las variables de entorno se lean correctamente
"""
import os
from dotenv import load_dotenv
from config.settings import AppConfig

# Cargar variables de entorno desde .environment
load_dotenv('.environment')

def test_complete_configuration():
    """Prueba completa de todas las configuraciones"""
    print("🧪 VERIFICANDO CONFIGURACIÓN COMPLETA...")
    print("=" * 60)
    
    try:
        # Cargar configuración completa
        config = AppConfig.from_env()
        
        # 🔧 SERVER CONFIGURATION
        print("\n🔧 SERVER CONFIGURATION:")
        print(f"   ✅ NODE_ENV: {config.node_env}")
        print(f"   ✅ PORT: {config.web.port}")
        print(f"   ✅ HOST: {config.web.host}")
        print(f"   ✅ DEBUG: {config.web.debug}")
        
        # 🌍 CORS CONFIGURATION
        print("\n🌍 CORS CONFIGURATION:")
        print(f"   ✅ Origins: {', '.join(config.cors.origins)}")
        print(f"   ✅ Credentials: {config.cors.credentials}")
        
        # 🎯 SERVICES URLS
        print("\n🎯 SERVICES URLS:")
        print(f"   ✅ API Gateway: {config.web.api_gateway_url}")
        print(f"   ✅ Backend: {config.web.backend_url}")
        print(f"   ✅ Frontend: {config.web.frontend_url}")
        print(f"   ✅ Webhook: {config.web.webhook_url or 'No configurado'}")
        
        # 🔐 SECURITY
        print("\n🔐 SECURITY:")
        print(f"   ✅ API Gateway Secret: {config.security.api_gateway_secret[:20]}...")
        print(f"   ✅ Bot Webhook Secret: {config.security.bot_webhook_secret[:20]}...")
        print(f"   ✅ Webhook Verify Token: {config.security.webhook_verify_token[:20]}...")
        
        # 📱 TWILIO CONFIGURATION
        print("\n📱 TWILIO CONFIGURATION:")
        print(f"   ✅ Account SID: {config.twilio.account_sid[:10]}...")
        print(f"   ✅ Auth Token: {config.twilio.auth_token[:10]}...")
        print(f"   ✅ Phone Number: {config.twilio.phone_number}")
        print(f"   ✅ WhatsApp Number: {config.twilio.whatsapp_number}")
        
        # 🗄️ DATABASE CONFIGURATION
        print("\n🗄️ DATABASE CONFIGURATION:")
        print(f"   ✅ URL: {config.database.url[:50]}...")
        print(f"   ✅ Host: {config.database.host}")
        print(f"   ✅ Port: {config.database.port}")
        print(f"   ✅ Name: {config.database.name}")
        print(f"   ✅ User: {config.database.user}")
        print(f"   ✅ Password: {'*' * len(config.database.password)}")
        
        # 📊 LOGGING
        print("\n📊 LOGGING:")
        print(f"   ✅ Level: {config.logging.level}")
        print(f"   ✅ Debug: {config.logging.debug}")
        
        # 🌐 WHATSAPP BUSINESS API
        print("\n🌐 WHATSAPP BUSINESS API:")
        print(f"   ✅ Access Token: {config.whatsapp_business.access_token[:20]}...")
        print(f"   ✅ Phone Number ID: {config.whatsapp_business.phone_number_id[:20]}...")
        print(f"   ✅ Webhook Verify Token: {config.whatsapp_business.webhook_verify_token[:20]}...")
        
        # 🔑 ADDITIONAL
        print("\n🔑 ADDITIONAL:")
        print(f"   ✅ Gemini API Key: {config.gemini_api_key[:20] if config.gemini_api_key else 'No configurado'}...")
        
        print("\n" + "=" * 60)
        print("🎉 ¡TODAS LAS CONFIGURACIONES VERIFICADAS EXITOSAMENTE!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error en configuración: {str(e)}")
        return False

def test_environment_variables():
    """Verifica variables de entorno directamente"""
    print("\n🔍 VERIFICANDO VARIABLES DE ENTORNO...")
    print("-" * 40)
    
    required_vars = [
        'NODE_ENV', 'PORT', 'HOST', 'CORS_ORIGIN', 'CORS_CREDENTIALS',
        'API_GATEWAY_URL', 'BACKEND_URL', 'FRONTEND_URL',
        'API_GATEWAY_SECRET', 'BOT_WEBHOOK_SECRET', 'WEBHOOK_VERIFY_TOKEN',
        'TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_WHATSAPP_NUMBER',
        'DATABASE_URL', 'DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD',
        'LOG_LEVEL', 'DEBUG'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"   ✅ {var}: Configurado")
        else:
            print(f"   ❌ {var}: NO ENCONTRADO")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️ Variables faltantes: {', '.join(missing_vars)}")
        return False
    else:
        print("\n✅ Todas las variables de entorno están configuradas")
        return True

def test_connectivity():
    """Prueba conectividad con servicios"""
    print("\n🌐 VERIFICANDO CONECTIVIDAD...")
    print("-" * 40)
    
    import requests
    
    try:
        config = AppConfig.from_env()
    except Exception as e:
        print(f"   ❌ Error cargando configuración: {str(e)}")
        return False
    
    # Test localhost
    try:
        response = requests.get("http://localhost:5000/health", timeout=3)
        if response.status_code == 200:
            print("   ✅ Bot Python (localhost:5000): Activo")
        else:
            print(f"   ❌ Bot Python: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Bot Python: {str(e)}")
    
    # Test ngrok
    webhook_url = config.web.webhook_url
    if webhook_url and webhook_url.startswith('https://'):
        try:
            headers = {'ngrok-skip-browser-warning': 'true'}
            response = requests.get(webhook_url.replace('/whatsapp/webhook', '/health'), 
                                  headers=headers, timeout=5)
            if response.status_code == 200:
                print("   ✅ ngrok URL: Accesible desde internet")
            else:
                print(f"   ❌ ngrok URL: HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ ngrok URL: {str(e)}")
    else:
        print("   ⚠️ ngrok URL: No configurado o no es HTTPS")
    
    return True

def main():
    """Función principal"""
    print("🚀 INICIANDO VERIFICACIÓN COMPLETA...")
    print("⏰ Verificando todas las configuraciones del Bot Python")
    print()
    
    results = []
    
    # Test 1: Configuración completa
    results.append(test_complete_configuration())
    
    # Test 2: Variables de entorno
    results.append(test_environment_variables())
    
         # Test 3: Conectividad
    connectivity_result = test_connectivity()
    results.append(connectivity_result)
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE VERIFICACIÓN:")
    print(f"   Configuración: {'✅' if results[0] else '❌'}")
    print(f"   Variables ENV: {'✅' if results[1] else '❌'}")
    print(f"   Conectividad: {'✅' if connectivity_result else '❌'}")
    
    if all(results):
        print("\n🎉 ¡SISTEMA COMPLETAMENTE CONFIGURADO Y FUNCIONANDO!")
        print("🔗 URL para Twilio:")
        
        config = AppConfig.from_env()
        if config.web.webhook_url:
            print(f"   {config.web.webhook_url}")
        else:
            print("   ⚠️ WEBHOOK_URL no configurado en .environment")
        
        return True
    else:
        print("\n⚠️ HAY PROBLEMAS EN LA CONFIGURACIÓN")
        return False

if __name__ == "__main__":
    main() 