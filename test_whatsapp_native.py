#!/usr/bin/env python3
"""
🧪 Test del servicio nativo WhatsApp Business API
Ejecuta cuando hayas configurado los IDs
"""

from whatsapp_native_service import whatsapp_native_service

def test_completo():
    print("🧪 TEST COMPLETO - WHATSAPP BUSINESS API NATIVA")
    print("=" * 60)
    
    # 1. Test de conexión
    print("\n1. 🔧 Probando conexión...")
    result = whatsapp_native_service.test_conexion()
    if result['success']:
        print("✅ Conexión exitosa")
        print(f"📱 Cuenta: {result['account_info'].get('name', 'Sin nombre')}")
    else:
        print(f"❌ Error: {result['message']}")
        return
    
    # 2. Test de información del número
    print("\n2. 📞 Verificando número de teléfono...")
    phone_info = whatsapp_native_service.get_phone_number_info()
    if 'error' in phone_info:
        print(f"❌ Error: {phone_info['error']}")
        if "NECESITAS_OBTENER_ESTO" in phone_info['error']:
            print("🔧 Ejecuta: python configurar_ids.py")
        return
    else:
        print("✅ Número verificado")
        if 'display_phone_number' in phone_info:
            print(f"📱 Número: {phone_info['display_phone_number']}")
    
    # 3. Verificar clientes
    print("\n3. 👥 Verificando clientes...")
    clientes = whatsapp_native_service.obtener_clientes_activos()
    print(f"✅ {len(clientes)} clientes encontrados")
    
    for cliente in clientes:
        print(f"  • {cliente['nombre']} - {cliente['telefono']}")
    
    # 4. Verificar templates
    print("\n4. 📝 Verificando templates...")
    templates = whatsapp_native_service.obtener_templates_disponibles()
    print(f"✅ {len(templates)} templates disponibles")
    
    for template in templates:
        estado_icon = "✅" if template['estado'] == 'approved' else "⏳"
        print(f"  {estado_icon} {template['nombre']} ({template['estado']})")
    
    # 5. Test de envío (opcional)
    print("\n5. 🚀 ¿Quieres hacer un test de envío? (s/N): ", end="")
    test_envio = input().strip().lower()
    
    if test_envio == 's' and clientes and templates:
        cliente_test = clientes[0]  # Primer cliente
        template_test = templates[0]  # Primer template
        
        print(f"\n📤 Enviando test a {cliente_test['nombre']}...")
        print(f"📝 Template: {template_test['nombre']}")
        
        # Enviar mensaje de prueba
        resultado = whatsapp_native_service.send_template_message(
            to_number=cliente_test['telefono'],
            template_name=template_test['template_name'],
            parameters=[cliente_test['nombre']],
            language_code=template_test['language_code']
        )
        
        if resultado.get('success'):
            print("✅ ¡Mensaje enviado exitosamente!")
            print(f"🆔 Message ID: {resultado.get('message_id')}")
        else:
            print("❌ Error enviando mensaje:")
            print(f"Error: {resultado.get('error')}")
    
    print("\n🎉 TEST COMPLETADO")
    print("\n💡 PARA USAR EN PRODUCCIÓN:")
    print("• Crea templates personalizados en tu panel Meta")
    print("• Espera aprobación de Meta (24-48 horas)")
    print("• Configura webhook para mensajes entrantes")
    print("• ¡Listo para reemplazar Twilio completamente!")

if __name__ == "__main__":
    test_completo() 