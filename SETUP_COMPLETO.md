# 🤖 Bot WhatsApp - Configuración Completa

## **FLUJO IMPLEMENTADO**

✅ **Campañas** → Bot envía mensajes masivos a contactos  
✅ **Webhook** → Bot recibe mensajes entrantes de WhatsApp  
✅ **Conversaciones** → Se crean automáticamente en la plataforma  
✅ **Chat bidireccional** → Desde plataforma hacia WhatsApp del cliente  

---

## **CONFIGURACIÓN REQUERIDA**

### **1. Variables de entorno**

Crear archivo `.env` en la carpeta `bot/`:

```bash
# Configuración de WhatsApp Business API
WHATSAPP_API_TOKEN=tu_token_de_whatsapp_aqui
WHATSAPP_NUMBER_ID=tu_number_id_aqui
WHATSAPP_VERIFY_TOKEN=tu_token_secreto_para_webhook

# Configuración del servidor
PORT=5000
HOST=0.0.0.0
DEBUG=false

# URLs de servicios
API_GATEWAY_URL=http://localhost:8080
BACKEND_URL=http://localhost:9000
WEBHOOK_URL=https://tu-dominio.com/webhook/whatsapp

# Configuración de seguridad
API_GATEWAY_SECRET=secret-123-gateway

# Configuración de CORS
CORS_ORIGIN=http://localhost:3000
CORS_CREDENTIALS=true

# Configuración de logs
LOG_LEVEL=INFO
LOG_FILE=bot.log

# Configuración de WhatsApp
WHATSAPP_API_VERSION=v21.0
WHATSAPP_BASE_URL=https://graph.facebook.com
```

### **2. Configurar WhatsApp Business API**

1. **Crear aplicación en Meta for Developers**:
   - Ve a https://developers.facebook.com/
   - Crea una nueva aplicación
   - Agrega el producto "WhatsApp Business API"

2. **Obtener credenciales**:
   - `WHATSAPP_API_TOKEN`: Token de acceso permanente
   - `WHATSAPP_NUMBER_ID`: ID del número de teléfono
   - `WHATSAPP_VERIFY_TOKEN`: Token secreto para webhook (créalo tú)

3. **Configurar webhook**:
   - URL del webhook: `https://tu-dominio.com/webhook/whatsapp`
   - Token de verificación: El que pusiste en `WHATSAPP_VERIFY_TOKEN`
   - Eventos: `messages`

---

## **ENDPOINTS IMPLEMENTADOS**

### **Campañas masivas**
- `POST /campaigns/send` - Envía campaña a todos los contactos
- `GET /campaigns/:id/status` - Estado de campaña

### **Mensajes individuales**
- `POST /send/message` - Envía mensaje individual

### **Webhook**
- `GET /webhook/whatsapp` - Verificación de webhook
- `POST /webhook/whatsapp` - Recibe mensajes entrantes

### **Sistema**
- `GET /health` - Health check

---

## **FLUJO DE FUNCIONAMIENTO**

### **1. Envío de campañas**
```
Frontend → API Gateway → Bot → WhatsApp API → Clientes
```

### **2. Respuesta de clientes**
```
WhatsApp API → Bot Webhook → Backend → Frontend (WebSocket)
```

### **3. Chat bidireccional**
```
Frontend → API Gateway → Bot → WhatsApp API → Cliente específico
```

---

## **INSTALACIÓN Y EJECUCIÓN**

### **1. Instalar dependencias**
```bash
cd bot/
pip install -r requirements.txt
```

### **2. Configurar variables**
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

### **3. Ejecutar bot**
```bash
python main.py
```

### **4. Verificar funcionamiento**
```bash
curl http://localhost:5000/health
```

---

## **INTEGRACIÓN CON OTROS SERVICIOS**

### **Backend (Puerto 9000)**
- Rutas internas para obtener contactos
- Creación automática de conversaciones
- Actualización de estados de campañas

### **API Gateway (Puerto 8080)**
- Proxy de rutas hacia el bot
- Autenticación y autorización
- Logging de peticiones

### **Frontend (Puerto 3000)**
- Envío de campañas desde la interfaz
- Visualización de conversaciones
- Chat en tiempo real

---

## **TESTING**

### **1. Test de campaña**
```bash
curl -X POST http://localhost:8080/campaigns/send \
  -H "Authorization: Bearer tu_token" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_id": "1",
    "message": "Hola, este es un mensaje de prueba"
  }'
```

### **2. Test de mensaje individual**
```bash
curl -X POST http://localhost:8080/send/message \
  -H "Authorization: Bearer tu_token" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+51987654321",
    "message": "Mensaje de prueba individual"
  }'
```

### **3. Test de webhook**
```bash
curl -X GET "http://localhost:5000/webhook/whatsapp?hub.mode=subscribe&hub.verify_token=tu_token_secreto&hub.challenge=test123"
```

---

## **TROUBLESHOOTING**

### **Error: Token inválido**
- Verificar `WHATSAPP_API_TOKEN` en Meta for Developers
- Asegurar que el token tenga permisos de WhatsApp Business API

### **Error: Webhook no verifica**
- Verificar que `WHATSAPP_VERIFY_TOKEN` coincida en Meta y en `.env`
- Asegurar que la URL del webhook sea accesible públicamente

### **Error: No se conecta al backend**
- Verificar que `BACKEND_URL` esté correcto
- Asegurar que el backend esté ejecutándose en el puerto 9000

### **Error: Mensajes no se envían**
- Verificar `WHATSAPP_NUMBER_ID` en Meta for Developers
- Asegurar que el número esté verificado y aprobado

---

## **LOGS Y MONITOREO**

Los logs se guardan en `bot.log` y incluyen:
- Mensajes enviados y recibidos
- Errores de conexión
- Estados de campañas
- Webhooks procesados

Para monitorear en tiempo real:
```bash
tail -f bot.log
``` 