"""
Value Object PhoneNumber - Representa un número de teléfono válido
"""
import re
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class PhoneNumber:
    """
    Value Object PhoneNumber - Representa un número de teléfono válido e inmutable
    """
    value: str
    
    def __post_init__(self):
        """Validaciones después de inicializar"""
        if not self.value or not self.value.strip():
            raise ValueError("El número de teléfono no puede estar vacío")
        
        # Normalizar y validar el número
        normalized = self._normalize(self.value)
        
        if not self._is_valid(normalized):
            raise ValueError(f"Número de teléfono inválido: {self.value}")
        
        # Usar object.__setattr__ porque la clase es frozen
        object.__setattr__(self, 'value', normalized)
    
    def _normalize(self, phone: str) -> str:
        """Normaliza el formato del número de teléfono"""
        # Remover espacios y caracteres especiales
        phone = re.sub(r'[\s\-\(\)]', '', phone.strip())
        
        # Agregar código de país si no existe
        if not phone.startswith('+'):
            if phone.startswith('51'):
                phone = '+' + phone
            elif phone.startswith('9') and len(phone) == 9:
                phone = '+51' + phone
            else:
                # Asumir que es número peruano
                phone = '+51' + phone
        
        return phone
    
    def _is_valid(self, phone: str) -> bool:
        """Valida si el número de teléfono es válido"""
        # Patrón para números peruanos: +51 seguido de 9 dígitos
        # Puede empezar con 9 (celular) o otros códigos de área
        pattern = r'^\+51[0-9]{9}$'
        return bool(re.match(pattern, phone))
    
    def for_whatsapp(self) -> str:
        """Retorna el número formateado para WhatsApp"""
        return f"whatsapp:{self.value}"
    
    def display_format(self) -> str:
        """Retorna el número en formato de visualización"""
        if self.value.startswith('+51'):
            # Formato: +51 999 123 456
            number = self.value[3:]  # Remover +51
            return f"+51 {number[:3]} {number[3:6]} {number[6:]}"
        return self.value
    
    def is_mobile(self) -> bool:
        """Verifica si es un número móvil peruano"""
        return self.value.startswith('+519')
    
    def __str__(self) -> str:
        return self.value 