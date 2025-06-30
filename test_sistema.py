#!/usr/bin/env python3
"""
Prueba simple del sistema DDD
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('.environment')

def test_system():
    """Prueba simple del sistema"""
    try:
        print("🧪 Probando sistema DDD...")
        
        # 1. Probar configuración
        print("1️⃣ Probando configuración...")
        from config.settings import AppConfig
        
        config = AppConfig.from_env()
        print(f"   ✅ Base de datos: {config.database.url[:30]}...")
        print(f"   ✅ Twilio SID: {config.twilio.account_sid[:10]}...")
        print(f"   ✅ Puerto web: {config.web.port}")
        
        # 2. Probar repositorio PostgreSQL
        print("2️⃣ Probando repositorio PostgreSQL...")
        from infrastructure.persistence.postgresql_client_repository import PostgreSQLClientRepository
        
        repo = PostgreSQLClientRepository(config.database.url)
        active_count = repo.count_active()
        print(f"   ✅ Clientes activos: {active_count}")
        
        # 3. Probar caso de uso
        print("3️⃣ Probando casos de uso...")
        from application.use_cases.add_client_use_case import AddClientUseCase
        
        add_client_uc = AddClientUseCase(repo)
        result = add_client_uc.execute(
            nombre="Test Cliente",
            telefono="+51999000000",
            email="test@example.com"
        )
        print(f"   ✅ Agregar cliente: {result['message']}")
        
        # 4. Probar servicio Twilio
        print("4️⃣ Probando servicio Twilio...")
        from infrastructure.external_services.twilio_service import TwilioWhatsAppService
        
        twilio_service = TwilioWhatsAppService(config.twilio)
        templates = twilio_service.get_available_templates()
        print(f"   ✅ Templates disponibles: {len(templates)}")
        
        # 5. Conexión Twilio
        print("5️⃣ Probando conexión Twilio...")
        twilio_ok, twilio_msg = twilio_service.test_connection()
        print(f"   {'✅' if twilio_ok else '❌'} Twilio: {twilio_msg}")
        
        print("\n🎉 ¡Sistema DDD funcionando correctamente!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error en el sistema: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_system() 