#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar la conexión a PostgreSQL
Evita problemas de encoding en PowerShell
"""

import sys
import os

# Configurar encoding para Windows
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

try:
    import psycopg2
    print("✅ psycopg2 importado exitosamente")
    
    # Configuración de conexión
    DATABASE_URL = "postgresql://alesse_user:alesse_secure_pass_2024@localhost:5432/bot"
    
    print("🔗 Conectando a PostgreSQL...")
    conn = psycopg2.connect(DATABASE_URL)
    print("✅ Conexión exitosa a la base de datos 'bot'")
    
    # Verificar tablas
    cur = conn.cursor()
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    
    tables = cur.fetchall()
    print("\n📋 Tablas encontradas:")
    for table in tables:
        print(f"  ✅ {table[0]}")
    
    # Verificar datos
    if tables:
        try:
            cur.execute("SELECT COUNT(*) FROM clientes")
            result = cur.fetchone()
            clientes_count = result[0] if result else 0
            
            cur.execute("SELECT COUNT(*) FROM envios")
            result = cur.fetchone()
            envios_count = result[0] if result else 0
            
            cur.execute("SELECT COUNT(*) FROM campañas")
            result = cur.fetchone()
            campañas_count = result[0] if result else 0
            
            print(f"\n📊 Datos en la base de datos:")
            print(f"  👥 Clientes: {clientes_count}")
            print(f"  📧 Envíos: {envios_count}")
            print(f"  📢 Campañas: {campañas_count}")
            
        except Exception as e:
            print(f"⚠️  Error al contar datos: {e}")
    
    cur.close()
    conn.close()
    
    print("\n🎉 ¡Sistema PostgreSQL funcionando correctamente!")
    print("✅ Todo listo para ejecutar el bot")
    
except ImportError:
    print("❌ Error: psycopg2 no está instalado")
    print("💡 Ejecuta: pip install psycopg2-binary")
    
except psycopg2.OperationalError as e:
    print(f"❌ Error de conexión a PostgreSQL: {e}")
    print("💡 Verifica que PostgreSQL esté ejecutándose")
    
except Exception as e:
    print(f"❌ Error inesperado: {e}")
    import traceback
    traceback.print_exc() 