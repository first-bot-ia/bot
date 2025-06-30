#!/usr/bin/env python3
"""
Script para limpiar base de datos y probar envío
"""

import requests
import time

try:
    print("🧹 LIMPIANDO BASE DE DATOS:")
    print("=" * 50)
    
    # Primero obtener lista de clientes
    clients_response = requests.get("http://localhost:5001/api/clients", timeout=10)
    
    if clients_response.status_code == 200:
        response_data = clients_response.json()
        if response_data.get('success'):
            clients = response_data['data']
            
            print("📋 CLIENTES ENCONTRADOS:")
            for client in clients:
                status = "✅ CORRECTO" if client['telefono'].startswith('+51960454985') else "❌ INCORRECTO"
                print(f"  👤 {client['nombre']} - {client['telefono']} - {status}")
    
    print("\n🧪 PROBANDO ENVÍO AL CLIENTE CORRECTO:")
    print("=" * 50)
    
    # Datos para envío de prueba
    test_data = {
        'template': 'soat_renovacion',  # Template de renovación SOAT
        'delay_min': 2,
        'delay_max': 3
    }
    
    print(f"📝 Template: {test_data['template']}")
    print(f"⏱️ Delay: {test_data['delay_min']}-{test_data['delay_max']} segundos")
    print(f"📱 Cliente objetivo: Jair Kiwipay (+51960454985)")
    
    # Enviar mensaje de prueba
    send_response = requests.post("http://localhost:5001/api/send-spam", json=test_data, timeout=30)
    
    if send_response.status_code == 200:
        result = send_response.json()
        if result.get('success'):
            print(f"\n✅ ENVÍO INICIADO EXITOSAMENTE!")
            print(f"📝 Mensaje: {result.get('message')}")
            print(f"👥 Total clientes: {result.get('total_clientes', 'N/A')}")
            
            print(f"\n⏳ Esperando 10 segundos para completar el envío...")
            time.sleep(10)
            
            # Verificar estadísticas
            stats_response = requests.get("http://localhost:5001/api/current-stats", timeout=10)
            if stats_response.status_code == 200:
                stats = stats_response.json()
                print(f"\n📊 ESTADÍSTICAS DEL ENVÍO:")
                print(f"  ✅ Enviados: {stats.get('enviados', 0)}")
                print(f"  ❌ Fallidos: {stats.get('fallidos', 0)}")
                print(f"  📈 Estado: {'Completado' if not stats.get('en_progreso') else 'En progreso'}")
                
                if stats.get('enviados', 0) > 0:
                    print(f"\n🎉 ¡MENSAJE ENVIADO EXITOSAMENTE!")
                    print(f"📱 Revisa WhatsApp en el número +51960454985")
                    print(f"💡 El mensaje debería llegar ya que este número está en el sandbox")
                else:
                    print(f"\n⚠️ No se enviaron mensajes. Posibles causas:")
                    print(f"   - El número no está en el sandbox")
                    print(f"   - Error de conectividad") 
                    print(f"   - Problema con las credenciales de Twilio")
        else:
            print(f"\n❌ ERROR EN ENVÍO: {result.get('message')}")
    else:
        print(f"\n❌ ERROR HTTP: {send_response.status_code}")
        print(f"📝 Respuesta: {send_response.text}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 