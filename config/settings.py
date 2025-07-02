"""
Configuración de la aplicación
"""
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class DatabaseConfig:
    """Configuración de base de datos"""
    url: str
    
    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        """Crea configuración desde variables de entorno"""
        url = os.getenv('DATABASE_URL')
        if not url:
            raise ValueError("DATABASE_URL no está configurada")
        return cls(url=url)

@dataclass 
class TwilioConfig:
    """Configuración de Twilio"""
    account_sid: str
    auth_token: str
    whatsapp_number: str
    
    @classmethod
    def from_env(cls) -> 'TwilioConfig':
        """Crea configuración desde variables de entorno"""
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
        
        if not all([account_sid, auth_token, whatsapp_number]):
            raise ValueError("Configuración de Twilio incompleta")
        
        # Type assertion después de validación
        assert account_sid is not None
        assert auth_token is not None
        assert whatsapp_number is not None
            
        return cls(
            account_sid=account_sid,
            auth_token=auth_token,
            whatsapp_number=whatsapp_number
        )

@dataclass
class WebConfig:
    """Configuración del servidor web"""
    port: int
    debug: bool
    api_gateway_url: str  # NUEVO para microservicio
    webhook_url: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> 'WebConfig':
        """Crea configuración desde variables de entorno"""
        port = int(os.getenv('FLASK_PORT', '5000'))
        debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
        api_gateway_url = os.getenv('API_GATEWAY_URL', 'http://localhost:8080')
        webhook_url = os.getenv('WEBHOOK_URL')
        
        return cls(
            port=port,
            debug=debug,
            api_gateway_url=api_gateway_url,
            webhook_url=webhook_url
        )

@dataclass
class AppConfig:
    """Configuración principal de la aplicación"""
    database: DatabaseConfig
    twilio: TwilioConfig
    web: WebConfig
    
    @classmethod
    def from_env(cls) -> 'AppConfig':
        """Crea configuración completa desde variables de entorno"""
        return cls(
            database=DatabaseConfig.from_env(),
            twilio=TwilioConfig.from_env(),
            web=WebConfig.from_env()
        ) 