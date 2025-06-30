#!/usr/bin/env python3
"""
🚀 Servicio Bot de Spam Masivo - PostgreSQL
Sistema para envío de templates masivos usando PostgreSQL (sin "database locked")
"""

import os
import time
import logging
import random
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from twilio.rest import Client
from dotenv import load_dotenv
import threading
import queue
import psycopg2
from psycopg2.extras import RealDictCursor

# Cargar variables de entorno
load_dotenv('.environment')

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SpamBotServicePG:
    """
    🤖 Servicio de Bot de Spam - PostgreSQL
    Envío masivo usando templates predefinidos con PostgreSQL
    """
    
    def __init__(self):
        # Configuración Twilio
        self.twilio_client = self._initialize_twilio()
        self.whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')
        
        # Configuración PostgreSQL
        self.pg_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'bot'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'root'),
            'port': int(os.getenv('DB_PORT', 5432))
        }
        
        # Inicializar base de datos
        self._initialize_database()
        
        # Templates específicos para Alesse Connect - Seguros
        self.sandbox_templates = {
            'soat_renovacion': {
                'nombre': '🚗 SOAT - Renovación Urgente',
                'descripcion': 'Hola {{1}}! Tu SOAT vence el {{2}}. Renuévalo con nosotros y ahorra hasta {{3}}% 💰 ¡No te quedes sin protección! Llama: {{4}}',
                'parametros': 4,
                'ejemplo': 'Hola Juan! Tu SOAT vence el 15 de Julio. Renuévalo con nosotros y ahorra hasta 25% 💰 ¡No te quedes sin protección! Llama: +51999888777'
            },
            'seguro_vehicular_promo': {
                'nombre': '🛡️ Seguro Vehicular - Oferta Especial',
                'descripcion': '¡{{1}}! 🎁 Oferta especial en seguro vehicular: {{2}} con {{3}}% descuento. Cobertura completa desde S/{{4}}. ¡Solo por tiempo limitado! 📞 Consulta ya',
                'parametros': 4,
                'ejemplo': '¡María! 🎁 Oferta especial en seguro vehicular: Todo Riesgo con 40% descuento. Cobertura completa desde S/299. ¡Solo por tiempo limitado! 📞 Consulta ya'
            },
            'recordatorio_poliza': {
                'nombre': '⏰ Recordatorio - Póliza por Vencer',
                'descripcion': 'Estimado/a {{1}}, tu póliza {{2}} vence en {{3}} días. 📋 Renueva antes del {{4}} y mantén tu protección activa. ¡Evita multas y sanciones! 🚨',
                'parametros': 4,
                'ejemplo': 'Estimado/a Carlos, tu póliza SOAT vence en 7 días. 📋 Renueva antes del 30 de Julio y mantén tu protección activa. ¡Evita multas y sanciones! 🚨'
            },
            'promocion_masiva': {
                'nombre': '🎯 Promoción Masiva - Alesse',
                'descripcion': '¡Hola {{1}}! 🔥 ¡MEGA OFERTA! {{2}} con {{3}}% OFF. Protege tu {{4}} desde S/{{5}} mensuales. ✅ Cobertura total ✅ Atención 24/7. ¡Llamanos YA! 📱',
                'parametros': 5,
                'ejemplo': '¡Hola Pedro! 🔥 ¡MEGA OFERTA! Seguro Vehicular con 50% OFF. Protege tu auto desde S/199 mensuales. ✅ Cobertura total ✅ Atención 24/7. ¡Llamanos YA! 📱'
            },
            'cliente_nuevo_bienvenida': {
                'nombre': '🤝 Bienvenida Cliente Nuevo',
                'descripcion': '¡Bienvenido a Alesse Connect, {{1}}! 🎉 Tu {{2}} está activo. Número de póliza: {{3}}. Cualquier consulta al {{4}}. ¡Gracias por confiar en nosotros! 💪',
                'parametros': 4,
                'ejemplo': '¡Bienvenido a Alesse Connect, Ana! 🎉 Tu SOAT está activo. Número de póliza: SOA-2024-001234. Cualquier consulta al +51999888777. ¡Gracias por confiar en nosotros! 💪'
            },
            'seguimiento_cotizacion': {
                'nombre': '💬 Seguimiento de Cotización',
                'descripcion': 'Hola {{1}}, vimos que cotizaste {{2}} hace {{3}} días. 🤔 ¿Tienes alguna duda? Te ofrecemos {{4}}% descuento adicional si decides hoy. ¿Te interesa? 🎯',
                'parametros': 4,
                'ejemplo': 'Hola Luis, vimos que cotizaste Seguro Vehicular hace 3 días. 🤔 ¿Tienes alguna duda? Te ofrecemos 15% descuento adicional si decides hoy. ¿Te interesa? 🎯'
            }
        }
        
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
        
        logger.info("🤖 SpamBotService inicializado con PostgreSQL")
    
    def _get_connection(self):
        """Obtener conexión a PostgreSQL con manejo de errores"""
        try:
            conn = psycopg2.connect(**self.pg_config)
            return conn
        except Exception as e:
            logger.error(f"❌ Error conectando PostgreSQL: {e}")
            return None
    
    def _initialize_twilio(self) -> Optional[Client]:
        """Inicializa cliente Twilio"""
        try:
            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            
            if account_sid and auth_token:
                client = Client(account_sid, auth_token)
                logger.info("✅ Twilio Sandbox configurado para spam bot")
                return client
            else:
                logger.error("❌ Credenciales Twilio no encontradas")
                return None
        except Exception as e:
            logger.error(f"❌ Error configurando Twilio: {e}")
            return None
    
    def _initialize_database(self):
        """Inicializa la base de datos PostgreSQL"""
        try:
            conn = self._get_connection()
            if not conn:
                logger.error("❌ No se pudo conectar a PostgreSQL")
                return
            
            cursor = conn.cursor()
            
            # Crear tabla de clientes
            cursor.execute('''
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
            ''')
            
            # Crear tabla de envíos
            cursor.execute('''
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
            ''')
            
            # Crear tabla de campañas
            cursor.execute('''
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
            ''')
            
            conn.commit()
            conn.close()
            
            # Cargar datos de ejemplo si está vacía
            self._load_sample_data()
            
            logger.info("✅ Base de datos PostgreSQL inicializada correctamente")
            
        except Exception as e:
            logger.error(f"❌ Error inicializando base de datos: {e}")
    
    def _load_sample_data(self):
        """Carga datos de ejemplo si la base está vacía"""
        try:
            conn = self._get_connection()
            if not conn:
                return
                
            cursor = conn.cursor()
            
            # Verificar si hay clientes
            cursor.execute("SELECT COUNT(*) FROM clientes")
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Insertar clientes de ejemplo
                clientes_ejemplo = [
                    ("Juan Pérez", "+51999123456", "juan@email.com"),
                    ("María García", "+51999234567", "maria@email.com"),
                    ("Carlos López", "+51999345678", "carlos@email.com"),
                    ("Ana Martín", "+51999456789", "ana@email.com"),
                    ("Pedro Sánchez", "+51999567890", "pedro@email.com")
                ]
                
                for nombre, telefono, email in clientes_ejemplo:
                    cursor.execute(
                        "INSERT INTO clientes (nombre, telefono, email) VALUES (%s, %s, %s)",
                        (nombre, telefono, email)
                    )
                
                logger.info("✅ Clientes de ejemplo insertados")
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Error cargando datos de ejemplo: {e}")
    
    def agregar_cliente(self, nombre: str, telefono: str, email: Optional[str] = None) -> bool:
        """Agrega un nuevo cliente a la base de datos"""
        try:
            conn = self._get_connection()
            if not conn:
                return False
                
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO clientes (nombre, telefono, email) VALUES (%s, %s, %s)",
                (nombre, telefono, email)
            )
            
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Cliente agregado: {nombre} - {telefono}")
            return True
            
        except psycopg2.IntegrityError:
            logger.warning(f"⚠️ Cliente ya existe: {telefono}")
            return False
        except Exception as e:
            logger.error(f"❌ Error agregando cliente: {e}")
            return False
    
    def obtener_clientes_activos(self) -> List[Dict]:
        """Obtiene lista de clientes activos"""
        clientes = []
        try:
            conn = self._get_connection()
            if not conn:
                return clientes
                
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT id, nombre, telefono, email, total_enviados, ultimo_envio
                FROM clientes 
                WHERE activo = true
                ORDER BY nombre
            """)
            
            rows = cursor.fetchall()
            for row in rows:
                clientes.append(dict(row))
            
            conn.close()
            logger.info(f"✅ {len(clientes)} clientes activos encontrados")
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo clientes: {e}")
        
        return clientes
    
    def obtener_templates_disponibles(self) -> List[Dict]:
        """Obtiene lista de templates disponibles del sandbox"""
        templates = []
        for key, template in self.sandbox_templates.items():
            templates.append({
                'id': key,
                'nombre': template['nombre'],
                'descripcion': template['descripcion'],
                'parametros': template['parametros'],
                'ejemplo': template['ejemplo']
            })
        return templates
    
    def crear_mensaje_personalizado(self, template_key: str, cliente: Dict, parametros_custom: Optional[List[str]] = None) -> Tuple[str, List[str]]:
        """Crea mensaje personalizado para templates de seguros de Alesse"""
        if template_key not in self.sandbox_templates:
            raise ValueError(f"Template '{template_key}' no disponible")
        
        template = self.sandbox_templates[template_key]
        nombre_cliente = cliente['nombre']
        
        # Parámetros por defecto según el template de seguros
        if template_key == 'soat_renovacion':
            parametros = parametros_custom if parametros_custom is not None else [
                nombre_cliente,
                f"{datetime.now() + timedelta(days=random.randint(7, 30)):%d de %B}",  # Fecha vencimiento
                str(random.randint(20, 35)),  # Descuento %
                "+51999888777"  # Teléfono contacto
            ]
            mensaje_preview = f"Hola {parametros[0]}! Tu SOAT vence el {parametros[1]}. Renuévalo con nosotros y ahorra hasta {parametros[2]}% 💰 ¡No te quedes sin protección! Llama: {parametros[3]}"
            
        elif template_key == 'seguro_vehicular_promo':
            parametros = parametros_custom if parametros_custom is not None else [
                nombre_cliente,
                random.choice(["Todo Riesgo", "Terceros Completo", "Responsabilidad Civil"]),  # Tipo seguro
                str(random.randint(30, 50)),  # Descuento %
                str(random.randint(199, 399))  # Precio desde
            ]
            mensaje_preview = f"¡{parametros[0]}! 🎁 Oferta especial en seguro vehicular: {parametros[1]} con {parametros[2]}% descuento. Cobertura completa desde S/{parametros[3]}. ¡Solo por tiempo limitado! 📞 Consulta ya"
            
        elif template_key == 'recordatorio_poliza':
            parametros = parametros_custom if parametros_custom is not None else [
                nombre_cliente,
                random.choice(["SOAT", "Seguro Vehicular", "Responsabilidad Civil"]),  # Tipo póliza
                str(random.randint(5, 15)),  # Días para vencer
                f"{datetime.now() + timedelta(days=random.randint(5, 15)):%d de %B}"  # Fecha límite
            ]
            mensaje_preview = f"Estimado/a {parametros[0]}, tu póliza {parametros[1]} vence en {parametros[2]} días. 📋 Renueva antes del {parametros[3]} y mantén tu protección activa. ¡Evita multas y sanciones! 🚨"
            
        elif template_key == 'promocion_masiva':
            parametros = parametros_custom if parametros_custom is not None else [
                nombre_cliente,
                random.choice(["SOAT 2025", "Seguro Todo Riesgo", "Seguro Familiar"]),  # Producto
                str(random.randint(40, 60)),  # Descuento %
                random.choice(["auto", "moto", "vehículo"]),  # Tipo vehículo
                str(random.randint(149, 299))  # Precio mensual
            ]
            mensaje_preview = f"¡Hola {parametros[0]}! 🔥 ¡MEGA OFERTA! {parametros[1]} con {parametros[2]}% OFF. Protege tu {parametros[3]} desde S/{parametros[4]} mensuales. ✅ Cobertura total ✅ Atención 24/7. ¡Llamanos YA! 📱"
            
        elif template_key == 'cliente_nuevo_bienvenida':
            parametros = parametros_custom if parametros_custom is not None else [
                nombre_cliente,
                random.choice(["SOAT", "Seguro Vehicular", "Seguro Todo Riesgo"]),  # Producto contratado
                f"SOA-{datetime.now().year}-{random.randint(100000, 999999)}",  # Número póliza
                "+51999888777"  # Teléfono contacto
            ]
            mensaje_preview = f"¡Bienvenido a Alesse Connect, {parametros[0]}! 🎉 Tu {parametros[1]} está activo. Número de póliza: {parametros[2]}. Cualquier consulta al {parametros[3]}. ¡Gracias por confiar en nosotros! 💪"
            
        elif template_key == 'seguimiento_cotizacion':
            parametros = parametros_custom if parametros_custom is not None else [
                nombre_cliente,
                random.choice(["SOAT", "Seguro Vehicular", "Todo Riesgo", "Responsabilidad Civil"]),  # Producto cotizado
                str(random.randint(1, 7)),  # Días desde cotización
                str(random.randint(10, 25))  # Descuento adicional %
            ]
            mensaje_preview = f"Hola {parametros[0]}, vimos que cotizaste {parametros[1]} hace {parametros[2]} días. 🤔 ¿Tienes alguna duda? Te ofrecemos {parametros[3]}% descuento adicional si decides hoy. ¿Te interesa? 🎯"
        
        else:
            parametros = [nombre_cliente]
            mensaje_preview = f"Hola {nombre_cliente}, mensaje de prueba desde Alesse Connect"
        
        return mensaje_preview, parametros
    
    def enviar_mensaje_template_sandbox(self, cliente: Dict, template_key: str, parametros: Optional[List[str]] = None) -> Tuple[bool, str]:
        """Envía mensaje usando templates del sandbox de Twilio"""
        if not self.twilio_client:
            return False, "Cliente Twilio no inicializado"
        
        try:
            # Crear mensaje personalizado
            mensaje_preview, params_finales = self.crear_mensaje_personalizado(template_key, cliente, parametros)
            
            # Formatear número de teléfono
            numero_destino = cliente['telefono']
            if not numero_destino.startswith('whatsapp:'):
                numero_destino = f"whatsapp:{numero_destino}"
            
            # Enviar mensaje de texto normal (sandbox no requiere templates aprobados)
            message = self.twilio_client.messages.create(
                body=mensaje_preview,
                from_=self.whatsapp_number,
                to=numero_destino
            )
            
            message_sid = message.sid or "no_sid"
            logger.info(f"✅ Mensaje enviado a {cliente['nombre']}: {message_sid}")
            return True, message_sid
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ Error enviando a {cliente['nombre']}: {error_msg}")
            return False, error_msg
    
    def enviar_campaña_masiva(self, template_key: str, parametros_custom: Optional[List[str]] = None, delay_min: int = 5, delay_max: int = 15) -> Dict:
        """Envía campaña masiva usando template del sandbox"""
        if self.is_sending:
            return {
                'success': False,
                'message': 'Ya hay un envío en progreso'
            }
        
        if template_key not in self.sandbox_templates:
            return {
                'success': False,
                'message': f'Template "{template_key}" no disponible'
            }
        
        # Inicializar estadísticas
        self.stats = {
            'enviados': 0,
            'fallidos': 0,
            'total': 0,
            'inicio': datetime.now(),
            'fin': None,
            'template': template_key
        }
        
        # Obtener clientes activos
        clientes = self.obtener_clientes_activos()
        self.stats['total'] = len(clientes)
        
        if not clientes:
            return {
                'success': False,
                'message': 'No hay clientes activos para enviar'
            }
        
        # Registrar campaña en BD
        campaña_id = self._registrar_campaña(template_key, len(clientes))
        
        # Iniciar envío en hilo separado
        self.is_sending = True
        thread = threading.Thread(
            target=self._proceso_envio_masivo,
            args=(clientes, template_key, parametros_custom, delay_min, delay_max, campaña_id)
        )
        thread.daemon = True
        thread.start()
        
        return {
            'success': True,
            'message': f'Iniciando envío masivo a {len(clientes)} clientes',
            'total_clientes': len(clientes),
            'template': template_key,
            'campaña_id': campaña_id
        }
    
    def _proceso_envio_masivo(self, clientes: List[Dict], template_key: str, parametros_custom: Optional[List[str]], delay_min: int, delay_max: int, campaña_id: int):
        """Proceso de envío masivo en hilo separado con PostgreSQL"""
        try:
            for cliente in clientes:
                if not self.is_sending:  # Permite cancelar el envío
                    break
                
                # Crear una nueva conexión para cada cliente para evitar locks
                conn = self._get_connection()
                if not conn:
                    logger.error("❌ No se pudo conectar a PostgreSQL")
                    self.stats['fallidos'] += 1
                    continue
                
                try:
                    cursor = conn.cursor()
                    
                    # Enviar mensaje
                    exito, respuesta = self.enviar_mensaje_template_sandbox(cliente, template_key, parametros_custom)
                    
                    # Registrar en base de datos
                    estado = 'enviado' if exito else 'fallido'
                    _, parametros_usados = self.crear_mensaje_personalizado(template_key, cliente, parametros_custom)
                    
                    cursor.execute("""
                        INSERT INTO envios (cliente_id, template_usado, parametros, estado, respuesta_twilio, message_sid)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        cliente['id'],
                        template_key,
                        str(parametros_usados),
                        estado,
                        respuesta,
                        respuesta if exito else None
                    ))
                    
                    # Actualizar cliente
                    if exito:
                        cursor.execute("""
                            UPDATE clientes 
                            SET ultimo_envio = CURRENT_TIMESTAMP, total_enviados = total_enviados + 1
                            WHERE id = %s
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
                finally:
                    conn.close()
            
            # Actualizar estadísticas de campaña
            self._actualizar_estadisticas_campaña(campaña_id, self.stats['enviados'], self.stats['fallidos'])
            
        except Exception as e:
            logger.error(f"❌ Error en proceso de envío masivo: {e}")
        finally:
            self.stats['fin'] = datetime.now()
            self.is_sending = False
            
            logger.info(f"🏁 Envío masivo completado: {self.stats['enviados']} enviados, {self.stats['fallidos']} fallidos")
    
    def _registrar_campaña(self, template_key: str, total_clientes: int) -> int:
        """Registra una nueva campaña en la base de datos"""
        try:
            conn = self._get_connection()
            if not conn:
                return 0
                
            cursor = conn.cursor()
            
            template_info = self.sandbox_templates[template_key]
            
            cursor.execute("""
                INSERT INTO campañas (nombre, template_usado, descripcion, fecha_ejecucion, total_enviados, estado)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP, %s, 'en_progreso')
                RETURNING id
            """, (
                template_info['nombre'],
                template_key,
                template_info['descripcion'],
                total_clientes
            ))
            
            campaña_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            
            return campaña_id
            
        except Exception as e:
            logger.error(f"❌ Error registrando campaña: {e}")
            return 0
    
    def _actualizar_estadisticas_campaña(self, campaña_id: int, exitosos: int, fallidos: int):
        """Actualiza las estadísticas de una campaña"""
        try:
            conn = self._get_connection()
            if not conn:
                return
                
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE campañas 
                SET total_exitosos = %s, total_fallidos = %s, estado = 'completada'
                WHERE id = %s
            """, (exitosos, fallidos, campaña_id))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Error actualizando estadísticas de campaña: {e}")
    
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
            conn = self._get_connection()
            if not conn:
                return historial
                
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT e.id, c.nombre, c.telefono, e.template_usado, 
                       e.estado, e.fecha_envio, e.parametros, e.mensaje
                FROM envios e
                JOIN clientes c ON e.cliente_id = c.id
                ORDER BY e.fecha_envio DESC
                LIMIT %s
            """, (limite,))
            
            rows = cursor.fetchall()
            for row in rows:
                historial.append(dict(row))
            
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo historial: {e}")
        
        return historial
    
    def test_conexion(self) -> Dict:
        """Prueba la conexión con Twilio"""
        if not self.twilio_client:
            return {
                'success': False,
                'message': 'Cliente Twilio no inicializado'
            }
        
        try:
            # Probar obteniendo información de la cuenta
            account_sid = self.twilio_client.account_sid
            if not account_sid:
                return {
                    'success': False,
                    'message': 'Account SID no disponible'
                }
            
            account = self.twilio_client.api.accounts(account_sid).fetch()
            
            return {
                'success': True,
                'message': 'Conexión exitosa con Twilio',
                'account_name': account.friendly_name,
                'account_sid': account.sid,
                'status': account.status,
                'whatsapp_number': self.whatsapp_number
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error de conexión: {str(e)}'
            }

# Instancia global del servicio PostgreSQL
spam_service = SpamBotServicePG() 