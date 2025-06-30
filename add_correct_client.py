#!/usr/bin/env python3
"""
Script para agregar cliente correcto que está en el sandbox
"""

import psycopg2

try:
    # Conectar a PostgreSQL
    conn = psycopg2.connect('postgresql://alesse_user:alesse_secure_pass_2024@localhost:5432/bot')
    cur = conn.cursor()
    
    # Datos del cliente correcto
    nombre = "Jair Kiwipay"
    telefono = "+51960454985"  # Formato correcto con +
    email = "jair.kiwipay@example.com"
    
    print("👤 AGREGANDO CLIENTE CORRECTO:")
    print("=" * 50)
    print(f"📝 Nombre: {nombre}")
    print(f"📱 Teléfono: {telefono}")
    print(f"📧 Email: {email}")
    print(f"✅ Estado: En sandbox de Twilio")
    
    # Eliminar cliente anterior (Jair con número incorrecto)
    cur.execute("DELETE FROM clientes WHERE nombre = 'Jair' AND telefono != %s", (telefono,))
    deleted_count = cur.rowcount
    if deleted_count > 0:
        print(f"🗑️ Cliente anterior eliminado: {deleted_count} registro(s)")
    
    # Agregar cliente correcto
    cur.execute("""
        INSERT INTO clientes (nombre, telefono, email, activo) 
        VALUES (%s, %s, %s, true)
        ON CONFLICT (telefono) DO UPDATE SET
        nombre = EXCLUDED.nombre,
        email = EXCLUDED.email,
        activo = true
    """, (nombre, telefono, email))
    
    conn.commit()
    
    print("✅ Cliente agregado/actualizado exitosamente")
    
    # Verificar resultado
    cur.execute("SELECT id, nombre, telefono, email, activo FROM clientes WHERE activo = true")
    clientes = cur.fetchall()
    
    print("\n📋 CLIENTES ACTIVOS:")
    print("=" * 50)
    for cliente_id, nombre_db, telefono_db, email_db, activo in clientes:
        print(f"🆔 ID: {cliente_id}")
        print(f"👤 Nombre: {nombre_db}")
        print(f"📱 Teléfono: {telefono_db}")
        print(f"📧 Email: {email_db or 'N/A'}")
        print(f"✅ Activo: {'Sí' if activo else 'No'}")
        print("-" * 30)
    
    conn.close()
    
    print("\n🎉 ¡LISTO! Cliente configurado correctamente")
    print("📱 Ahora puedes enviar mensajes a +51960454985")
    print("🔥 Este número SÍ está en el sandbox de Twilio")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 