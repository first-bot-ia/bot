"""
Interfaz ClientRepository - Define el contrato para persistencia de clientes
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.client import Client

class ClientRepository(ABC):
    """
    Interfaz ClientRepository - Define operaciones de persistencia para clientes
    """
    
    @abstractmethod
    def save(self, client: Client) -> Client:
        """
        Guarda un cliente en la persistencia
        
        Args:
            client: Cliente a guardar
            
        Returns:
            Cliente guardado con ID asignado
            
        Raises:
            ValueError: Si el cliente ya existe (por teléfono)
        """
        pass
    
    @abstractmethod
    def find_by_id(self, client_id: int) -> Optional[Client]:
        """
        Busca un cliente por su ID
        
        Args:
            client_id: ID del cliente
            
        Returns:
            Cliente si existe, None si no
        """
        pass
    
    @abstractmethod
    def find_by_phone(self, phone: str) -> Optional[Client]:
        """
        Busca un cliente por su número de teléfono
        
        Args:
            phone: Número de teléfono
            
        Returns:
            Cliente si existe, None si no
        """
        pass
    
    @abstractmethod
    def find_all_active(self) -> List[Client]:
        """
        Obtiene todos los clientes activos
        
        Returns:
            Lista de clientes activos
        """
        pass
    
    @abstractmethod
    def find_all(self) -> List[Client]:
        """
        Obtiene todos los clientes
        
        Returns:
            Lista de todos los clientes
        """
        pass
    
    @abstractmethod
    def update(self, client: Client) -> Client:
        """
        Actualiza un cliente existente
        
        Args:
            client: Cliente a actualizar
            
        Returns:
            Cliente actualizado
            
        Raises:
            ValueError: Si el cliente no existe
        """
        pass
    
    @abstractmethod
    def delete(self, client_id: int) -> bool:
        """
        Elimina un cliente
        
        Args:
            client_id: ID del cliente a eliminar
            
        Returns:
            True si se eliminó, False si no existía
        """
        pass
    
    @abstractmethod
    def count_active(self) -> int:
        """
        Cuenta los clientes activos
        
        Returns:
            Número de clientes activos
        """
        pass 