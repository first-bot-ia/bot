#!/usr/bin/env python3
"""
👥 Script para agregar clientes de prueba
Para probar las campañas masivas
"""

from whatsapp_native_service import whatsapp_native_service

def agregar_clientes_test():
    """Agrega clientes de prueba para campañas"""
    
    clientes_test = [
        ("Jair", "51965181346", "jair@test.com"),  # Ya existe
        ("María García", "51987654321", "maria@test.com"),
        ("Carlos López", "51976543210", "carlos@test.com"),
        ("Ana Rodríguez", "51965432109", "ana@test.com"),
        ("Luis Torres", "51954321098", "luis@test.com")
    ]
    
    print("👥 Agregando clientes de prueba...")
    print("=" * 40)
    
    for nombre, telefono, email in clientes_test:
        resultado = whatsapp_native_service.agregar_cliente(nombre, telefono, email)
        if resultado:
            print(f"✅ {nombre} - {telefono}")
        else:
            print(f"⚠️ {nombre} - {telefono} (ya existía)")
    
    # Mostrar resumen
    clientes = whatsapp_native_service.obtener_clientes_activos()
    print(f"\n📊 Total clientes activos: {len(clientes)}")
    
    print("\n🎯 Clientes para campañas:")
    for cliente in clientes:
        print(f"  - {cliente['nombre']}: {cliente['telefono']}")

if __name__ == "__main__":
    agregar_clientes_test() 