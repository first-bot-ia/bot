#!/usr/bin/env python3
"""
Script para verificar datos del cliente
"""

from spam_bot_service_pg import spam_service

try:
    clientes = spam_service.obtener_clientes_activos()
    
    print("📋 DATOS DEL CLIENTE:")
    print("=" * 40)
    
    for cliente in clientes:
        print(f"👤 Nombre: {cliente['nombre']}")
        print(f"📱 Teléfono: {cliente['telefono']}")
        print(f"📧 Email: {cliente.get('email', 'N/A')}")
        print(f"📊 Total enviados: {cliente.get('total_enviados', 0)}")
        print(f"🆔 ID: {cliente['id']}")
        print("-" * 40)
    
    # Verificar últimos envíos
    print("\n📨 ÚLTIMOS ENVÍOS:")
    print("=" * 40)
    
    historial = spam_service.obtener_historial_envios(limite=5)
    
    for envio in historial:
        print(f"👤 Cliente: {envio['nombre']}")
        print(f"📱 Teléfono: {envio['telefono']}")
        print(f"📝 Template: {envio['template_usado']}")
        print(f"✅ Estado: {envio['estado']}")
        print(f"⏰ Fecha: {envio['fecha_envio']}")
        if envio.get('parametros'):
            print(f"📋 Parámetros: {envio['parametros']}")
        print("-" * 40)

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 