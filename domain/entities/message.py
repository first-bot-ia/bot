"""
Entidad Mensaje - Representa un mensaje enviado en el sistema
"""
from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass
from enum import Enum

class MessageStatus(Enum):
    """Estados posibles de un mensaje"""
    PENDING = "pendiente"
    SENT = "enviado"
    FAILED = "fallido"
    DELIVERED = "entregado"

@dataclass
class Message:
    """
    Entidad Mensaje - Representa un mensaje enviado a un cliente
    """
    id: Optional[int]
    client_id: int
    template_key: str
    content: str
    parameters: List[str]
    status: MessageStatus
    sent_at: Optional[datetime] = None
    twilio_response: Optional[str] = None
    message_sid: Optional[str] = None
    
    def __post_init__(self):
        """Validaciones después de inicializar"""
        if not self.content or not self.content.strip():
            raise ValueError("El contenido del mensaje no puede estar vacío")
        
        if not self.template_key or not self.template_key.strip():
            raise ValueError("La clave del template no puede estar vacía")
        
        if self.client_id <= 0:
            raise ValueError("El ID del cliente debe ser válido")
        
        if self.sent_at is None and self.status == MessageStatus.SENT:
            self.sent_at = datetime.now()
    
    def mark_as_sent(self, message_sid: str, twilio_response: str):
        """Marca el mensaje como enviado exitosamente"""
        self.status = MessageStatus.SENT
        self.sent_at = datetime.now()
        self.message_sid = message_sid
        self.twilio_response = twilio_response
    
    def mark_as_failed(self, error_message: str):
        """Marca el mensaje como fallido"""
        self.status = MessageStatus.FAILED
        self.twilio_response = error_message
    
    def mark_as_delivered(self):
        """Marca el mensaje como entregado"""
        if self.status == MessageStatus.SENT:
            self.status = MessageStatus.DELIVERED
    
    def is_sent(self) -> bool:
        """Verifica si el mensaje fue enviado exitosamente"""
        return self.status == MessageStatus.SENT
    
    def is_failed(self) -> bool:
        """Verifica si el mensaje falló al enviarse"""
        return self.status == MessageStatus.FAILED
    
    def get_parameters_string(self) -> str:
        """Obtiene los parámetros como string para persistencia"""
        return str(self.parameters) if self.parameters else "[]" 