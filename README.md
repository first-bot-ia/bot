# 🤖 WhatsApp Microservice - Alesse Connect

## 📋 Descripción

Microservicio especializado en operaciones de WhatsApp/Twilio, diseñado para funcionar como parte de una arquitectura de microservicios más amplia. Este servicio actúa como un "driver" o "adapter" especializado que únicamente se encarga de traducir requests del API Gateway a llamadas optimizadas de Twilio API.

## 🏗️ Arquitectura de Microservicio

```
API Gateway (8080) → WhatsApp Microservice (5000) → Twilio API
```

### 🎯 Especializaciones

- **Envío directo via Twilio**: Operaciones optimizadas de WhatsApp Business
- **Webhook adapter**: Normalización de eventos de Twilio para API Gateway
- **Campañas masivas**: Ejecución masiva con rate limiting
- **Health checks**: Monitoreo especializado de conectividad Twilio

## 🚀 Endpoints Especializados

### Health Check
- `GET /health` - Estado del microservicio y conectividad Twilio

### Webhook Processing
- `POST /whatsapp/webhook` - Adapter que normaliza y reenvía al API Gateway

### Message Operations
- `POST /send/message` - Envío directo de mensaje individual
- `POST /execute/campaign` - Ejecución de campaña masiva (recibe datos procesados)

## 📦 Instalación

```bash
# Instalar dependencias especializadas
pip install -r requirements.txt

# Configurar variables de entorno
cp .environment.example .environment
# Editar .environment con tus credenciales

# Ejecutar microservicio
python main.py
```

## ⚙️ Variables de Entorno

```bash
# Requeridas
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token  
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
API_GATEWAY_URL=http://localhost:8080

# Base de datos (configuración específica)
DATABASE_URL=postgresql://postgres:root@localhost:5432/alesse_connect

# Opcionales
FLASK_PORT=5000
```

## 🗄️ Configuración de Base de Datos

El microservicio está configurado para usar PostgreSQL con esta configuración específica:

- **Base de datos:** `alesse_connect`
- **Host:** `localhost`  
- **Puerto:** `5432`
- **Usuario:** `postgres`
- **Password:** `root`

### Configurar PostgreSQL:

1. **Abrir pgAdmin y conectar al servidor PostgreSQL**
2. **Crear la base de datos:**
   ```sql
   CREATE DATABASE alesse_connect;
   ```
3. **Verificar conexión:**
   ```bash
   python scripts/verify-database.py
   ```

## 🔄 Integración con API Gateway

Este microservicio está diseñado para recibir comandos del API Gateway y devolver solo resultados de ejecución:

### Flujo de Campaña
1. **API Gateway** procesa business logic y envía a `/execute/campaign`
2. **Microservicio** ejecuta envíos via Twilio
3. **Retorna** estadísticas de ejecución al Gateway

### Flujo de Webhook
1. **Twilio** envía webhook a `/whatsapp/webhook`
2. **Microservicio** normaliza datos
3. **Reenvía** al API Gateway para procesamiento

## 📊 Beneficios de la Arquitectura

- **70% menos código** (de 744 a ~200 líneas)
- **Zero business logic** - Solo operaciones Twilio
- **Zero UI components** - Interfaz en Frontend React
- **Mejor performance** - Especialización pura
- **Fácil escalabilidad** - Microservicio independiente

## 🧪 Testing

```bash
# Test de conectividad
curl http://localhost:5000/health

# Test de envío directo
curl -X POST http://localhost:5000/send/message \
  -H "Content-Type: application/json" \
  -d '{"phone": "+51999123456", "message": "Test message"}'
```

## 🔧 Desarrollo

Este microservicio sigue el principio de **Single Responsibility** y está optimizado para:

- Operaciones de Twilio API únicamente
- Comunicación con API Gateway
- Procesamiento mínimo de datos
- Máxima especialización en WhatsApp

## 📝 Notas

- Microservicio siempre corre en modo producción
- CORS manejado por API Gateway
- Business logic procesada por Backend Node.js
- UI servida por Frontend React 