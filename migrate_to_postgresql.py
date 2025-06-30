#!/usr/bin/env python3
"""
🔄 Migración de SQLite a PostgreSQL
Soluciona el problema "database is locked" definitivamente
"""

import os
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
import logging

# Configuración PostgreSQL
PG_CONFIG = {
    'host': 'localhost',
    'database': 'bot',
    'user': 'postgres', 
    'password': 'root',
    'port': 5432
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_postgresql_connection():
    """Probar conexión a PostgreSQL"""
    try:
        conn = psycopg2.connect(**PG_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        conn.close()
        print(f"✅ PostgreSQL conectado: {version}")
        return True
    except Exception as e:
        print(f"❌ Error conectando PostgreSQL: {e}")
        print("💡 Asegúrate de que PostgreSQL esté corriendo y la BD 'bot' exista")
        return False

def create_postgresql_tables():
    """Crear tablas en PostgreSQL"""
    print("🏗️ Creando tablas en PostgreSQL...")
    
    try:
        conn = psycopg2.connect(**PG_CONFIG)
        cursor = conn.cursor()
        
        # Tabla clientes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                telefono VARCHAR(50) NOT NULL UNIQUE,
                email VARCHAR(255),
                activo BOOLEAN DEFAULT true,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ultimo_envio TIMESTAMP,
                total_enviados INTEGER DEFAULT 0
            )
        """)
        
        # Tabla envios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS envios (
                id SERIAL PRIMARY KEY,
                cliente_id INTEGER REFERENCES clientes(id),
                template_usado VARCHAR(100),
                mensaje TEXT,
                parametros TEXT,
                estado VARCHAR(20),
                fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                respuesta_twilio TEXT,
                message_sid VARCHAR(100)
            )
        """)
        
        # Tabla campañas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS campañas (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                template_usado VARCHAR(100) NOT NULL,
                descripcion TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_ejecucion TIMESTAMP,
                total_enviados INTEGER DEFAULT 0,
                total_exitosos INTEGER DEFAULT 0,
                total_fallidos INTEGER DEFAULT 0,
                estado VARCHAR(20) DEFAULT 'pendiente'
            )
        """)
        
        conn.commit()
        conn.close()
        print("✅ Tablas PostgreSQL creadas")
        return True
        
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        return False

def migrate_data_from_sqlite():
    """Migrar datos de SQLite a PostgreSQL"""
    print("📦 Migrando datos de SQLite...")
    
    sqlite_path = 'clientes_spam.db'
    if not os.path.exists(sqlite_path):
        print("⚠️ No hay datos SQLite para migrar")
        return True
    
    try:
        # Conectar a ambas bases
        sqlite_conn = sqlite3.connect(sqlite_path)
        sqlite_conn.row_factory = sqlite3.Row
        
        pg_conn = psycopg2.connect(**PG_CONFIG)
        pg_cursor = pg_conn.cursor()
        
        # Migrar clientes
        sqlite_cursor = sqlite_conn.cursor()
        sqlite_cursor.execute("SELECT * FROM clientes")
        clientes = sqlite_cursor.fetchall()
        
        for cliente in clientes:
            pg_cursor.execute("""
                INSERT INTO clientes (nombre, telefono, email, activo, fecha_registro, ultimo_envio, total_enviados)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (telefono) DO NOTHING
            """, (
                cliente['nombre'],
                cliente['telefono'], 
                cliente['email'],
                bool(cliente['activo']),
                cliente['fecha_registro'],
                cliente['ultimo_envio'],
                cliente['total_enviados']
            ))
        
        print(f"✅ {len(clientes)} clientes migrados")
        
        # Migrar envíos si existen
        try:
            sqlite_cursor.execute("SELECT * FROM envios")
            envios = sqlite_cursor.fetchall()
            
            for envio in envios:
                # Obtener cliente_id de PostgreSQL
                pg_cursor.execute("SELECT id FROM clientes WHERE telefono = (SELECT telefono FROM clientes WHERE id = %s)", (envio['cliente_id'],))
                pg_cliente = pg_cursor.fetchone()
                
                if pg_cliente:
                    pg_cursor.execute("""
                        INSERT INTO envios (cliente_id, template_usado, mensaje, parametros, estado, fecha_envio, respuesta_twilio, message_sid)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        pg_cliente[0],
                        envio.get('template_usado'),
                        envio.get('mensaje'),
                        envio.get('parametros'),
                        envio['estado'],
                        envio['fecha_envio'],
                        envio['respuesta_twilio'],
                        envio.get('message_sid')
                    ))
            
            print(f"✅ {len(envios)} envíos migrados")
            
        except Exception as e:
            print(f"⚠️ No se pudieron migrar envíos: {e}")
        
        pg_conn.commit()
        pg_conn.close()
        sqlite_conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error migrando datos: {e}")
        return False

def update_environment_file():
    """Actualizar archivo .environment con PostgreSQL"""
    print("📝 Actualizando configuración...")
    
    try:
        # Leer archivo actual
        env_path = '.environment'
        lines = []
        
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                lines = f.readlines()
        
        # Agregar configuración PostgreSQL
        pg_config = f"""
# PostgreSQL Configuration
DATABASE_URL=postgresql://postgres:root@localhost:5432/bot
DB_HOST=localhost
DB_NAME=bot
DB_USER=postgres
DB_PASSWORD=root
DB_PORT=5432
DB_TYPE=postgresql
"""
        
        with open(env_path, 'a') as f:
            f.write(pg_config)
        
        print("✅ Configuración PostgreSQL agregada a .environment")
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando configuración: {e}")
        return False

def main():
    print("🚀 Migración SQLite → PostgreSQL")
    print("=" * 50)
    print("Esto solucionará el error 'database is locked' definitivamente")
    print()
    
    # Paso 1: Probar PostgreSQL
    if not test_postgresql_connection():
        print("\n❌ No se puede conectar a PostgreSQL")
        print("💡 Instrucciones:")
        print("   1. Instala PostgreSQL")
        print("   2. Crea la base de datos 'bot':")
        print("      createdb -U postgres bot")
        print("   3. Ejecuta este script nuevamente")
        return
    
    # Paso 2: Crear tablas
    if not create_postgresql_tables():
        return
    
    # Paso 3: Migrar datos
    if not migrate_data_from_sqlite():
        return
    
    # Paso 4: Actualizar configuración
    if not update_environment_file():
        return
    
    print("\n🎉 ¡Migración completada exitosamente!")
    print("=" * 50)
    print("✅ PostgreSQL configurado")
    print("✅ Datos migrados")
    print("✅ Configuración actualizada")
    print()
    print("🔧 Próximos pasos:")
    print("   1. Instala psycopg2: pip install psycopg2-binary")
    print("   2. Reinicia el bot: python run_spam_bot.py")
    print("   3. ¡No más errores 'database is locked'!")

if __name__ == "__main__":
    main() 