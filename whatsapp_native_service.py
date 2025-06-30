#!/usr/bin/env python3
"""
🚀 Servicio Bot de Spam con API Nativa de WhatsApp Business
Reemplaza completamente a Twilio - Sin limitaciones de sandbox
"""

import os
import sqlite3
import time
import logging
import random
import requests
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import threading
import queue

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WhatsAppNativeService:
    """
    🚀 Servicio de Bot de Spam con API Nativa de WhatsApp
    Sin limitaciones de sandbox - Mensajes directos a cualquier número
    """
    
    def __init__(self):
        # 🔑 CONFIGURACIÓN DE WHATSAPP BUSINESS API
        self.access_token = "EAAauiqhK8cABO0Qvk2ZAoEfZA2MAiC1Q8krYmckco3yblUNkHMZAZAKKvMnMTc94y0h9nJUj400FmnDZCjntKWKsZAsaUMZAZB9d0rpJWspfajJxUQRIKQSrj6XX15UMr12zZARmCexC2bQU5yZBAuMwSBPpDPywCKTinwrz4WzfZBZATlYkXrNiPrpvLZBFiqHPE9t8zWDfXj3eECj5AwvAF4tMyglJEN1lG2j4mYUZCE17hoYwZDZD"
        
        # ✅ CONFIGURADO CON TUS DATOS REALES:
        self.phone_number_id = "616282071577878"  # Tu Phone Number ID
        self.business_account_id = "657056067365992"  # Tu Business Account ID
        
        # API Configuration
        self.api_version = "v22.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
        
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        # Base de datos
        self.db_path = 'clientes_spam.db'
        self._initialize_database()
        
        # Templates predefinidos para WhatsApp Business
        self.templates = self._load_templates()
        
        # Control de envío
        self.sending_queue = queue.Queue()
        self.is_sending = False
        self.stats = {
            'enviados': 0,
            'fallidos': 0,
            'total': 0,
            'inicio': None,
            'fin': None
        }
        
        logger.info("🚀 WhatsAppNativeService inicializado")
    
    def _initialize_database(self):
        """Inicializa la base de datos SQLite (igual que antes)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Crear tabla de clientes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    telefono TEXT NOT NULL UNIQUE,
                    email TEXT,
                    activo INTEGER DEFAULT 1,
                    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                    ultimo_envio DATETIME,
                    total_enviados INTEGER DEFAULT 0
                )
            ''')
            
            # Crear tabla de templates (para WhatsApp Business)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS templates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    template_name TEXT NOT NULL,
                    contenido TEXT NOT NULL,
                    language_code TEXT DEFAULT 'es',
                    estado TEXT DEFAULT 'pending',
                    activo INTEGER DEFAULT 1,
                    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Crear tabla de envíos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS envios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER,
                    template_id INTEGER,
                    mensaje TEXT,
                    estado TEXT,
                    fecha_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
                    respuesta_api TEXT,
                    message_id TEXT,
                    FOREIGN KEY (cliente_id) REFERENCES clientes (id),
                    FOREIGN KEY (template_id) REFERENCES templates (id)
                )
            ''')
            
            conn.commit()
            conn.close()
            
            # Cargar datos de ejemplo si está vacía
            self._load_sample_data()
            
            logger.info("✅ Base de datos inicializada correctamente")
            
        except Exception as e:
            logger.error(f"❌ Error inicializando base de datos: {e}")
    
    def _load_sample_data(self):
        """Carga templates de ejemplo para WhatsApp Business"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verificar si hay templates
            cursor.execute("SELECT COUNT(*) FROM templates")
            if cursor.fetchone()[0] == 0:
                # Templates para WhatsApp Business (deben ser aprobados por Meta)
                templates_ejemplo = [
                    ("hello_world", "hello_world", "Hello {{1}}, this is a test message.", "en"),
                    ("oferta_soat", "oferta_soat", "🚗 ¡Hola {{1}}! Tu SOAT vence pronto. Renuévalo con 30% descuento.", "es"),
                    ("recordatorio", "recordatorio_seguro", "⏰ {{1}}, tu póliza vence el {{2}}. Renueva antes del vencimiento.", "es")
                ]
                
                cursor.executemany(
                    "INSERT INTO templates (nombre, template_name, contenido, language_code) VALUES (?, ?, ?, ?)",
                    templates_ejemplo
                )
                
                logger.info("✅ Templates de ejemplo para WhatsApp Business insertados")
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Error cargando datos de ejemplo: {e}")
    
    def _load_templates(self) -> Dict[str, Dict]:
        """Carga templates desde base de datos"""
        templates = {}
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT nombre, template_name, contenido, language_code FROM templates WHERE activo = 1")
            for nombre, template_name, contenido, language_code in cursor.fetchall():
                templates[nombre] = {
                    'template_name': template_name,
                    'contenido': contenido,
                    'language_code': language_code
                }
            
            conn.close()
            logger.info(f"✅ {len(templates)} templates cargados")
            
        except Exception as e:
            logger.error(f"❌ Error cargando templates: {e}")
        
        return templates
    
    def test_conexion(self) -> Dict:
        """Prueba la conexión con WhatsApp Business API"""
        try:
            # Test con el endpoint de información de la cuenta
            url = f"{self.base_url}/me"
            
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'account_info': data,
                    'message': 'Conexión WhatsApp Business API exitosa'
                }
            else:
                return {
                    'success': False,
                    'message': f'Error de conexión: {response.status_code} - {response.text}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Error de conexión: {str(e)}'
            }
    
    def get_phone_number_info(self):
        """Obtiene información del número de teléfono configurado"""
        if self.phone_number_id == "NECESITAS_OBTENER_ESTO":
            return {
                'error': 'Phone Number ID no configurado. Ve a tu panel de Meta Developer.'
            }
        
        url = f"{self.base_url}/{self.phone_number_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def send_template_message(self, to_number: str, template_name: str, parameters: Optional[List[str]] = None, language_code: str = "en_US"):
        """Envía mensaje usando template aprobado de WhatsApp Business"""
        if self.phone_number_id == "NECESITAS_OBTENER_ESTO":
            return {
                'error': 'Phone Number ID no configurado'
            }
        
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        # Limpiar número de teléfono - dejar solo números (sin + ni espacios)
        clean_number = to_number.replace("+", "").replace(" ", "").replace("-", "")
        
        payload = {
            "messaging_product": "whatsapp",
            "to": clean_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
        }
        
        # Agregar parámetros si existen y el template los requiere
        if parameters and template_name != "hello_world":
            payload["template"]["components"] = [
                {
                    "type": "body",
                    "parameters": [{"type": "text", "text": param} for param in parameters]
                }
            ]
        
        try:
            logger.info(f"🚀 Enviando mensaje a {clean_number} usando template '{template_name}'")
            logger.info(f"📡 URL: {url}")
            logger.info(f"📦 Payload: {payload}")
            
            response = requests.post(url, headers=self.headers, json=payload)
            result = response.json()
            
            logger.info(f"📊 Status Code: {response.status_code}")
            logger.info(f"📋 Response: {result}")
            
            if response.status_code == 200:
                logger.info(f"✅ Mensaje enviado a {to_number}: {result.get('messages', [{}])[0].get('id', 'No ID')}")
                return {
                    'success': True,
                    'message_id': result.get('messages', [{}])[0].get('id'),
                    'response': result
                }
            else:
                logger.error(f"❌ Error enviando a {to_number}: {result}")
                return {
                    'success': False,
                    'error': result,
                    'response': result
                }
                
        except Exception as e:
            logger.error(f"❌ Excepción enviando a {to_number}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def agregar_cliente(self, nombre: str, telefono: str, email: Optional[str] = None) -> bool:
        """Agrega un nuevo cliente a la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO clientes (nombre, telefono, email) VALUES (?, ?, ?)",
                (nombre, telefono, email)
            )
            
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Cliente agregado: {nombre} - {telefono}")
            return True
            
        except sqlite3.IntegrityError:
            logger.warning(f"⚠️ Cliente ya existe: {telefono}")
            return False
        except Exception as e:
            logger.error(f"❌ Error agregando cliente: {e}")
            return False
    
    def obtener_clientes_activos(self) -> List[Dict]:
        """Obtiene lista de clientes activos"""
        clientes = []
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, nombre, telefono, email, total_enviados, ultimo_envio
                FROM clientes 
                WHERE activo = 1
                ORDER BY nombre
            """)
            
            for row in cursor.fetchall():
                clientes.append({
                    'id': row[0],
                    'nombre': row[1],
                    'telefono': row[2],
                    'email': row[3],
                    'total_enviados': row[4],
                    'ultimo_envio': row[5]
                })
            
            conn.close()
            logger.info(f"✅ {len(clientes)} clientes activos encontrados")
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo clientes: {e}")
        
        return clientes
    
    def obtener_templates_disponibles(self) -> List[Dict]:
        """Obtiene lista de templates disponibles"""
        templates = []
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT nombre, template_name, contenido, language_code, estado, fecha_creacion
                FROM templates 
                WHERE activo = 1
                ORDER BY nombre
            """)
            
            for row in cursor.fetchall():
                templates.append({
                    'nombre': row[0],
                    'template_name': row[1],
                    'contenido': row[2],
                    'language_code': row[3],
                    'estado': row[4],
                    'fecha_creacion': row[5]
                })
            
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo templates: {e}")
        
        return templates

# Instancia global del servicio
whatsapp_native_service = WhatsAppNativeService()

if __name__ == "__main__":
    print("🚀 WhatsApp Native Service - Reemplaza a Twilio")
    print("=" * 50)
    
    # Test de conexión
    result = whatsapp_native_service.test_conexion()
    if result['success']:
        print("✅ Conexión exitosa con WhatsApp Business API")
    else:
        print(f"❌ Error de conexión: {result['message']}")
    
    # Mostrar templates disponibles
    templates = whatsapp_native_service.obtener_templates_disponibles()
    print(f"\n📝 Templates disponibles: {len(templates)}")
    for template in templates:
        print(f"  - {template['nombre']} ({template['estado']})")
    
    # Mostrar clientes
    clientes = whatsapp_native_service.obtener_clientes_activos()
    print(f"\n👥 Clientes activos: {len(clientes)}")
    for cliente in clientes[:3]:  # Solo primeros 3
        print(f"  - {cliente['nombre']} - {cliente['telefono']}") 