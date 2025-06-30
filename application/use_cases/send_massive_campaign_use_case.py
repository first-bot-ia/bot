"""
Caso de uso: Envío Masivo de Campaña
"""
from typing import Dict, Any, List

from domain.repositories.client_repository import ClientRepository
from infrastructure.external_services.twilio_service import TwilioWhatsAppService


class SendMassiveCampaignUseCase:
    """
    Caso de uso para envío masivo de mensajes a clientes activos
    """
    
    def __init__(self, client_repository: ClientRepository, twilio_service: TwilioWhatsAppService):
        self.client_repository = client_repository
        self.twilio_service = twilio_service
    
    def execute(self, template_key: str, delay_seconds: int = 3) -> Dict[str, Any]:
        """
        Ejecuta el envío masivo de campaña
        
        Args:
            template_key: Clave del template a usar
            delay_seconds: Segundos de delay entre envíos
            
        Returns:
            Dict con resultado de la operación
        """
        try:
            # Validar que el template existe
            try:
                template = self.twilio_service.get_template(template_key)
            except ValueError as e:
                return {
                    'success': False,
                    'message': str(e),
                    'stats': None
                }
            
            # Obtener clientes activos
            active_clients = self.client_repository.find_all_active()
            
            if not active_clients:
                return {
                    'success': False,
                    'message': 'No hay clientes activos para enviar mensajes',
                    'stats': {'total_clientes': 0, 'enviados': 0, 'fallidos': 0}
                }
            
            print(f"🚀 Iniciando campaña masiva: {template.name}")
            print(f"📱 Template: {template_key}")
            print(f"👥 Total clientes: {len(active_clients)}")
            print(f"⏱️ Delay entre mensajes: {delay_seconds} segundos")
            print("=" * 50)
            
            # Enviar mensajes masivos
            stats = self.twilio_service.send_bulk_messages(
                clients=active_clients,
                template_key=template_key,
                delay_seconds=delay_seconds
            )
            
            # Actualizar contadores de envío para clientes exitosos
            if stats['enviados'] > 0:
                self._update_client_send_counts(active_clients[:stats['enviados']])
            
            print("=" * 50)
            print(f"🏁 Campaña completada:")
            print(f"✅ Enviados: {stats['enviados']}")
            print(f"❌ Fallidos: {stats['fallidos']}")
            print(f"📊 Tasa de éxito: {(stats['enviados']/len(active_clients)*100):.1f}%")
            
            return {
                'success': True,
                'message': f'Campaña completada: {stats["enviados"]} enviados, {stats["fallidos"]} fallidos',
                'stats': {
                    'total_clientes': len(active_clients),
                    'enviados': stats['enviados'],
                    'fallidos': stats['fallidos'],
                    'tasa_exito': round((stats['enviados']/len(active_clients)*100), 1),
                    'template_usado': template_key,
                    'template_nombre': template.name
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error ejecutando campaña: {str(e)}',
                'stats': None
            }
    
    def _update_client_send_counts(self, successful_clients: List):
        """Actualiza contadores de envío para clientes exitosos"""
        try:
            for client in successful_clients:
                client.registrar_envio()
                self.client_repository.update(client)
        except Exception as e:
            print(f"⚠️ Error actualizando contadores de clientes: {e}")
    
    def get_available_templates(self) -> List[Dict[str, Any]]:
        """Obtiene lista de templates disponibles"""
        templates = self.twilio_service.get_available_templates()
        
        return [
            {
                'key': template.key,
                'name': template.name,
                'description': template.description,
                'parameters_count': template.parameters_count,
                'example': template.example
            }
            for template in templates
        ] 