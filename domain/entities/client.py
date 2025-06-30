"""
Entidad Cliente - Representa un cliente en el sistema de spam bot
"""
from datetime import datetime
from typing import Optional
from dataclasses import dataclass

@dataclass
class Client:
    """
    Entidad Cliente - Representa un cliente que puede recibir mensajes de WhatsApp
    """
    id: Optional[int]
    nombre: str
    telefono: str
    email: Optional[str]
    activo: bool = True
    fecha_registro: Optional[datetime] = None
    ultimo_envio: Optional[datetime] = None
    total_enviados: int = 0
    
    def __post_init__(self):
        """Validaciones después de inicializar"""
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del cliente no puede estar vacío")
        
        if not self.telefono or not self.telefono.strip():
            raise ValueError("El teléfono del cliente no puede estar vacío")
        
        # Normalizar teléfono
        self.telefono = self._normalize_phone(self.telefono)
        
        if self.fecha_registro is None:
            self.fecha_registro = datetime.now()
    
    def _normalize_phone(self, phone: str) -> str:
        """Normaliza el formato del teléfono"""
        phone = phone.strip()
        
        # Si no empieza con +, agregarlo asumiendo código de país Perú
        if not phone.startswith('+'):
            if phone.startswith('51'):
                phone = '+' + phone
            elif phone.startswith('9'):
                phone = '+51' + phone
            else:
                phone = '+51' + phone
                
        return phone
    
    def desactivar(self):
        """Desactiva el cliente para que no reciba más mensajes"""
        self.activo = False
    
    def activar(self):
        """Activa el cliente para que pueda recibir mensajes"""
        self.activo = True
    
    def registrar_envio(self):
        """Registra un envío exitoso al cliente"""
        self.ultimo_envio = datetime.now()
        self.total_enviados += 1
    
    def puede_recibir_mensajes(self) -> bool:
        """Verifica si el cliente puede recibir mensajes"""
        return self.activo
    
    def get_whatsapp_number(self) -> str:
        """Obtiene el número formateado para WhatsApp"""
        return f"whatsapp:{self.telefono}" 