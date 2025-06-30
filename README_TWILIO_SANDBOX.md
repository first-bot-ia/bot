# 🤖 Bot de Spam Masivo - Twilio WhatsApp Sandbox

Sistema completo para envío masivo de mensajes WhatsApp usando Twilio Sandbox.

## 🎯 Características

- ✅ **Sin limitaciones de Meta/Facebook** - Usa Twilio Sandbox
- 📱 **Envío masivo** a múltiples clientes
- 🎨 **Interfaz web moderna** para gestión
- 📊 **Estadísticas en tiempo real**
- 🔄 **Webhooks automáticos** para respuestas
- 🎭 **Templates predefinidos** del sandbox
- ⏱️ **Delays personalizables** para parecer humano

## 📋 Requisitos Previos

1. **Cuenta de Twilio** (gratuita): https://console.twilio.com/
2. **Python 3.7+**
3. **ngrok** para exponer webhooks

## 🚀 Instalación Rápida

### 1. Instalar dependencias
```bash
pip install -r requirements_spam.txt
```

### 2. Configurar Twilio
1. Ve a https://console.twilio.com/
2. Copia tu **Account SID** y **Auth Token**
3. Edita el archivo `.environment`:
```env
TWILIO_ACCOUNT_SID=tu_account_sid_aqui
TWILIO_AUTH_TOKEN=tu_auth_token_aqui
```

### 3. Configurar WhatsApp Sandbox
1. Ve a: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
2. Únete al sandbox enviando `join [tu-keyword]` al **+1 415 523 8886**
3. Anota tu keyword (ej: "join happy-lion")

### 4. Instalar ngrok
```bash
# Opción 1: Instalación automática
python setup_ngrok.py

# Opción 2: Manual
# Ve a https://ngrok.com/download
# Descarga y coloca ngrok.exe en esta carpeta
```

## 🎮 Uso del Sistema

### Iniciar el Bot
```bash
python run_spam_bot.py
```

### Configurar Webhook (en otra terminal)
```bash
python setup_ngrok.py
# Elige opción 1 para iniciar ngrok
# Copia la URL (ej: https://abc123.ngrok.io)
```

### Configurar en Twilio Console
1. Ve a: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
2. En **"When a message comes in"**, pega:
   ```
   https://abc123.ngrok.io/whatsapp/webhook
   ```
3. Guarda los cambios

## 🌐 Interfaz Web

Abre en tu navegador: **http://localhost:5001**

### Pestañas Disponibles:

#### 📊 Dashboard
- Estado del sistema
- Estadísticas de envío
- Test de conexión Twilio

#### 👥 Clientes
- Agregar nuevos clientes
- Ver lista de clientes activos
- Gestionar base de datos

#### 📝 Templates
- Ver templates disponibles del sandbox:
  - 📅 **Recordatorio de Cita**
  - 📦 **Notificación de Pedido** 
  - 🔐 **Código de Verificación**

#### 🚀 Enviar Spam
- Seleccionar template
- Configurar delays entre envíos
- Iniciar campaña masiva

#### 📈 Historial
- Ver envíos realizados
- Estadísticas detalladas
- Logs del sistema

## ⚠️ Limitaciones del Sandbox

- Solo pueden recibir mensajes los números que se unieron al sandbox
- Máximo 1 mensaje cada 3 segundos
- Templates predefinidos (no se pueden crear nuevos)
- Solo para pruebas y desarrollo

## 📱 Agregar Números de Prueba

Para que un número pueda recibir mensajes:

1. Desde WhatsApp, envía mensaje a **+1 415 523 8886**
2. Mensaje: `join [tu-keyword]`
3. Recibirás confirmación
4. Ahora ese número puede recibir mensajes del bot

## 🎭 Templates Disponibles

### 📅 Recordatorio de Cita
```
Your appointment is coming up on {{1}} at {{2}}
```
**Ejemplo:** "Your appointment is coming up on July 21 at 3PM"

### 📦 Notificación de Pedido
```
Your {{1}} order of {{2}} has shipped and should be delivered on {{3}}. Details: {{4}}
```
**Ejemplo:** "Your SOAT order of 2 chairs has shipped and should be delivered on July 25. Details: Track with code ABC123"

### 🔐 Código de Verificación
```
Your {{1}} code is {{2}}
```
**Ejemplo:** "Your verification code is 123456"

## 🔧 Configuración Avanzada

### Variables de Entorno (.environment)
```env
# Credenciales Twilio
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Configuración servidor
FLASK_PORT=5000
FLASK_DEBUG=True
WEBHOOK_URL=http://localhost:5000/whatsapp/webhook

# Base de datos
DATABASE_PATH=clientes_spam.db
```

### Personalizar Delays
- **delay_min**: Tiempo mínimo entre envíos (segundos)
- **delay_max**: Tiempo máximo entre envíos (segundos)
- Recomendado: 5-15 segundos para parecer humano

## 🐛 Solución de Problemas

### Error: "Cliente Twilio no inicializado"
- Verifica las credenciales en `.environment`
- Ejecuta `python run_spam_bot.py` para test automático

### Error: "ngrok no encontrado"
- Ejecuta `python setup_ngrok.py`
- Descarga manual: https://ngrok.com/download

### Error: "No se puede enviar mensaje"
- Verifica que el número se unió al sandbox
- Envía `join [keyword]` al +1 415 523 8886

### Error: "Webhook no recibe mensajes"
- Verifica que ngrok esté ejecutándose
- Copia correctamente la URL en Twilio Console
- URL debe terminar en `/whatsapp/webhook`

## 📊 APIs Disponibles

### GET /api/stats
Estadísticas generales del sistema

### GET /api/clients
Lista de clientes activos

### POST /api/clients
Agregar nuevo cliente

### GET /api/templates
Templates disponibles del sandbox

### POST /api/send-spam
Iniciar envío masivo

### GET /api/history
Historial de envíos

## 🔒 Seguridad

- Las credenciales se almacenan en `.environment`
- No incluir `.environment` en control de versiones
- Usar solo para pruebas y desarrollo
- Para producción, usar WhatsApp Business API completa

## 📞 Soporte

- **Documentación Twilio**: https://www.twilio.com/docs/whatsapp/sandbox
- **Console Twilio**: https://console.twilio.com/
- **Sandbox WhatsApp**: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn

## 🎉 ¡Listo para Usar!

1. ✅ Configurar credenciales en `.environment`
2. ✅ Ejecutar `python run_spam_bot.py`
3. ✅ Iniciar ngrok con `python setup_ngrok.py`
4. ✅ Configurar webhook en Twilio Console
5. ✅ Abrir http://localhost:5001
6. ✅ ¡Enviar mensajes masivos!

---

**⚠️ Uso Responsable**: Este sistema es para pruebas y desarrollo. Respeta las políticas de WhatsApp y Twilio. 