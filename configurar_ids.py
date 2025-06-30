#!/usr/bin/env python3
"""
🔧 Script para configurar Phone Number ID y Business Account ID
"""

def configurar_ids():
    print("🔧 CONFIGURAR IDS DE WHATSAPP BUSINESS API")
    print("=" * 50)
    
    print("\n📋 Necesitas estos datos de tu panel Meta:")
    print("1. Phone Number ID (número largo)")
    print("2. Business Account ID (número largo)")
    
    print("\n🔍 Dónde encontrarlos:")
    print("• Panel Meta Developer > Tu App > WhatsApp > Getting Started")
    print("• O en Configuration/Settings")
    
    phone_id = input("\n📞 Phone Number ID: ").strip()
    business_id = input("🏢 Business Account ID: ").strip()
    
    if phone_id and business_id:
        print(f"\n✅ IDs proporcionados:")
        print(f"📞 Phone: {phone_id}")
        print(f"🏢 Business: {business_id}")
        
        # Actualizar archivo de configuración
        with open('whatsapp_native_service.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar los valores
        content = content.replace(
            'self.phone_number_id = "NECESITAS_OBTENER_ESTO"',
            f'self.phone_number_id = "{phone_id}"'
        )
        content = content.replace(
            'self.business_account_id = "NECESITAS_OBTENER_ESTO"',
            f'self.business_account_id = "{business_id}"'
        )
        
        with open('whatsapp_native_service.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("\n✅ Configuración actualizada en whatsapp_native_service.py")
        print("\n🚀 ¡Ahora puedes enviar mensajes sin Twilio!")
        
    else:
        print("\n❌ IDs no proporcionados")

if __name__ == "__main__":
    configurar_ids() 