#!/usr/bin/env python3
"""
Script para corregir formato de número de teléfono
"""

import psycopg2

try:
    # Conectar a PostgreSQL
    conn = psycopg2.connect('postgresql://alesse_user:alesse_secure_pass_2024@localhost:5432/bot')
    cur = conn.cursor()
    
    # Buscar números sin formato correcto
    cur.execute("SELECT id, nombre, telefono FROM clientes WHERE telefono NOT LIKE '+%'")
    numeros_incorrectos = cur.fetchall()
    
    print("📱 CORRIGIENDO FORMATOS DE NÚMERO:")
    print("=" * 50)
    
    for cliente_id, nombre, telefono in numeros_incorrectos:
        # Corregir formato (agregar + si no lo tiene)
        telefono_corregido = f"+{telefono}" if not telefono.startswith('+') else telefono
        
        # Actualizar en base de datos
        cur.execute("UPDATE clientes SET telefono = %s WHERE id = %s", (telefono_corregido, cliente_id))
        
        print(f"✅ {nombre}: {telefono} → {telefono_corregido}")
    
    conn.commit()
    conn.close()
    
    print(f"\n🎉 {len(numeros_incorrectos)} números corregidos")
    
    # Verificar resultado
    conn = psycopg2.connect('postgresql://alesse_user:alesse_secure_pass_2024@localhost:5432/bot')
    cur = conn.cursor()
    cur.execute("SELECT nombre, telefono FROM clientes")
    todos_clientes = cur.fetchall()
    
    print("\n📋 CLIENTES ACTUALIZADOS:")
    print("=" * 50)
    for nombre, telefono in todos_clientes:
        print(f"👤 {nombre}: {telefono}")
    
    conn.close()

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 