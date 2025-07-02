#!/usr/bin/env python3
"""
Script para verificar conexión a PostgreSQL
Configuración: alesse_connect database
"""
import os
import sys
import psycopg2
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('.environment')

def test_postgresql_connection():
    """
    Verifica la conexión a PostgreSQL usando la configuración del .environment
    """
    print("🔍 VERIFICACIÓN DE CONEXIÓN POSTGRESQL")
    print("=" * 50)
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL no encontrada en .environment")
        return False
    
    print(f"🔗 Conectando a: {database_url}")
    print("")
    
    try:
        # Intentar conexión
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Verificar versión de PostgreSQL
        cursor.execute("SELECT version();")
        version_result = cursor.fetchone()
        version = version_result[0] if version_result else "Desconocida"
        print(f"✅ Conexión exitosa!")
        print(f"📊 PostgreSQL Version: {version}")
        print("")
        
        # Verificar base de datos actual
        cursor.execute("SELECT current_database();")
        db_result = cursor.fetchone()
        current_db = db_result[0] if db_result else "Desconocida"
        print(f"🗄️ Base de datos actual: {current_db}")
        
        # Verificar usuario actual
        cursor.execute("SELECT current_user;")
        user_result = cursor.fetchone()
        current_user = user_result[0] if user_result else "Desconocido"
        print(f"👤 Usuario actual: {current_user}")
        print("")
        
        # Listar tablas existentes
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        if tables:
            print(f"📋 Tablas existentes ({len(tables)}):")
            for table in tables:
                print(f"   • {table[0]}")
        else:
            print("📋 No hay tablas en la base de datos (esto es normal para una DB nueva)")
        
        print("")
        
        # Verificar permisos básicos
        try:
            cursor.execute("CREATE TEMP TABLE test_permissions (id INTEGER);")
            cursor.execute("DROP TABLE test_permissions;")
            print("✅ Permisos de CREATE/DROP: OK")
        except Exception as e:
            print(f"⚠️ Permisos limitados: {str(e)}")
        
        cursor.close()
        conn.close()
        
        print("")
        print("🎉 VERIFICACIÓN COMPLETADA EXITOSAMENTE")
        print("🚀 La base de datos está lista para el microservicio")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Error de conexión: {str(e)}")
        print("")
        print("💡 POSIBLES SOLUCIONES:")
        print("   1. Verificar que PostgreSQL esté corriendo:")
        print("      • Windows: services.msc → PostgreSQL")
        print("      • Linux: sudo systemctl status postgresql")
        print("      • Mac: brew services list | grep postgresql")
        print("")
        print("   2. Verificar credenciales en .environment:")
        print("      • Usuario: postgres")
        print("      • Password: root")
        print("      • Base de datos: alesse_connect")
        print("")
        print("   3. Crear la base de datos si no existe:")
        print("      • Conectar a pgAdmin")
        print("      • CREATE DATABASE alesse_connect;")
        return False
        
    except Exception as e:
        print(f"💥 Error inesperado: {str(e)}")
        return False

def create_database_if_not_exists():
    """
    Intenta crear la base de datos alesse_connect si no existe
    """
    print("🔧 CREANDO BASE DE DATOS SI NO EXISTE")
    print("=" * 50)
    
    try:
        # Conectar a PostgreSQL sin especificar base de datos (usa 'postgres' por defecto)
        base_url = os.getenv('DATABASE_URL', '').replace('/alesse_connect', '/postgres')
        
        conn = psycopg2.connect(base_url)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Verificar si la base de datos existe
        cursor.execute("""
            SELECT 1 FROM pg_database 
            WHERE datname = 'alesse_connect';
        """)
        
        if cursor.fetchone():
            print("✅ Base de datos 'alesse_connect' ya existe")
        else:
            print("🔧 Creando base de datos 'alesse_connect'...")
            cursor.execute("CREATE DATABASE alesse_connect;")
            print("✅ Base de datos 'alesse_connect' creada exitosamente")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creando base de datos: {str(e)}")
        print("💡 Crea la base de datos manualmente en pgAdmin:")
        print("   CREATE DATABASE alesse_connect;")
        return False

def quick_connection_test():
    """
    Test rápido y silencioso de conexión para usar en scripts
    """
    try:
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            return False
            
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        cursor.close()
        conn.close()
        return True
    except:
        return False

if __name__ == "__main__":
    # Modo silencioso para scripts
    if len(sys.argv) > 1 and sys.argv[1] == '--quiet':
        if quick_connection_test():
            sys.exit(0)
        else:
            sys.exit(1)
    
    # Modo completo
    print("🐘 VERIFICADOR DE POSTGRESQL - ALESSE CONNECT")
    print("Configuración para microservicio WhatsApp")
    print("")
    
    # Paso 1: Intentar crear la base de datos si no existe
    if create_database_if_not_exists():
        print("")
        
    # Paso 2: Verificar conexión completa
    if test_postgresql_connection():
        print("")
        print("🎯 CONFIGURACIÓN LISTA PARA:")
        print("   • Templates de WhatsApp")
        print("   • Logs de mensajes")
        print("   • Configuración de microservicio")
        print("   • Comunicación con API Gateway")
        sys.exit(0)
    else:
        print("")
        print("🔧 PASOS MANUALES NECESARIOS:")
        print("   1. Abrir pgAdmin")
        print("   2. Conectar al servidor PostgreSQL")
        print("   3. Crear base de datos: alesse_connect")
        print("   4. Ejecutar este script de nuevo")
        sys.exit(1) 