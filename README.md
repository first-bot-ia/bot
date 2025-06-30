# 🤖 Bot de Spam WhatsApp - Alesse Connect

Sistema de envío masivo de mensajes de WhatsApp implementado con **Domain-Driven Design (DDD)** y arquitectura limpia.

## 🏗️ Arquitectura DDD

```
bot/
├── domain/                     # 🏛️ Capa de Dominio
│   ├── entities/              # Entidades con identidad
│   │   ├── client.py          # Cliente
│   │   ├── message.py         # Mensaje  
│   │   └── campaign.py        # Campaña
│   ├── value_objects/         # Objetos de valor inmutables
│   │   ├── phone_number.py    # Número de teléfono
│   │   └── message_template.py # Template de mensaje
│   ├── repositories/          # Interfaces de repositorios
│   │   ├── client_repository.py
│   │   ├── message_repository.py
│   │   └── campaign_repository.py
│   └── services/              # Servicios de dominio
│
├── infrastructure/            # 🔧 Capa de Infraestructura
│   ├── persistence/           # Implementaciones de persistencia
│   │   ├── postgresql_client_repository.py
│   │   ├── postgresql_message_repository.py
│   │   └── postgresql_campaign_repository.py
│   ├── external_services/     # Servicios externos
│   │   ├── twilio_service.py
│   │   └── ngrok_service.py
│   └── web/                   # Controladores web
│       ├── web_interface.py
│       └── webhook_controller.py
│
├── application/               # 🎯 Capa de Aplicación  
│   ├── use_cases/            # Casos de uso
│   │   ├── send_massive_campaign_use_case.py
│   │   ├── add_client_use_case.py
│   │   └── get_campaign_stats_use_case.py
│   └── dto/                  # Data Transfer Objects
│       ├── client_dto.py
│       └── campaign_dto.py
│
├── config/                   # ⚙️ Configuración
│   └── settings.py
│
├── main.py                   # 🚀 Punto de entrada principal
├── requirements.txt          # 📦 Dependencias
└── .environment             # 🔐 Variables de entorno
```

## ✨ Características

- 🎯 **Domain-Driven Design**: Arquitectura limpia y mantenible
- 📱 **WhatsApp Business**: Integración con Twilio Sandbox
- 🗄️ **PostgreSQL**: Base de datos robusta
- 🌐 **Web Interface**: Panel de control con Flask
- 📊 **Analytics**: Estadísticas de campañas en tiempo real
- 🔄 **Templates**: Sistema de plantillas personalizables
- 🚀 **Escalable**: Diseño modular y extensible

## 🚀 Inicio Rápido

### 1. Instalación

```bash
# Clonar repositorio
git clone <repo-url>
cd alesse-connect/bot

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configuración

Edita el archivo `.environment`:

```env
# Credenciales Twilio
TWILIO_ACCOUNT_SID=tu_account_sid
TWILIO_AUTH_TOKEN=tu_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Base de datos PostgreSQL
DATABASE_URL=postgresql://usuario:password@localhost:5432/base_datos

# Servidor web
FLASK_PORT=5000
FLASK_DEBUG=True
WEBHOOK_URL=http://localhost:5000/whatsapp/webhook
```

### 3. Configurar WhatsApp Sandbox

1. Ve a [Twilio Console](https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn)
2. Únete al sandbox enviando `join` a **+1 415 523 8886**
3. Configura la URL del webhook

### 4. Ejecutar

```bash
# Opción 1: Nuevo sistema DDD (recomendado)
python main.py

# Opción 2: Sistema existente (funcional)
python run_spam_bot.py
```

### 5. Iniciar ngrok

En otra terminal:

```bash
./ngrok.exe http 5000
```

Copia la URL HTTPS de ngrok al webhook de Twilio.

## 🎯 Casos de Uso

### ✅ Funcionalidades Implementadas

1. **Gestión de Clientes**
   - ✅ Agregar cliente
   - ✅ Listar clientes activos
   - ✅ Validación de números de teléfono

2. **Envío de Mensajes**
   - ✅ Templates personalizables
   - ✅ Envío masivo con delay
   - ✅ Registro de estados

3. **Campañas**
   - ✅ Crear campaña
   - ✅ Ejecutar envío masivo
   - ✅ Estadísticas en tiempo real

4. **Interfaz Web**
   - ✅ Panel de control
   - ✅ API REST
   - ✅ Webhook para respuestas

### 🔄 Templates Disponibles

| Template | Descripción | Parámetros |
|----------|-------------|------------|
| `soat_renovacion` | Renovación de SOAT | Nombre, Fecha vencimiento, Descuento %, Teléfono |
| `seguro_vehicular_promo` | Promoción seguro vehicular | Nombre, Tipo seguro, Descuento %, Precio |
| `promocion_masiva` | Oferta masiva general | Nombre, Producto, Descuento %, Vehículo, Precio |
| `recordatorio_poliza` | Recordatorio de vencimiento | Nombre, Tipo póliza, Días restantes, Fecha límite |

## 📊 API Endpoints

### Clientes
- `GET /api/clients` - Listar clientes
- `POST /api/clients` - Agregar cliente
- `GET /api/clients/{id}` - Obtener cliente

### Campañas
- `GET /api/campaigns` - Listar campañas
- `POST /api/campaigns` - Crear campaña
- `POST /api/campaigns/{id}/start` - Iniciar campaña

### Templates
- `GET /api/templates` - Listar templates
- `GET /api/templates/{key}` - Obtener template

## 🛠️ Desarrollo

### Principios DDD Aplicados

1. **Entidades**: Cliente, Mensaje, Campaña
2. **Value Objects**: PhoneNumber, MessageTemplate
3. **Repositorios**: Interfaces para persistencia
4. **Servicios de Dominio**: Lógica de negocio compleja
5. **Casos de Uso**: Orquestación de flujos de negocio

### Patrón de Capas

- **Dominio**: Lógica de negocio pura
- **Aplicación**: Casos de uso y DTOs  
- **Infraestructura**: Implementaciones concretas
- **Config**: Configuración centralizada

## 🔧 Troubleshooting

### Problemas Comunes

1. **Error de encoding UTF-8**
   - Problema: Caracteres especiales en rutas de Windows
   - Solución: Usar la interfaz web en lugar de línea de comandos

2. **ngrok ERROR 108**
   - Problema: Múltiples sesiones activas
   - Solución: `taskkill /f /im ngrok.exe`

3. **Mensajes no llegan**
   - Verificar que el número esté en el sandbox de Twilio
   - Enviar `join` al +1 415 523 8886

## 📈 Métricas y Monitoreo

- ✅ Tasa de entrega de mensajes
- ✅ Tiempo de respuesta de API
- ✅ Estadísticas por campaña
- ✅ Logs estructurados

## 🛡️ Seguridad

- ✅ Validación de números de teléfono
- ✅ Rate limiting en envíos
- ✅ Logging de actividades
- ✅ Variables de entorno para credenciales

---

## 📞 Soporte

Para soporte técnico o consultas:
- 📧 Email: soporte@aleseconnect.com
- 📱 WhatsApp: +51 999 888 777

**Desarrollado con ❤️ por el equipo de Alesse Connect** 