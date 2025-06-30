#!/usr/bin/env python3
"""
🤖 Script Principal - Bot de Spam Masivo
Menú interactivo para gestionar el bot de spam
"""

import os
import sys
from spam_bot_service import spam_service

def mostrar_menu():
    """Mostrar menú principal"""
    print("\n" + "="*50)
    print("🤖 BOT DE SPAM MASIVO - ALESSE CONNECT")
    print("="*50)
    print("1. 📊 Ver estadísticas")
    print("2. 👥 Gestionar clientes")
    print("3. 📝 Gestionar templates")
    print("4. 🚀 Enviar spam masivo")
    print("5. 📈 Ver historial")
    print("6. 🔧 Test de conexión")
    print("0. ❌ Salir")
    print("="*50)

def ver_estadisticas():
    """Mostrar estadísticas del sistema"""
    print("\n📊 ESTADÍSTICAS DEL SISTEMA")
    print("-" * 30)
    
    clientes = spam_service.obtener_clientes_activos()
    templates = spam_service.obtener_templates_disponibles()
    historial = spam_service.obtener_historial_envios()
    stats = spam_service.obtener_estadisticas()
    
    print(f"👥 Total clientes activos: {len(clientes)}")
    print(f"📝 Templates disponibles: {len(templates)}")
    print(f"📨 Total envíos registrados: {len(historial)}")
    
    if stats.get('en_progreso'):
        print(f"🔄 Envío en progreso: {stats.get('template', 'N/A')}")
        print(f"📊 Progreso: {stats.get('enviados', 0) + stats.get('fallidos', 0)}/{stats.get('total', 0)}")
        print(f"✅ Exitosos: {stats.get('enviados', 0)}")
        print(f"❌ Fallidos: {stats.get('fallidos', 0)}")
    else:
        print("💤 No hay envíos en progreso")

def gestionar_clientes():
    """Gestionar clientes"""
    while True:
        print("\n👥 GESTIÓN DE CLIENTES")
        print("1. Ver lista de clientes")
        print("2. Agregar nuevo cliente")
        print("0. Volver al menú principal")
        
        opcion = input("\nSelecciona una opción: ").strip()
        
        if opcion == "1":
            clientes = spam_service.obtener_clientes_activos()
            print(f"\n📋 LISTA DE CLIENTES ({len(clientes)} activos)")
            print("-" * 70)
            for i, cliente in enumerate(clientes, 1):
                print(f"{i:2d}. {cliente['nombre']:20} | {cliente['telefono']:15} | Enviados: {cliente['total_enviados']}")
        
        elif opcion == "2":
            print("\n➕ AGREGAR NUEVO CLIENTE")
            nombre = input("Nombre completo: ").strip()
            telefono = input("Teléfono (+51999123456): ").strip()
            email_input = input("Email (opcional): ").strip()
            
            if nombre and telefono:
                if email_input:
                    success = spam_service.agregar_cliente(nombre, telefono, email_input)
                else:
                    success = spam_service.agregar_cliente(nombre, telefono)
                if success:
                    print("✅ Cliente agregado exitosamente")
                else:
                    print("❌ Error agregando cliente (posible duplicado)")
            else:
                print("❌ Nombre y teléfono son obligatorios")
        
        elif opcion == "0":
            break

def gestionar_templates():
    """Gestionar templates"""
    while True:
        print("\n📝 GESTIÓN DE TEMPLATES")
        print("1. Ver templates disponibles")
        print("2. Crear nuevo template")
        print("0. Volver al menú principal")
        
        opcion = input("\nSelecciona una opción: ").strip()
        
        if opcion == "1":
            templates = spam_service.obtener_templates_disponibles()
            print(f"\n📋 TEMPLATES DISPONIBLES ({len(templates)})")
            print("-" * 50)
            for i, template in enumerate(templates, 1):
                print(f"{i}. {template['nombre']}")
                print(f"   📄 {template['contenido'][:100]}...")
                print()
        
        elif opcion == "2":
            print("\n➕ CREAR NUEVO TEMPLATE")
            nombre = input("Nombre del template: ").strip()
            print("Contenido del mensaje (usa {nombre} para personalizar):")
            contenido = input("> ").strip()
            
            if nombre and contenido:
                success = spam_service.crear_template(nombre, contenido)
                if success:
                    print("✅ Template creado exitosamente")
                else:
                    print("❌ Error creando template")
            else:
                print("❌ Nombre y contenido son obligatorios")
        
        elif opcion == "0":
            break

