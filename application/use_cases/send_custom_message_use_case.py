"""
Caso de uso: Envío de Mensaje Personalizado Masivo
"""
from typing import Dict, Any, List, Union
import os
from werkzeug.datastructures import FileStorage

from domain.repositories.client_repository import ClientRepository
from infrastructure.external_services.twilio_service import TwilioWhatsAppService


class SendCustomMessageUseCase:
    """
    Caso de uso para envío masivo de mensajes personalizados con archivos
    """
    
    def __init__(self, client_repository: ClientRepository, twilio_service: TwilioWhatsAppService):
        self.client_repository = client_repository
        self.twilio_service = twilio_service
    
    def execute(self, custom_message: str, media_files: Union[List[FileStorage], None] = None, 
                delay_seconds: int = 3) -> Dict[str, Any]:
        """
        Ejecuta el envío masivo de mensaje personalizado
        
        Args:
            custom_message: Mensaje personalizado del usuario
            media_files: Lista de archivos de imagen/documento (opcional)
            delay_seconds: Segundos de delay entre envíos
            
        Returns:
            Dict con resultado de la operación
        """
        try:
            # Validar mensaje
            if not custom_message or not custom_message.strip():
                return {
                    'success': False,
                    'message': 'El mensaje personalizado no puede estar vacío',
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
            
            # Procesar archivos multimedia si existen
            media_urls = []
            if media_files:
                for media_file in media_files:
                    if media_file and media_file.filename:
                        media_url = self._save_media_file(media_file)
                        if media_url:
                            media_urls.append(media_url)
                        else:
                            return {
                                'success': False,
                                'message': f'Error al procesar el archivo {media_file.filename}',
                                'stats': None
                            }
            
            print(f"🚀 Iniciando campaña personalizada masiva")
            print(f"💬 Mensaje: {custom_message[:50]}...")
            print(f"📎 Archivos: {len(media_urls)} archivo(s)")
            print(f"👥 Total clientes: {len(active_clients)}")
            print(f"⏱️ Delay entre mensajes: {delay_seconds} segundos")
            print("=" * 50)
            
            # Enviar mensajes personalizados masivos (usar primera URL por ahora)
            first_media_url = media_urls[0] if media_urls else None
            stats = self.twilio_service.send_custom_bulk_messages(
                clients=active_clients,
                message=custom_message.strip(),
                media_url=first_media_url,
                delay_seconds=delay_seconds
            )
            
            # Actualizar contadores de envío para clientes exitosos
            if stats['enviados'] > 0:
                self._update_client_send_counts(active_clients[:stats['enviados']])
            
            print("=" * 50)
            print(f"🏁 Campaña personalizada completada:")
            print(f"✅ Enviados: {stats['enviados']}")
            print(f"❌ Fallidos: {stats['fallidos']}")
            print(f"📊 Tasa de éxito: {(stats['enviados']/len(active_clients)*100):.1f}%")
            
            return {
                'success': True,
                'message': f'Campaña personalizada completada: {stats["enviados"]} enviados, {stats["fallidos"]} fallidos',
                'stats': {
                    'total_clientes': len(active_clients),
                    'enviados': stats['enviados'],
                    'fallidos': stats['fallidos'],
                    'tasa_exito': round((stats['enviados']/len(active_clients)*100), 1),
                    'mensaje_personalizado': True,
                    'con_archivos': len(media_urls) > 0
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error ejecutando campaña personalizada: {str(e)}',
                'stats': None
            }
    
    def _save_media_file(self, media_file: FileStorage) -> Union[str, None]:
        """
        Guarda el archivo multimedia y retorna la URL
        
        Args:
            media_file: Archivo subido
            
        Returns:
            URL del archivo guardado o None si hay error
        """
        try:
            # Crear directorio de uploads si no existe
            upload_dir = "uploads"
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            # Generar nombre único para el archivo
            import uuid
            from datetime import datetime
            
            if not media_file.filename:
                return None
                
            file_extension = os.path.splitext(media_file.filename)[1]
            unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}{file_extension}"
            file_path = os.path.join(upload_dir, unique_filename)
            
            # Guardar archivo
            media_file.save(file_path)
            
            # Retornar URL completa (en producción sería una URL pública)
            return f"http://localhost:5000/uploads/{unique_filename}"
            
        except Exception as e:
            print(f"Error guardando archivo multimedia: {e}")
            return None
    
    def _update_client_send_counts(self, successful_clients: List):
        """Actualiza contadores de envío para clientes exitosos"""
        try:
            for client in successful_clients:
                client.registrar_envio()
                self.client_repository.update(client)
        except Exception as e:
            print(f"⚠️ Error actualizando contadores de clientes: {e}")
    
    def get_supported_file_types(self) -> List[str]:
        """Retorna tipos de archivo soportados"""
        return [
            '.jpg', '.jpeg', '.png', '.gif',  # Imágenes
            '.pdf', '.doc', '.docx',          # Documentos
            '.mp4', '.avi', '.mov',           # Videos
            '.mp3', '.wav', '.ogg'            # Audio
        ]
    
    def validate_file_type(self, filename: str) -> bool:
        """Valida si el tipo de archivo es soportado"""
        if not filename:
            return False
        
        file_extension = os.path.splitext(filename)[1].lower()
        return file_extension in self.get_supported_file_types()
    
    def get_max_file_size_mb(self) -> int:
        """Retorna el tamaño máximo de archivo en MB"""
        return 16  # 16MB límite de Twilio para WhatsApp 