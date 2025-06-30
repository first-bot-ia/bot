#!/usr/bin/env python3
"""
Script para agregar cliente usando la API web
"""

import requests
import json

try:
    # Datos del cliente correcto
    client_data = {
        'nombre': 'Jair Kiwipay',
        'telefono': '+51960454985',
        'email': 'jair.kiwipay@example.com'
    }
    
    print("👤 AGREGANDO CLIENTE VÍA API WEB:")
    print("=" * 50)
    print(f"📝 Nombre: {client_data['nombre']}")
    print(f"📱 Teléfono: {client_data['telefono']}")
    print(f"📧 Email: {client_data['email']}")
    print(f"✅ Estado: En sandbox de Twilio")
    
    # Enviar solicitud POST a la API
    url = "http://localhost:5001/api/clients"
    response = requests.post(url, json=client_data, timeout=10)
    
    if response.status_code == 200:
        print("\n✅ Cliente agregado exitosamente!")
        result = response.json()
        print(f"📝 Respuesta: {result.get('message', 'N/A')}")
    else:
        print(f"\n❌ Error HTTP: {response.status_code}")
        print(f"📝 Respuesta: {response.text}")
    
    # Verificar clientes activos
    print("\n📋 VERIFICANDO CLIENTES ACTIVOS:")
    print("=" * 50)
    
    clients_response = requests.get("http://localhost:5001/api/clients", timeout=10)
    
    if clients_response.status_code == 200:
        response_data = clients_response.json()
        if response_data.get('success') and 'data' in response_data:
            clients = response_data['data']
            for client in clients:
                print(f"👤 {client['nombre']} - {client['telefono']}")
        else:
            print(f"❌ Error en respuesta: {response_data}")
    else:
        print(f"❌ Error obteniendo clientes: {clients_response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"❌ Error de conexión: {e}")
    print("💡 Asegúrate de que el bot esté ejecutándose en localhost:5001")
except Exception as e:
    print(f"❌ Error inesperado: {e}")
    import traceback
    traceback.print_exc() 