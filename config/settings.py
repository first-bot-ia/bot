"""
Configuración del Bot Python - Especializado y Simplificado
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
    phone_number: str
    whatsapp_number: str
    
    @classmethod
    def from_env(cls) -> 'TwilioConfig':
        """Crea configuración desde variables de entorno"""
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        phone_number = os.getenv('TWILIO_PHONE_NUMBER', '+14155238886')
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
            phone_number=phone_number,
            whatsapp_number=whatsapp_number
        )

@dataclass
class WebConfig:
    """Configuración del servidor web"""
    port: int
    host: str
    debug: bool
    api_gateway_url: str
    backend_url: str
    webhook_url: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> 'WebConfig':
        """Crea configuración desde variables de entorno"""
        port = int(os.getenv('PORT', os.getenv('BOT_PORT', '5000')))
        host = os.getenv('HOST', '0.0.0.0')
        debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
        api_gateway_url = os.getenv('API_GATEWAY_URL', 'http://localhost:8080')
        backend_url = os.getenv('BACKEND_URL', 'http://localhost:9000')
        webhook_url = os.getenv('WEBHOOK_URL')
        
        return cls(
            port=port,
            host=host,
            debug=debug,
            api_gateway_url=api_gateway_url,
            backend_url=backend_url,
            webhook_url=webhook_url
        )

@dataclass
class SecurityConfig:
    """Configuración de seguridad"""
    api_gateway_secret: str
    webhook_verify_token: str
    
    @classmethod
    def from_env(cls) -> 'SecurityConfig':
        """Crea configuración desde variables de entorno"""
        api_gateway_secret = os.getenv('API_GATEWAY_SECRET', 'secret-123-gateway')
        webhook_verify_token = os.getenv('WEBHOOK_VERIFY_TOKEN', 'secret-123-gateway')
        
        return cls(
            api_gateway_secret=api_gateway_secret,
            webhook_verify_token=webhook_verify_token
        )

@dataclass
class AppConfig:
    """Configuración principal de la aplicación"""
    database: DatabaseConfig
    twilio: TwilioConfig
    web: WebConfig
    security: SecurityConfig
    
    # Variables adicionales específicas del bot
    cors_origin: str
    cors_credentials: bool
    log_level: str
    debug: bool
    
    @classmethod
    def from_env(cls) -> 'AppConfig':
        """Crea configuración completa desde variables de entorno"""
        cors_origin = os.getenv('CORS_ORIGIN', 'http://localhost:8080')
        cors_credentials = os.getenv('CORS_CREDENTIALS', 'true').lower() == 'true'
        log_level = os.getenv('LOG_LEVEL', 'INFO')
        debug = os.getenv('DEBUG', 'true').lower() == 'true'
        
        return cls(
            database=DatabaseConfig.from_env(),
            twilio=TwilioConfig.from_env(),
            web=WebConfig.from_env(),
            security=SecurityConfig.from_env(),
            cors_origin=cors_origin,
            cors_credentials=cors_credentials,
            log_level=log_level,
            debug=debug
        ) 