def enviar_spam_masivo():
    """Iniciar envío masivo"""
    print("\n🚀 ENVÍO MASIVO")
    
    # Verificar si ya hay un envío en progreso
    stats = spam_service.obtener_estadisticas()
    if stats.get('en_progreso'):
        print("⚠️ Ya hay un envío en progreso")
        print(f"Template: {stats.get('template')}")
        print(f"Progreso: {stats.get('enviados', 0) + stats.get('fallidos', 0)}/{stats.get('total', 0)}")
        
        cancelar = input("\n¿Deseas cancelar el envío actual? (s/N): ").strip().lower()
        if cancelar == 's':
            if spam_service.cancelar_envio():
                print("✅ Envío cancelado")
            else:
                print("❌ No se pudo cancelar el envío")
        return
    
    # Mostrar templates disponibles
    templates = spam_service.obtener_templates_disponibles()
    if not templates:
        print("❌ No hay templates disponibles. Crea uno primero.")
        return
    
    print("\n📝 Templates disponibles:")
    for i, template in enumerate(templates, 1):
        print(f"{i}. {template['nombre']}")
    
    # Seleccionar template
    try:
        opcion = int(input(f"\nSelecciona template (1-{len(templates)}): ")) - 1
        if opcion < 0 or opcion >= len(templates):
            print("❌ Opción inválida")
            return
        
        template_seleccionado = templates[opcion]['nombre']
    except ValueError:
        print("❌ Por favor ingresa un número válido")
        return
    
    # Configurar delays
    try:
        delay_min = int(input("Delay mínimo entre envíos (segundos, default 5): ") or "5")
        delay_max = int(input("Delay máximo entre envíos (segundos, default 15): ") or "15")
    except ValueError:
        delay_min, delay_max = 5, 15
    
    # Mostrar información del envío
    clientes = spam_service.obtener_clientes_activos()
    print(f"\n📊 RESUMEN DEL ENVÍO:")
    print(f"📝 Template: {template_seleccionado}")
    print(f"👥 Clientes objetivo: {len(clientes)}")
    print(f"⏱️ Delay entre envíos: {delay_min}-{delay_max} segundos")
    print(f"🕐 Tiempo estimado: {len(clientes) * ((delay_min + delay_max) / 2) / 60:.1f} minutos")
    
    # Confirmar envío
    confirmar = input("\n¿Confirmas el envío masivo? (s/N): ").strip().lower()
    if confirmar != 's':
        print("❌ Envío cancelado")
        return
    
    # Iniciar envío
    result = spam_service.enviar_spam_masivo(template_seleccionado, delay_min, delay_max)
    
    if result['success']:
        print(f"✅ {result['message']}")
        print("\n🔄 El envío se está ejecutando en segundo plano.")
        print("💡 Puedes ver el progreso en 'Ver estadísticas'")
    else:
        print(f"❌ Error: {result['message']}")

def ver_historial():
    """Ver historial de envíos"""
    print("\n📈 HISTORIAL DE ENVÍOS")
    
    historial = spam_service.obtener_historial_envios(limite=20)
    
    if not historial:
        print("📭 No hay envíos registrados")
        return
    
    print(f"\n📋 Últimos {len(historial)} envíos:")
    print("-" * 80)
    
    for envio in historial:
        estado_icon = "✅" if envio['estado'] == 'enviado' else "❌"
        print(f"{estado_icon} {envio['cliente']:20} | {envio['template']:20} | {envio['fecha']}")

def test_conexion():
    """Probar conexión con Twilio"""
    print("\n🔧 TEST DE CONEXIÓN")
    print("Probando conexión con Twilio...")
    
    result = spam_service.test_conexion()
    
    if result['success']:
        print("✅ CONEXIÓN EXITOSA")
        print(f"📱 WhatsApp Number: {result['whatsapp_number']}")
        print(f"🏢 Account: {result['account_name']}")
        print(f"🆔 SID: {result['account_sid']}")
    else:
        print("❌ ERROR DE CONEXIÓN")
        print(f"📋 Mensaje: {result['message']}")
        print("\n💡 Verifica las credenciales en el archivo .environment")

def main():
    """Función principal"""
    print("🤖 Inicializando Bot de Spam Masivo...")
    
    # Verificar que el servicio está inicializado
    try:
        spam_service.test_conexion()
        print("✅ Servicio inicializado correctamente")
    except Exception as e:
        print(f"❌ Error inicializando servicio: {e}")
        print("💡 Verifica tu configuración en .environment")
        return
    
    while True:
        try:
            mostrar_menu()
            opcion = input("\nSelecciona una opción: ").strip()
            
            if opcion == "1":
                ver_estadisticas()
            elif opcion == "2":
                gestionar_clientes()
            elif opcion == "3":
                gestionar_templates()
            elif opcion == "4":
                enviar_spam_masivo()
            elif opcion == "5":
                ver_historial()
            elif opcion == "6":
                test_conexion()
            elif opcion == "0":
                print("\n👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción inválida")
            
            input("\nPresiona Enter para continuar...")
            
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    main() 