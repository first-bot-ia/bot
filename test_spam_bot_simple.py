#!/usr/bin/env python3
"""
🧪 Test Simple del Bot de Spam
Prueba básica de funcionalidad
"""

from spam_bot_service import spam_service

def test_basico():
    """Prueba básica del bot de spam"""
    print("🧪 INICIANDO PRUEBAS DEL BOT DE SPAM")
    print("=" * 50)
    
    # 1. Test de conexión
    print("\n1. 🔧 Probando conexión Twilio...")
    result = spam_service.test_conexion()
    if result['success']:
        print("✅ Conexión exitosa")
        print(f"📱 WhatsApp: {result['whatsapp_number']}")
    else:
        print(f"❌ Error: {result['message']}")
        return
    
    # 2. Verificar clientes
    print("\n2. 👥 Verificando clientes...")
    clientes = spam_service.obtener_clientes_activos()
    print(f"✅ {len(clientes)} clientes encontrados")
    
    # 3. Verificar templates
    print("\n3. 📝 Verificando templates...")
    templates = spam_service.obtener_templates_disponibles()
    print(f"✅ {len(templates)} templates encontrados")
    
    if templates:
        print("\nTemplates disponibles:")
        for i, template in enumerate(templates, 1):
            print(f"  {i}. {template['nombre']}")
    
    # 4. Mostrar estadísticas
    print("\n4. 📊 Estadísticas actuales...")
    stats = spam_service.obtener_estadisticas()
    if stats.get('en_progreso'):
        print(f"🔄 Envío en progreso: {stats.get('template')}")
    else:
        print("💤 No hay envíos en progreso")
    
    # 5. Mostrar historial reciente
    print("\n5. 📈 Historial reciente...")
    historial = spam_service.obtener_historial_envios(limite=5)
    if historial:
        print(f"✅ {len(historial)} envíos recientes encontrados")
        for envio in historial[:3]:
            estado_icon = "✅" if envio['estado'] == 'enviado' else "❌"
            print(f"  {estado_icon} {envio['cliente']} - {envio['template']}")
    else:
        print("📭 No hay historial de envíos")
    
    print("\n🎉 PRUEBAS COMPLETADAS")
    print("🚀 El bot está listo para usar!")

def agregar_cliente_prueba():
    """Agregar un cliente de prueba"""
    print("\n➕ Agregando cliente de prueba...")
    
    success = spam_service.agregar_cliente(
        nombre="Cliente Prueba",
        telefono="+51999000999", 
        email="prueba@test.com"
    )
    
    if success:
        print("✅ Cliente de prueba agregado")
    else:
        print("⚠️ Cliente ya existe o error agregando")

def crear_template_prueba():
    """Crear un template de prueba"""
    print("\n📝 Creando template de prueba...")
    
    success = spam_service.crear_template(
        nombre="Test Template",
        contenido="🧪 Hola {nombre}, este es un mensaje de prueba del bot de spam de Alesse Connect!"
    )
    
    if success:
        print("✅ Template de prueba creado")
    else:
        print("⚠️ Template ya existe o error creando")

def main():
    """Función principal de pruebas"""
    print("🤖 BOT DE SPAM - PRUEBAS BÁSICAS")
    print("=" * 40)
    
    try:
        test_basico()
        
        print("\n" + "=" * 40)
        respuesta = input("¿Quieres agregar datos de prueba? (s/N): ").strip().lower()
        
        if respuesta == 's':
            agregar_cliente_prueba()
            crear_template_prueba()
            print("\n🔄 Ejecutando pruebas nuevamente...")
            test_basico()
        
        print("\n💡 PARA USAR EL BOT:")
        print("  - Ejecuta: python run_spam_bot.py")
        print("  - O crea una interfaz web personalizada")
        
    except Exception as e:
        print(f"\n❌ Error en pruebas: {e}")
        print("💡 Verifica tu configuración en .environment")

if __name__ == "__main__":
    main() 