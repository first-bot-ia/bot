"""
Servicio de Twilio para envío de mensajes de WhatsApp
"""
from typing import Tuple, Dict, List
import random
from datetime import datetime, timedelta
from twilio.rest import Client as TwilioClient

from config.settings import TwilioConfig
from domain.entities.client import Client
from domain.value_objects.message_template import MessageTemplate


class TwilioWhatsAppService:
    """
    Servicio para envío de mensajes de WhatsApp a través de Twilio
    """
    
    def __init__(self, config: TwilioConfig):
        self.config = config
        self.client = TwilioClient(config.account_sid, config.auth_token)
        
        # Templates predefinidos para el sistema
        self.templates = {
            'soat_renovacion': MessageTemplate(
                key='soat_renovacion',
                name='🚗 SOAT - Renovación Urgente',
                description='Hola {{1}}! Tu SOAT vence el {{2}}. Renuévalo con nosotros y ahorra hasta {{3}}% 💰 ¡No te quedes sin protección! Llama: {{4}}',
                parameters_count=4,
                example='Hola Juan! Tu SOAT vence el 15 de Julio. Renuévalo con nosotros y ahorra hasta 25% 💰 ¡No te quedes sin protección! Llama: +51999888777'
            ),
            'promocion_masiva': MessageTemplate(
                key='promocion_masiva',
                name='🎯 Promoción Masiva - Alesse',
                description='¡Hola {{1}}! 🔥 ¡MEGA OFERTA! {{2}} con {{3}}% OFF. Protege tu {{4}} desde S/{{5}} mensuales. ✅ Cobertura total ✅ Atención 24/7. ¡Llamanos YA! 📱',
                parameters_count=5,
                example='¡Hola Pedro! 🔥 ¡MEGA OFERTA! Seguro Vehicular con 50% OFF. Protege tu auto desde S/199 mensuales. ✅ Cobertura total ✅ Atención 24/7. ¡Llamanos YA! 📱'
            ),
            'recordatorio_poliza': MessageTemplate(
                key='recordatorio_poliza',
                name='⏰ Recordatorio - Póliza por Vencer',
                description='Estimado/a {{1}}, tu póliza {{2}} vence en {{3}} días. 📋 Renueva antes del {{4}} y mantén tu protección activa. ¡Evita multas y sanciones! 🚨',
                parameters_count=4,
                example='Estimado/a Carlos, tu póliza SOAT vence en 7 días. 📋 Renueva antes del 30 de Julio y mantén tu protección activa. ¡Evita multas y sanciones! 🚨'
            )
        }
    
    def get_available_templates(self) -> List[MessageTemplate]:
        """Obtiene templates disponibles"""
        return list(self.templates.values())
    
    def get_template(self, template_key: str) -> MessageTemplate:
        """Obtiene un template específico"""
        if template_key not in self.templates:
            raise ValueError(f"Template '{template_key}' no disponible")
        return self.templates[template_key]
    
    def generate_default_parameters(self, template_key: str, client: Client) -> List[str]:
        """Genera parámetros por defecto para un template"""
        template = self.get_template(template_key)
        
        if template_key == 'soat_renovacion':
            return [
                client.nombre,
                f"{datetime.now() + timedelta(days=random.randint(7, 30)):%d de %B}",
                str(random.randint(20, 35)),
                "+51999888777"
            ]
        elif template_key == 'promocion_masiva':
            return [
                client.nombre,
                random.choice(["SOAT 2025", "Seguro Todo Riesgo", "Seguro Familiar"]),
                str(random.randint(40, 60)),
                random.choice(["auto", "moto", "vehículo"]),
                str(random.randint(149, 299))
            ]
        elif template_key == 'recordatorio_poliza':
            return [
                client.nombre,
                random.choice(["SOAT", "Seguro Vehicular", "Responsabilidad Civil"]),
                str(random.randint(5, 15)),
                f"{datetime.now() + timedelta(days=random.randint(5, 15)):%d de %B}"
            ]
        else:
            # Parámetros por defecto genéricos
            return [client.nombre] + [f"param_{i}" for i in range(2, template.parameters_count + 1)]
    
    def send_message(self, client: Client, template_key: str, parameters: List[str] | None = None) -> Tuple[bool, str]:
        """
        Envía mensaje de WhatsApp a un cliente
        
        Args:
            client: Cliente destinatario
            template_key: Clave del template a usar
            parameters: Parámetros del mensaje (opcional, se generan automáticamente)
            
        Returns:
            Tuple[bool, str]: (éxito, message_sid o error)
        """
        try:
            template = self.get_template(template_key)
            
            # Usar parámetros proporcionados o generar automáticamente
            if parameters is None:
                parameters = self.generate_default_parameters(template_key, client)
            
            # Asegurar que tenemos parámetros válidos
            assert parameters is not None, "Parámetros no pueden ser None después de generación"
            
            # Validar parámetros
            if not template.validate_parameters(parameters):
                return False, "Parámetros inválidos para el template"
            
            # Formatear mensaje
            message_content = template.format_message(parameters)
            
            # Enviar a través de Twilio
            message = self.client.messages.create(
                body=message_content,
                from_=self.config.whatsapp_number,
                to=client.get_whatsapp_number()
            )
            
            return True, message.sid or "unknown_sid"
            
        except Exception as e:
            error_msg = str(e)
            print(f"Error enviando mensaje a {client.nombre}: {error_msg}")
            return False, error_msg
    
    def send_bulk_messages(self, clients: List[Client], template_key: str, 
                          delay_seconds: int = 3) -> Dict[str, int]:
        """
        Envía mensajes masivos a múltiples clientes
        
        Args:
            clients: Lista de clientes
            template_key: Template a usar
            delay_seconds: Segundos entre envíos
            
        Returns:
            Dict con estadísticas: {"enviados": int, "fallidos": int}
        """
        stats = {"enviados": 0, "fallidos": 0}
        
        for client in clients:
            success, result = self.send_message(client, template_key)
            
            if success:
                stats["enviados"] += 1
                print(f"✅ Mensaje enviado a {client.nombre}: {result}")
            else:
                stats["fallidos"] += 1
                print(f"❌ Error enviando a {client.nombre}: {result}")
            
            # Delay entre mensajes para parecer más humano
            if delay_seconds > 0:
                import time
                time.sleep(delay_seconds)
        
        return stats
    
    def test_connection(self) -> Tuple[bool, str]:
        """Prueba la conexión con Twilio"""
        try:
            # Intentar obtener información de la cuenta
            account = self.client.api.account.fetch()
            return True, f"Conexión exitosa: {account.friendly_name}"
        except Exception as e:
            return False, f"Error de conexión: {str(e)}" 