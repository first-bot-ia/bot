#!/usr/bin/env python3
"""
🧪 Script de Testing - Integración Bot Python ↔ Backend Node.js
Verifica que todos los endpoints y clientes funcionen correctamente
"""
import requests
import json
import time
from datetime import datetime
from typing import Dict, Any
from infrastructure.external_services.backend_client import AlesseBackendClient


class IntegrationTester:
    """
    Tester completo para verificar integración bidireccional
    """
    
    def __init__(self):
        self.bot_url = "http://localhost:5000"
        self.backend_url = "http://localhost:9000"
        self.backend_client = AlesseBackendClient(self.backend_url)
        self.test_phone = "573001234567"
        self.test_message = "Mensaje de prueba desde tester"
    
    def run_all_tests(self):
        """Ejecuta todos los tests de integración"""
        print("🧪 TESTING DE INTEGRACIÓN BOT ↔ BACKEND")
        print("=" * 50)
        
        # Test 1: Verificar conectividad
        self.test_connectivity()
        
        # Test 2: Verificar endpoint Bot → Backend
        self.test_bot_to_backend()
        
        # Test 3: Verificar endpoint Backend → Bot
        self.test_backend_to_bot()
        
        # Test 4: Verificar webhook bidireccional
        self.test_webhook_forwarding()
        
        # Test 5: Verificar health checks
        self.test_health_checks()
        
        print("\n🎉 TESTING COMPLETO")
        print("=" * 50)
    
    def test_connectivity(self):
        """Test 1: Verificar que ambos servicios estén funcionando"""
        print("\n1️⃣ VERIFICANDO CONECTIVIDAD...")
        
        # Verificar Bot Python
        try:
            bot_response = requests.get(f"{self.bot_url}/health", timeout=5)
            if bot_response.status_code == 200:
                print("   ✅ Bot Python funcionando (Puerto 5000)")
            else:
                print(f"   ❌ Bot Python error: {bot_response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ Bot Python no accesible: {str(e)}")
            return False
        
        # Verificar Backend Node.js
        try:
            backend_ok, backend_data = self.backend_client.health_check()
            if backend_ok:
                print("   ✅ Backend Node.js funcionando (Puerto 9000)")
            else:
                print(f"   ❌ Backend Node.js error: {backend_data}")
                return False
        except Exception as e:
            print(f"   ❌ Backend Node.js no accesible: {str(e)}")
            return False
        
        return True
    
    def test_bot_to_backend(self):
        """Test 2: Bot Python → Backend Node.js"""
        print("\n2️⃣ TESTING BOT → BACKEND...")
        
        try:
            response = self.backend_client.send_message_to_backend(
                phone=self.test_phone,
                message=f"Test message at {datetime.now().strftime('%H:%M:%S')}",
                message_id="test_msg_123",
                contact_name="Usuario de Prueba"
            )
            
            if response["success"]:
                print("   ✅ Mensaje enviado al Backend exitosamente")
                print(f"   📨 Message ID: {response['data']['messageId']}")
                print(f"   💬 Conversation ID: {response['data']['conversationId']}")
                print(f"   👤 Contact ID: {response['data']['contactId']}")
                return True
            else:
                print(f"   ❌ Error enviando al Backend: {response['error']}")
                return False
        except Exception as e:
            print(f"   ❌ Excepción en Bot → Backend: {str(e)}")
            return False
    
    def test_backend_to_bot(self):
        """Test 3: Backend Node.js → Bot Python"""
        print("\n3️⃣ TESTING BACKEND → BOT...")
        
        test_payload = {
            "phone": self.test_phone,
            "message": f"Mensaje desde Backend - {datetime.now().strftime('%H:%M:%S')}",
            "conversationId": 123,
            "advisorId": "5",
            "timestamp": datetime.now().isoformat(),
            "source": "backend-direct"
        }
        
        try:
            response = requests.post(
                f"{self.bot_url}/send-message-to-user",
                json=test_payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print("   ✅ Mensaje enviado desde Backend al Bot")
                print(f"   📱 WhatsApp Message ID: {data['data']['whatsappMessageId']}")
                print(f"   📞 Phone: {data['data']['phone']}")
                return True
            else:
                print(f"   ❌ Error Backend → Bot: {response.status_code}")
                print(f"   Respuesta: {response.text}")
                return False
        except Exception as e:
            print(f"   ❌ Excepción en Backend → Bot: {str(e)}")
            return False
    
    def test_webhook_forwarding(self):
        """Test 4: Webhook bidireccional (simular WhatsApp)"""
        print("\n4️⃣ TESTING WEBHOOK BIDIRECCIONAL...")
        
        # Simular webhook de Twilio
        twilio_webhook = {
            "From": f"whatsapp:{self.test_phone}",
            "Body": f"Mensaje desde WhatsApp - {datetime.now().strftime('%H:%M:%S')}",
            "MessageSid": "SM1234567890abcdef",
            "AccountSid": "ACa04b8f9a85c8c2668b35343b45ed080e",
            "NumMedia": "0"
        }
        
        try:
            response = requests.post(
                f"{self.bot_url}/whatsapp/webhook",
                json=twilio_webhook,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print("   ✅ Webhook procesado correctamente")
                print("   📡 Forward al API Gateway:", data.get('api_gateway_response', 'OK'))
                print("   🔄 Forward al Backend:", 
                      'OK' if data.get('backend_response', {}).get('success') else 'Error')
                return True
            else:
                print(f"   ❌ Error en webhook: {response.status_code}")
                print(f"   Respuesta: {response.text}")
                return False
        except Exception as e:
            print(f"   ❌ Excepción en webhook: {str(e)}")
            return False
    
    def test_health_checks(self):
        """Test 5: Health checks detallados"""
        print("\n5️⃣ TESTING HEALTH CHECKS...")
        
        try:
            # Health check del Bot
            bot_health = requests.get(f"{self.bot_url}/health", timeout=5)
            if bot_health.status_code == 200:
                health_data = bot_health.json()
                print(f"   ✅ Bot Health: {health_data['status']}")
                print(f"   🔌 Twilio: {health_data['twilio']['status']}")
            
            # Health check interno
            internal_health = requests.get(f"{self.bot_url}/internal/health/detailed", timeout=5)
            if internal_health.status_code in [200, 503]:  # 503 es aceptable para degraded
                health_data = internal_health.json()
                print(f"   ✅ Internal Health: {health_data['status']}")
                
            return True
        except Exception as e:
            print(f"   ❌ Error en health checks: {str(e)}")
            return False
    
    def test_database_queries(self):
        """Test 6: Consultas a base de datos (opcional)"""
        print("\n6️⃣ TESTING CONSULTAS BASE DE DATOS...")
        
        try:
            # Obtener conversaciones pendientes
            conversations = self.backend_client.get_pending_conversations()
            if conversations["success"]:
                print(f"   ✅ Conversaciones pendientes: {len(conversations['data'])}")
            
            # Obtener asesores disponibles
            advisors = self.backend_client.get_available_advisors()
            if advisors["success"]:
                print(f"   ✅ Asesores disponibles: {len(advisors['data'])}")
            
            return True
        except Exception as e:
            print(f"   ❌ Error en consultas DB: {str(e)}")
            return False


def main():
    """Función principal de testing"""
    tester = IntegrationTester()
    
    print("🔄 Iniciando tests de integración...")
    print("⏰ Asegúrate de que estén corriendo:")
    print("   • Bot Python (puerto 5000)")
    print("   • Backend Node.js (puerto 9000)")
    print("   • PostgreSQL (puerto 5432)")
    print()
    
    input("Presiona ENTER para continuar...")
    
    try:
        tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⚠️ Testing interrumpido por el usuario")
    except Exception as e:
        print(f"\n\n💥 Error inesperado: {str(e)}")


if __name__ == "__main__":
    main() 