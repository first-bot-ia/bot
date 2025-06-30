#!/usr/bin/env python3
"""
🚀 Servicio Bot de Spam Masivo
Sistema para envío de templates masivos a clientes desde base de datos
"""

import os
import sqlite3
import time
import logging
import random
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from twilio.rest import Client
from dotenv import load_dotenv
import threading
import queue

# Cargar variables de entorno
load_dotenv('.environment')

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SpamBotService:
    """
    🤖 Servicio de Bot de Spam
    Envío masivo de templates a base de datos de clientes
    """
    
    def __init__(self):
        # Configuración Twilio
        self.twilio_client = self._initialize_twilio()
        self.whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
        
        # Base de datos
        self.db_path = 'clientes_spam.db'
        self._initialize_database()
        
        # Templates predefinidos
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
        
        logger.info("🤖 SpamBotService inicializado correctamente")
    
    def _initialize_twilio(self) -> Optional[Client]:
        """Inicializa cliente Twilio"""
        try:
            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            
            if account_sid and auth_token:
                client = Client(account_sid, auth_token)
                logger.info("✅ Twilio configurado para spam bot")
                return client
            else:
                logger.error("❌ Credenciales Twilio no encontradas")
                return None
        except Exception as e:
            logger.error(f"❌ Error configurando Twilio: {e}")
            return None
    
    def _initialize_database(self):
        """Inicializa la base de datos SQLite"""
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
            
            # Crear tabla de templates
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS templates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    contenido TEXT NOT NULL,
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
                    estado TEXT, -- 'enviado', 'fallido', 'pendiente'
                    fecha_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
                    respuesta_twilio TEXT,
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
        """Carga datos de ejemplo si la base está vacía"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verificar si hay clientes
            cursor.execute("SELECT COUNT(*) FROM clientes")
            if cursor.fetchone()[0] == 0:
                # Insertar clientes de ejemplo
                clientes_ejemplo = [
                    ("Juan Pérez", "+51999123456", "juan@email.com"),
                    ("María García", "+51999234567", "maria@email.com"),
                    ("Carlos López", "+51999345678", "carlos@email.com"),
                    ("Ana Martín", "+51999456789", "ana@email.com"),
                    ("Pedro Sánchez", "+51999567890", "pedro@email.com")
                ]
                
                cursor.executemany(
                    "INSERT INTO clientes (nombre, telefono, email) VALUES (?, ?, ?)",
                    clientes_ejemplo
                )
                
                logger.info("✅ Clientes de ejemplo insertados")
            
            # Verificar si hay templates
            cursor.execute("SELECT COUNT(*) FROM templates")
            if cursor.fetchone()[0] == 0:
                # Insertar templates de ejemplo
                templates_ejemplo = [
                    ("Promoción SOAT", "🚗 ¡Hola {nombre}! Tu SOAT está por vencer. Renuévalo con nosotros y ahorra hasta 30%. ¡No te quedes sin protección! 📞 Llámanos: +51999888777"),
                    ("Seguro Vehicular", "🛡️ ¡{nombre}! Protege tu vehículo con nuestro seguro todo riesgo. Cobertura completa desde S/299. ¡Consulta ya! 🚙"),
                    ("Recordatorio Renovación", "⏰ Estimado/a {nombre}, tu póliza vence pronto. Renueva antes del vencimiento y mantén tu protección activa. 📋"),
                    ("Oferta Especial", "🎉 ¡OFERTA ESPECIAL para {nombre}! 50% de descuento en tu segundo seguro. Solo por tiempo limitado. ¡Aprovecha ya! 💰"),
                    ("Saludo Personalizado", "👋 ¡Hola {nombre}! Somos Alesse Seguros, tu mejor opción en protección vehicular. ¿Necesitas ayuda con algún seguro? 🤝")
                ]
                
                cursor.executemany(
                    "INSERT INTO templates (nombre, contenido) VALUES (?, ?)",
                    templates_ejemplo
                )
                
                logger.info("✅ Templates de ejemplo insertados")
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Error cargando datos de ejemplo: {e}")
    
    def _load_templates(self) -> Dict[str, str]:
        """Carga templates desde base de datos"""
        templates = {}
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT nombre, contenido FROM templates WHERE activo = 1")
            for nombre, contenido in cursor.fetchall():
                templates[nombre] = contenido
            
            conn.close()
            logger.info(f"✅ {len(templates)} templates cargados")
            
        except Exception as e:
            logger.error(f"❌ Error cargando templates: {e}")
        
        return templates
    
    def agregar_cliente(self, nombre: str, telefono: str, email: str = None) -> bool:
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
    
    def crear_template(self, nombre: str, contenido: str) -> bool:
        """Crea un nuevo template"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO templates (nombre, contenido) VALUES (?, ?)",
                (nombre, contenido)
            )
            
            conn.commit()
            conn.close()
            
            # Recargar templates
            self.templates = self._load_templates()
            
            logger.info(f"✅ Template creado: {nombre}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error creando template: {e}")
            return False
    
    def personalizar_mensaje(self, template: str, cliente: Dict) -> str:
        """Personaliza un template con datos del cliente"""
        mensaje = template.replace('{nombre}', cliente['nombre'])
        mensaje = mensaje.replace('{telefono}', cliente['telefono'])
        if cliente.get('email'):
            mensaje = mensaje.replace('{email}', cliente['email'])
        
        return mensaje
    
    def enviar_mensaje_individual(self, cliente: Dict, mensaje: str) -> Tuple[bool, str]:
        """Envía un mensaje individual a un cliente"""
        if not self.twilio_client:
            return False, "Cliente Twilio no inicializado"
        
        try:
            # Formatear número de teléfono
            numero_destino = f"whatsapp:{cliente['telefono']}"
            
            # Enviar mensaje
            message = self.twilio_client.messages.create(
                body=mensaje,
                from_=self.whatsapp_number,
                to=numero_destino
            )
            
            logger.info(f"✅ Mensaje enviado a {cliente['nombre']}: {message.sid}")
            return True, message.sid
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ Error enviando a {cliente['nombre']}: {error_msg}")
            return False, error_msg
    
    def enviar_spam_masivo(self, template_nombre: str, delay_min: int = 5, delay_max: int = 15) -> Dict:
        """Envía spam masivo usando un template específico"""
        if self.is_sending:
            return {
                'success': False,
                'message': 'Ya hay un envío en progreso'
            }
        
        if template_nombre not in self.templates:
            return {
                'success': False,
                'message': f'Template "{template_nombre}" no encontrado'
            }
        
        # Inicializar estadísticas
        self.stats = {
            'enviados': 0,
            'fallidos': 0,
            'total': 0,
            'inicio': datetime.now(),
            'fin': None,
            'template': template_nombre
        }
        
        # Obtener clientes activos
        clientes = self.obtener_clientes_activos()
        self.stats['total'] = len(clientes)
        
        if not clientes:
            return {
                'success': False,
                'message': 'No hay clientes activos para enviar'
            }
        
        # Iniciar envío en hilo separado
        self.is_sending = True
        thread = threading.Thread(
            target=self._proceso_envio_masivo,
            args=(clientes, template_nombre, delay_min, delay_max)
        )
        thread.daemon = True
        thread.start()
        
        return {
            'success': True,
            'message': f'Iniciando envío masivo a {len(clientes)} clientes',
            'total_clientes': len(clientes),
            'template': template_nombre
        }
    
    def _proceso_envio_masivo(self, clientes: List[Dict], template_nombre: str, delay_min: int, delay_max: int):
        """Proceso de envío masivo en hilo separado"""
        template = self.templates[template_nombre]
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for cliente in clientes:
                if not self.is_sending:  # Permite cancelar el envío
                    break
                
                try:
                    # Personalizar mensaje
                    mensaje = self.personalizar_mensaje(template, cliente)
                    
                    # Enviar mensaje
                    exito, respuesta = self.enviar_mensaje_individual(cliente, mensaje)
                    
                    # Registrar en base de datos
                    estado = 'enviado' if exito else 'fallido'
                    cursor.execute("""
                        INSERT INTO envios (cliente_id, template_id, mensaje, estado, respuesta_twilio)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        cliente['id'],
                        self._get_template_id(template_nombre),
                        mensaje,
                        estado,
                        respuesta
                    ))
                    
                    # Actualizar cliente
                    if exito:
                        cursor.execute("""
                            UPDATE clientes 
                            SET ultimo_envio = CURRENT_TIMESTAMP, total_enviados = total_enviados + 1
                            WHERE id = ?
                        """, (cliente['id'],))
                        self.stats['enviados'] += 1
                    else:
                        self.stats['fallidos'] += 1
                    
                    conn.commit()
                    
                    # Delay entre envíos para parecer humano
                    delay = random.randint(delay_min, delay_max)
                    logger.info(f"💤 Esperando {delay}s antes del siguiente envío...")
                    time.sleep(delay)
                    
                except Exception as e:
                    logger.error(f"❌ Error procesando cliente {cliente['nombre']}: {e}")
                    self.stats['fallidos'] += 1
            
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Error en proceso de envío masivo: {e}")
        finally:
            self.stats['fin'] = datetime.now()
            self.is_sending = False
            
            logger.info(f"🏁 Envío masivo completado: {self.stats['enviados']} enviados, {self.stats['fallidos']} fallidos")
    
    def _get_template_id(self, template_nombre: str) -> Optional[int]:
        """Obtiene el ID de un template por nombre"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT id FROM templates WHERE nombre = ?", (template_nombre,))
            result = cursor.fetchone()
            
            conn.close()
            
            return result[0] if result else None
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo template ID: {e}")
            return None
    
    def obtener_estadisticas(self) -> Dict:
        """Obtiene estadísticas del envío actual"""
        stats = self.stats.copy()
        
        if stats['inicio']:
            if stats['fin']:
                duracion = stats['fin'] - stats['inicio']
            else:
                duracion = datetime.now() - stats['inicio']
            
            stats['duracion_segundos'] = duracion.total_seconds()
            stats['duracion_formateada'] = str(duracion).split('.')[0]  # Sin microsegundos
        
        stats['en_progreso'] = self.is_sending
        
        return stats
    
    def cancelar_envio(self) -> bool:
        """Cancela el envío en progreso"""
        if self.is_sending:
            self.is_sending = False
            logger.info("🛑 Envío masivo cancelado por usuario")
            return True
        return False
    
    def obtener_historial_envios(self, limite: int = 50) -> List[Dict]:
        """Obtiene historial de envíos recientes"""
        historial = []
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT e.id, c.nombre, c.telefono, t.nombre as template, 
                       e.estado, e.fecha_envio, e.mensaje
                FROM envios e
                JOIN clientes c ON e.cliente_id = c.id
                JOIN templates t ON e.template_id = t.id
                ORDER BY e.fecha_envio DESC
                LIMIT ?
            """, (limite,))
            
            for row in cursor.fetchall():
                historial.append({
                    'id': row[0],
                    'cliente': row[1],
                    'telefono': row[2],
                    'template': row[3],
                    'estado': row[4],
                    'fecha': row[5],
                    'mensaje': row[6][:100] + '...' if len(row[6]) > 100 else row[6]
                })
            
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo historial: {e}")
        
        return historial
    
    def obtener_templates_disponibles(self) -> List[Dict]:
        """Obtiene lista de templates disponibles"""
        templates = []
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT nombre, contenido, fecha_creacion
                FROM templates 
                WHERE activo = 1
                ORDER BY nombre
            """)
            
            for row in cursor.fetchall():
                templates.append({
                    'nombre': row[0],
                    'contenido': row[1],
                    'fecha_creacion': row[2]
                })
            
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo templates: {e}")
        
        return templates
    
    def test_conexion(self) -> Dict:
        """Prueba la conexión con Twilio"""
        if not self.twilio_client:
            return {
                'success': False,
                'message': 'Cliente Twilio no inicializado'
            }
        
        try:
            # Obtener información de la cuenta
            account = self.twilio_client.api.accounts(self.twilio_client.username).fetch()
            
            return {
                'success': True,
                'account_sid': account.sid,
                'account_name': account.friendly_name,
                'whatsapp_number': self.whatsapp_number,
                'message': 'Conexión Twilio exitosa'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error de conexión: {str(e)}'
            }

# Instancia global del servicio
spam_service = SpamBotService()