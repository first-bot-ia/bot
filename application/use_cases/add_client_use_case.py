"""
Caso de uso: Agregar Cliente
"""
from typing import Dict, Any

from domain.entities.client import Client
from domain.repositories.client_repository import ClientRepository
from domain.value_objects.phone_number import PhoneNumber


class AddClientUseCase:
    """
    Caso de uso para agregar un nuevo cliente al sistema
    """
    
    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository
    
    def execute(self, nombre: str, telefono: str, email: str | None = None) -> Dict[str, Any]:
        """
        Ejecuta el caso de uso de agregar cliente
        
        Args:
            nombre: Nombre del cliente
            telefono: Número de teléfono  
            email: Email del cliente (opcional)
            
        Returns:
            Dict con resultado de la operación
        """
        try:
            # Validar número de teléfono usando Value Object
            phone_number = PhoneNumber(telefono)
            
            # Verificar si el cliente ya existe
            existing_client = self.client_repository.find_by_phone(phone_number.value)
            if existing_client:
                return {
                    'success': False,
                    'message': f'Cliente con teléfono {phone_number.display_format()} ya existe',
                    'client_id': existing_client.id
                }
            
            # Crear nueva entidad Cliente
            new_client = Client(
                id=None,
                nombre=nombre.strip(),
                telefono=phone_number.value,
                email=email.strip() if email is not None else None
            )
            
            # Guardar en repositorio
            saved_client = self.client_repository.save(new_client)
            
            return {
                'success': True,
                'message': f'Cliente {saved_client.nombre} agregado exitosamente',
                'client_id': saved_client.id,
                'client': {
                    'id': saved_client.id,
                    'nombre': saved_client.nombre,
                    'telefono': saved_client.telefono,
                    'telefono_display': phone_number.display_format(),
                    'email': saved_client.email,
                    'activo': saved_client.activo,
                    'fecha_registro': saved_client.fecha_registro.isoformat() if saved_client.fecha_registro else None
                }
            }
            
        except ValueError as e:
            return {
                'success': False,
                'message': f'Error de validación: {str(e)}',
                'client_id': None
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error interno: {str(e)}',
                'client_id': None
            } 