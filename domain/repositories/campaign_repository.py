"""
Repositorio de Campañas - Interfaz para persistencia de campañas
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.campaign import Campaign, CampaignStatus

class CampaignRepository(ABC):
    """
    Repositorio abstracto para Campañas
    Define la interfaz para todas las operaciones de persistencia de campañas
    """
    
    @abstractmethod
    async def save(self, campaign: Campaign) -> Campaign:
        """
        Guarda una campaña en el repositorio
        
        Args:
            campaign: La campaña a guardar
            
        Returns:
            Campaign: La campaña guardada con ID actualizado
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, campaign_id: int) -> Optional[Campaign]:
        """
        Busca una campaña por su ID
        
        Args:
            campaign_id: ID de la campaña a buscar
            
        Returns:
            Optional[Campaign]: La campaña encontrada o None
        """
        pass
    
    @abstractmethod
    async def find_active(self) -> List[Campaign]:
        """
        Obtiene todas las campañas activas (en progreso)
        
        Returns:
            List[Campaign]: Lista de campañas activas
        """
        pass
    
    @abstractmethod
    async def find_by_status(self, status: CampaignStatus) -> List[Campaign]:
        """
        Busca campañas por estado
        
        Args:
            status: Estado de las campañas a buscar
            
        Returns:
            List[Campaign]: Lista de campañas con el estado especificado
        """
        pass
    
    @abstractmethod
    async def update_status(self, campaign_id: int, status: CampaignStatus) -> bool:
        """
        Actualiza el estado de una campaña
        
        Args:
            campaign_id: ID de la campaña
            status: Nuevo estado
            
        Returns:
            bool: True si se actualizó correctamente
        """
        pass
    
    @abstractmethod
    async def update_counters(self, campaign_id: int, successful: int, failed: int) -> bool:
        """
        Actualiza los contadores de mensajes de una campaña
        
        Args:
            campaign_id: ID de la campaña
            successful: Número de mensajes exitosos
            failed: Número de mensajes fallidos
            
        Returns:
            bool: True si se actualizó correctamente
        """
        pass
    
    @abstractmethod
    async def get_all(self, limit: Optional[int] = None, offset: int = 0) -> List[Campaign]:
        """
        Obtiene todas las campañas con paginación opcional
        
        Args:
            limit: Límite de resultados
            offset: Desplazamiento para paginación
            
        Returns:
            List[Campaign]: Lista de campañas
        """
        pass
    
    @abstractmethod
    async def delete(self, campaign_id: int) -> bool:
        """
        Elimina una campaña del repositorio
        
        Args:
            campaign_id: ID de la campaña a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        pass 