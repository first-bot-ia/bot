#!/usr/bin/env python3
"""
Script para configurar datos iniciales del sistema
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('.environment')

def setup_initial_data():
    """Configura datos iniciales del sistema"""
    try:
        from config.settings import AppConfig
        from infrastructure.persistence.postgresql_client_repository import PostgreSQLClientRepository
        from application.use_cases.add_client_use_case import AddClientUseCase
        
        print("🔧 Configurando datos iniciales...")
        
        # Cargar configuración
        config = AppConfig.from_env()
        
        # Inicializar repositorio y caso de uso
        client_repository = PostgreSQLClientRepository(config.database.url)
        add_client_use_case = AddClientUseCase(client_repository)
        
        # Clientes de ejemplo
        sample_clients = [
            {
                'nombre': 'Jair Kiwipay',
                'telefono': '+51960454985',  # Este número está en el sandbox
                'email': 'jair.kiwipay@alesse.com'
            },
            {
                'nombre': 'María García',
                'telefono': '+51999234567',
                'email': 'maria.garcia@example.com'
            },
            {
                'nombre': 'Carlos López',
                'telefono': '+51999345678',
                'email': 'carlos.lopez@example.com'
            }
        ]
        
        print("👥 Agregando clientes de ejemplo...")
        
        for client_data in sample_clients:
            result = add_client_use_case.execute(
                nombre=client_data['nombre'],
                telefono=client_data['telefono'],
                email=client_data['email']
            )
            
            if result['success']:
                print(f"✅ Cliente agregado: {client_data['nombre']} - {client_data['telefono']}")
            else:
                if "ya existe" in result['message']:
                    print(f"ℹ️ Cliente ya existe: {client_data['nombre']}")
                else:
                    print(f"❌ Error agregando {client_data['nombre']}: {result['message']}")
        
        # Verificar estado final
        active_clients = client_repository.count_active()
        print(f"\n📊 Total clientes activos: {active_clients}")
        
        print("\n✅ Configuración inicial completada!")
        return True
        
    except Exception as e:
        print(f"❌ Error configurando datos iniciales: {e}")
        return False

if __name__ == "__main__":
    setup_initial_data() 