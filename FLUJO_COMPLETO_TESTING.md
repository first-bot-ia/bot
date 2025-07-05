# 🧪 Testing del Flujo Completo - WhatsApp Bot

## **🎯 FLUJO IMPLEMENTADO COMPLETO**

```
1. CAMPAÑA MASIVA:
   Frontend → API Gateway → Bot → Backend (contactos) → WhatsApp API → Todos los contactos

2. RESPUESTA DE CLIENTE:
   WhatsApp API → Bot Webhook → Backend → Conversación creada → Frontend (WebSocket) → Notificación

3. CHAT BIDIRECCIONAL:
   Frontend → API Gateway → Bot → WhatsApp API → Cliente específico
```

---

## **🚀 PASOS PARA PROBAR TODO**

### **PASO 1: Configurar servicios**

```bash
# 1. Backend (Puerto 9000)
cd Backend
npm run dev

# 2. API Gateway (Puerto 8080)
cd api-gateway
npm run dev

# 3. Bot (Puerto 5000)
cd bot
python main.py

# 4. Frontend (Puerto 3000)
cd Fronted
npm start
```

### **PASO 2: Verificar conexiones**

```bash
# Health checks
curl http://localhost:9000/health
curl http://localhost:8080/health
curl http://localhost:5000/health

# WebSocket del backend debe estar en puerto 9001
# El frontend se conectará automáticamente al WebSocket
```

---

## **🧪 TESTING PASO A PASO**

### **TEST 1: Envío de Campaña Masiva**

1. **Acceder al frontend** → `http://localhost:3000`
2. **Login** como admin/supervisor
3. **Ir a Campañas** → Crear nueva campaña
4. **Enviar campaña** con mensaje: `"Hola, este es un mensaje de prueba desde nuestra plataforma"`

**Resultado esperado:**
- ✅ Mensaje se envía a todos los contactos en la base de datos
- ✅ Estado de campaña se actualiza en tiempo real
- ✅ Logs del bot muestran envíos exitosos

**Comando de prueba directo:**
```bash
curl -X POST http://localhost:8080/campaigns/send \
  -H "Authorization: Bearer tu_token_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_id": "1",
    "message": "Hola, este es un mensaje de prueba"
  }'
```

### **TEST 2: Webhook - Respuesta de Cliente**

1. **Desde tu WhatsApp personal** → Responder al mensaje de la campaña
2. **Verificar en el frontend** → Debe aparecer nueva conversación automáticamente
3. **Verificar notificación** → Debe sonar/aparecer notificación en el navegador

**Resultado esperado:**
- ✅ Conversación aparece en la lista automáticamente
- ✅ Mensaje del cliente se muestra correctamente
- ✅ WebSocket funciona (tiempo real)
- ✅ Notificación del navegador aparece

**Logs a verificar:**
```bash
# En el bot
tail -f bot.log
# Debe mostrar: "Received message from +51XXXXXXXXX: [mensaje]"
# Debe mostrar: "Conversation created/updated for +51XXXXXXXXX"

# En el backend
# Debe mostrar: "New conversation created from webhook"
```

### **TEST 3: Chat Bidireccional**

1. **En el frontend** → Hacer clic en la conversación recién creada
2. **Escribir respuesta** → "Hola, gracias por contactarnos. ¿En qué te puedo ayudar?"
3. **Enviar mensaje** → Debe llegar al WhatsApp del cliente
4. **Cliente responde** → Debe aparecer en tiempo real en la plataforma

**Resultado esperado:**
- ✅ Mensaje del asesor llega al WhatsApp del cliente
- ✅ Respuesta del cliente aparece automáticamente en la plataforma
- ✅ Chat fluye de forma bidireccional
- ✅ Timestamps correctos en ambos lados

**Comando de prueba directo:**
```bash
curl -X POST http://localhost:8080/conversations/1/reply \
  -H "Authorization: Bearer tu_token_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hola, gracias por contactarnos"
  }'
```

---

## **🔍 VERIFICACIONES TÉCNICAS**

### **Backend - Base de datos**
```sql
-- Verificar conversaciones creadas
SELECT * FROM conversations ORDER BY createdAt DESC LIMIT 5;

-- Verificar mensajes
SELECT * FROM messages ORDER BY timestamp DESC LIMIT 10;

-- Verificar contactos
SELECT * FROM contacts WHERE status = 'ACTIVE';
```

### **WebSocket - Conexión**
```javascript
// En el navegador (DevTools → Console)
console.log('WebSocket status:', websocketService.isConnected());

// Verificar eventos recibidos
// Deben aparecer logs como:
// "🔔 Nueva conversación: {...}"
// "💬 Nuevo mensaje: {...}"
```

### **Bot - Logs detallados**
```bash
# Verificar logs del bot
tail -f bot.log | grep -E "(Campaign|Webhook|Message)"

# Logs esperados:
# "Starting campaign 1 with message: Hola..."
# "Message sent to +51XXXXXXXXX"
# "Received message from +51XXXXXXXXX: ..."
# "Conversation created/updated for +51XXXXXXXXX"
```

---

## **🐛 TROUBLESHOOTING**

### **Error: Campaña no se envía**
```bash
# Verificar contactos en base de datos
curl http://localhost:9000/internal/campaigns/1/contacts

# Verificar token de WhatsApp
# Revisar bot/.env → WHATSAPP_API_TOKEN
```

### **Error: Webhook no recibe mensajes**
```bash
# Verificar webhook en Meta for Developers
# URL: https://tu-dominio.com/webhook/whatsapp
# Token: debe coincidir con WHATSAPP_VERIFY_TOKEN

# Test webhook local
curl -X GET "http://localhost:5000/webhook/whatsapp?hub.mode=subscribe&hub.verify_token=tu_token&hub.challenge=test123"
```

### **Error: WebSocket no conecta**
```bash
# Verificar puerto del backend WebSocket
netstat -an | grep 9001

# Verificar CORS en backend
# Debe permitir origen http://localhost:3000
```

### **Error: Mensajes no llegan a WhatsApp**
```bash
# Verificar número de WhatsApp en Meta
# Debe estar verificado y aprobado para envío

# Test directo al bot
curl -X POST http://localhost:5000/send/message \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+51XXXXXXXXX",
    "message": "Test directo"
  }'
```

---

## **✅ CHECKLIST DE FUNCIONAMIENTO COMPLETO**

- [ ] **Backend ejecutándose** (Puerto 9000)
- [ ] **API Gateway ejecutándose** (Puerto 8080)
- [ ] **Bot ejecutándose** (Puerto 5000)
- [ ] **Frontend ejecutándose** (Puerto 3000)
- [ ] **WebSocket conectado** (Puerto 9001)
- [ ] **Base de datos con contactos** (Al menos 1 contacto activo)
- [ ] **Token de WhatsApp válido** (Configurado en bot/.env)
- [ ] **Webhook verificado** (En Meta for Developers)
- [ ] **Campaña se envía correctamente**
- [ ] **Webhook recibe respuestas**
- [ ] **Conversaciones aparecen automáticamente**
- [ ] **Chat bidireccional funciona**
- [ ] **Notificaciones en tiempo real**

---

## **🎉 RESULTADO FINAL ESPERADO**

**¡Si todos los tests pasan, tendrás:**

1. ✅ **Plataforma completa de campañas masivas**
2. ✅ **Recepción automática de respuestas**
3. ✅ **Chat bidireccional en tiempo real**
4. ✅ **Notificaciones instantáneas**
5. ✅ **Integración completa WhatsApp ↔ Plataforma**

**🚀 Tu plataforma estará 100% funcional para uso en producción!** 