#!/usr/bin/env python3
"""
🔧 Test Ultra Simple - Solo verificar que el servidor responde
"""

import requests

try:
    # Test más básico posible
    response = requests.get("http://localhost:5000/health")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Servidor funcionando")
        data = response.json()
        print(f"Status: {data.get('status', 'unknown')}")
    else:
        print("❌ Servidor con problemas")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}") 