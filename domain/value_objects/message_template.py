"""
Value Object MessageTemplate - Representa un template de mensaje
"""
from dataclasses import dataclass
from typing import List, Dict, Any
import re

@dataclass(frozen=True)
class MessageTemplate:
    """
    Value Object MessageTemplate - Representa un template de mensaje inmutable
    """
    key: str
    name: str
    description: str
    parameters_count: int
    example: str
    
    def __post_init__(self):
        """Validaciones después de inicializar"""
        if not self.key or not self.key.strip():
            raise ValueError("La clave del template no puede estar vacía")
        
        if not self.name or not self.name.strip():
            raise ValueError("El nombre del template no puede estar vacío")
        
        if not self.description or not self.description.strip():
            raise ValueError("La descripción del template no puede estar vacía")
        
        if self.parameters_count < 0:
            raise ValueError("El número de parámetros no puede ser negativo")
        
        # Validar que la descripción tenga los placeholders correctos
        placeholders = re.findall(r'\{\{(\d+)\}\}', self.description)
        expected_placeholders = set(str(i) for i in range(1, self.parameters_count + 1))
        actual_placeholders = set(placeholders)
        
        if actual_placeholders != expected_placeholders:
            raise ValueError(f"Los placeholders del template no coinciden. Esperados: {expected_placeholders}, Encontrados: {actual_placeholders}")
    
    def format_message(self, parameters: List[str]) -> str:
        """Formatea el mensaje con los parámetros proporcionados"""
        if len(parameters) != self.parameters_count:
            raise ValueError(f"Se esperaban {self.parameters_count} parámetros, se recibieron {len(parameters)}")
        
        message = self.description
        
        # Reemplazar placeholders {{1}}, {{2}}, etc.
        for i, param in enumerate(parameters, 1):
            placeholder = f"{{{{{i}}}}}"
            message = message.replace(placeholder, str(param))
        
        return message
    
    def get_placeholder_names(self) -> List[str]:
        """Obtiene los nombres de los placeholders en orden"""
        return [f"{{{{{{i}}}}}}" for i in range(1, self.parameters_count + 1)]
    
    def validate_parameters(self, parameters: List[str]) -> bool:
        """Valida que los parámetros sean válidos para este template"""
        if len(parameters) != self.parameters_count:
            return False
        
        # Validar que ningún parámetro esté vacío
        return all(param and param.strip() for param in parameters)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el template a diccionario"""
        return {
            'key': self.key,
            'name': self.name,
            'description': self.description,
            'parameters_count': self.parameters_count,
            'example': self.example
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MessageTemplate':
        """Crea un template desde un diccionario"""
        return cls(
            key=data['key'],
            name=data['name'],
            description=data['description'],
            parameters_count=data['parameters_count'],
            example=data['example']
        )
    
    def __str__(self) -> str:
        return f"MessageTemplate(key='{self.key}', name='{self.name}')" 