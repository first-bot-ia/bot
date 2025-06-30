"""
Entidad Campaña - Representa una campaña de envío masivo
"""
from datetime import datetime
from typing import Optional
from dataclasses import dataclass
from enum import Enum

class CampaignStatus(Enum):
    """Estados posibles de una campaña"""
    PENDING = "pendiente"
    IN_PROGRESS = "en_progreso"
    COMPLETED = "completada"
    FAILED = "fallida"
    CANCELLED = "cancelada"

@dataclass
class Campaign:
    """
    Entidad Campaña - Representa una campaña de envío masivo de mensajes
    """
    id: Optional[int]
    name: str
    template_key: str
    description: Optional[str]
    status: CampaignStatus
    created_at: Optional[datetime] = None
    executed_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    total_messages: int = 0
    successful_messages: int = 0
    failed_messages: int = 0
    
    def __post_init__(self):
        """Validaciones después de inicializar"""
        if not self.name or not self.name.strip():
            raise ValueError("El nombre de la campaña no puede estar vacío")
        
        if not self.template_key or not self.template_key.strip():
            raise ValueError("La clave del template no puede estar vacía")
        
        if self.created_at is None:
            self.created_at = datetime.now()
        
        # Validar que los contadores sean consistentes
        if self.successful_messages + self.failed_messages > self.total_messages:
            raise ValueError("Los mensajes exitosos + fallidos no pueden superar el total")
    
    def start_execution(self, total_messages: int):
        """Inicia la ejecución de la campaña"""
        if self.status != CampaignStatus.PENDING:
            raise ValueError("Solo se pueden ejecutar campañas pendientes")
        
        self.status = CampaignStatus.IN_PROGRESS
        self.executed_at = datetime.now()
        self.total_messages = total_messages
        self.successful_messages = 0
        self.failed_messages = 0
    
    def record_successful_message(self):
        """Registra un mensaje enviado exitosamente"""
        if self.status != CampaignStatus.IN_PROGRESS:
            raise ValueError("Solo se pueden registrar mensajes en campañas en progreso")
        
        self.successful_messages += 1
        self._check_completion()
    
    def record_failed_message(self):
        """Registra un mensaje fallido"""
        if self.status != CampaignStatus.IN_PROGRESS:
            raise ValueError("Solo se pueden registrar mensajes en campañas en progreso")
        
        self.failed_messages += 1
        self._check_completion()
    
    def _check_completion(self):
        """Verifica si la campaña está completa"""
        if self.successful_messages + self.failed_messages >= self.total_messages:
            self.complete()
    
    def complete(self):
        """Marca la campaña como completada"""
        if self.status == CampaignStatus.IN_PROGRESS:
            self.status = CampaignStatus.COMPLETED
            self.completed_at = datetime.now()
    
    def cancel(self):
        """Cancela la campaña"""
        if self.status in [CampaignStatus.PENDING, CampaignStatus.IN_PROGRESS]:
            self.status = CampaignStatus.CANCELLED
            self.completed_at = datetime.now()
    
    def mark_as_failed(self):
        """Marca la campaña como fallida"""
        self.status = CampaignStatus.FAILED
        self.completed_at = datetime.now()
    
    def is_active(self) -> bool:
        """Verifica si la campaña está activa (en progreso)"""
        return self.status == CampaignStatus.IN_PROGRESS
    
    def is_completed(self) -> bool:
        """Verifica si la campaña está completada"""
        return self.status == CampaignStatus.COMPLETED
    
    def get_success_rate(self) -> float:
        """Calcula la tasa de éxito de la campaña"""
        if self.total_messages == 0:
            return 0.0
        return (self.successful_messages / self.total_messages) * 100
    
    def get_duration_minutes(self) -> Optional[float]:
        """Calcula la duración de la campaña en minutos"""
        if not self.executed_at:
            return None
        
        end_time = self.completed_at or datetime.now()
        duration = end_time - self.executed_at
        return duration.total_seconds() / 60 