"""
Repositorio de Mensajes - Interfaz para persistencia de mensajes
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from ..entities.message import Message, MessageStatus

class MessageRepository(ABC):
    """
    Repositorio abstracto para Mensajes
    Define la interfaz para todas las operaciones de persistencia de mensajes
    """
    
    @abstractmethod
    async def save(self, message: Message) -> Message:
        """
        Guarda un mensaje en el repositorio
        
        Args:
            message: El mensaje a guardar
            
        Returns:
            Message: El mensaje guardado con ID actualizado
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, message_id: int) -> Optional[Message]:
        """
        Busca un mensaje por su ID
        
        Args:
            message_id: ID del mensaje a buscar
            
        Returns:
            Optional[Message]: El mensaje encontrado o None
        """
        pass
    
    @abstractmethod
    async def find_by_campaign(self, campaign_id: int) -> List[Message]:
        """
        Busca todos los mensajes de una campaña específica
        
        Args:
            campaign_id: ID de la campaña
            
        Returns:
            List[Message]: Lista de mensajes de la campaña
        """
        pass
    
    @abstractmethod
    async def find_by_phone(self, phone: str) -> List[Message]:
        """
        Busca mensajes por número de teléfono del cliente
        
        Args:
            phone: Número de teléfono a buscar
            
        Returns:
            List[Message]: Lista de mensajes enviados a ese teléfono
        """
        pass
    
    @abstractmethod
    async def find_by_client_id(self, client_id: int) -> List[Message]:
        """
        Busca mensajes por ID del cliente
        
        Args:
            client_id: ID del cliente
            
        Returns:
            List[Message]: Lista de mensajes del cliente
        """
        pass
    
    @abstractmethod
    async def find_by_status(self, status: MessageStatus) -> List[Message]:
        """
        Busca mensajes por estado
        
        Args:
            status: Estado de los mensajes a buscar
            
        Returns:
            List[Message]: Lista de mensajes con el estado especificado
        """
        pass
    
    @abstractmethod
    async def find_pending_messages(self) -> List[Message]:
        """
        Obtiene todos los mensajes pendientes de envío
        
        Returns:
            List[Message]: Lista de mensajes pendientes
        """
        pass
    
    @abstractmethod
    async def update_status(self, message_id: int, status: MessageStatus, 
                           message_sid: Optional[str] = None, 
                           twilio_response: Optional[str] = None) -> bool:
        """
        Actualiza el estado de un mensaje
        
        Args:
            message_id: ID del mensaje
            status: Nuevo estado
            message_sid: SID del mensaje de Twilio (opcional)
            twilio_response: Respuesta de Twilio (opcional)
            
        Returns:
            bool: True si se actualizó correctamente
        """
        pass
    
    @abstractmethod
    async def get_messages_by_date_range(self, start_date: datetime, 
                                       end_date: datetime) -> List[Message]:
        """
        Obtiene mensajes en un rango de fechas
        
        Args:
            start_date: Fecha de inicio
            end_date: Fecha de fin
            
        Returns:
            List[Message]: Lista de mensajes en el rango
        """
        pass
    
    @abstractmethod
    async def count_by_status(self, status: MessageStatus) -> int:
        """
        Cuenta mensajes por estado
        
        Args:
            status: Estado a contar
            
        Returns:
            int: Número de mensajes con ese estado
        """
        pass
    
    @abstractmethod
    async def get_failed_messages_for_retry(self, max_retries: int = 3) -> List[Message]:
        """
        Obtiene mensajes fallidos que pueden ser reintentados
        
        Args:
            max_retries: Número máximo de reintentos
            
        Returns:
            List[Message]: Lista de mensajes para reintentar
        """
        pass
    
    @abstractmethod
    async def delete(self, message_id: int) -> bool:
        """
        Elimina un mensaje del repositorio
        
        Args:
            message_id: ID del mensaje a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        pass
    
    @abstractmethod
    async def get_all(self, limit: Optional[int] = None, offset: int = 0) -> List[Message]:
        """
        Obtiene todos los mensajes con paginación opcional
        
        Args:
            limit: Límite de resultados
            offset: Desplazamiento para paginación
            
        Returns:
            List[Message]: Lista de mensajes
        """
        pass 