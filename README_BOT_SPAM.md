# 🤖 Bot de Spam Masivo - Alesse Connect

## 📋 Descripción

Sistema completo de envío masivo de templates para WhatsApp integrado con tu bot existente de Alesse Connect. Permite:

- ✅ **Leer base de datos** de clientes con nombres y números
- ✅ **Enviar templates personalizados** masivamente
- ✅ **Control de delays** para parecer humano
- ✅ **Historial completo** de envíos
- ✅ **Interfaz de gestión** fácil de usar

## 🚀 Instalación y Configuración

### 1. Dependencias

Tu proyecto ya tiene las dependencias necesarias configuradas:

```bash
# Ya instaladas en tu proyecto:
# - twilio (para WhatsApp)
# - sqlite3 (base de datos)
# - flask (interfaz web)
# - dotenv (variables de entorno)
```

### 2. Configuración

Las credenciales ya están en tu archivo `.environment`:

```env
TWILIO_ACCOUNT_SID=ACa04b8f9a85c8c2668b35343b45ed080e
TWILIO_AUTH_TOKEN=921ceec8e8869000aebe9bec97f4b106
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

## 🎯 Uso del Sistema

### Opción 1: Menú Interactivo (Recomendado)

```bash
# Ejecutar el menú principal
python run_spam_bot.py
```

**Funciones disponibles:**

1. **📊 Ver estadísticas** - Estado actual del sistema
2. **👥 Gestionar clientes** - Agregar/ver clientes
3. **📝 Gestionar templates** - Crear/ver mensajes
4. **🚀 Enviar spam masivo** - Iniciar envío
5. **📈 Ver historial** - Revisar envíos anteriores
6. **🔧 Test de conexión** - Verificar Twilio

### Opción 2: Prueba Rápida

```bash
# Verificar que todo funciona
python test_spam_bot_simple.py
```

## 📊 Base de Datos Automática

El sistema crea automáticamente una base SQLite (`clientes_spam.db`) con:

### Tabla `clientes`
- `nombre` - Nombre completo
- `telefono` - Número WhatsApp (+51999123456)
- `email` - Email opcional
- `activo` - Estado del cliente
- `total_enviados` - Contador de mensajes
- `ultimo_envio` - Última fecha de envío

### Tabla `templates`
- `nombre` - Nombre del template
- `contenido` - Mensaje con variables {nombre}
- `activo` - Estado del template

### Tabla `envios`
- `cliente_id` - ID del cliente
- `template_id` - ID del template
- `mensaje` - Mensaje personalizado enviado
- `estado` - 'enviado' o 'fallido'
- `fecha_envio` - Timestamp del envío

## 🎯 Templates Predefinidos

El sistema incluye templates de ejemplo:

1. **Promoción SOAT**
```
🚗 ¡Hola {nombre}! Tu SOAT está por vencer. Renuévalo con nosotros y ahorra hasta 30%. ¡No te quedes sin protección! 📞 Llámanos: +51999888777
```

2. **Seguro Vehicular**
```
🛡️ ¡{nombre}! Protege tu vehículo con nuestro seguro todo riesgo. Cobertura completa desde S/299. ¡Consulta ya! 🚙
```

3. **Recordatorio Renovación**
```
⏰ Estimado/a {nombre}, tu póliza vence pronto. Renueva antes del vencimiento y mantén tu protección activa. 📋
```

## 🔧 Funciones Principales

### 1. Gestión de Clientes

```python
# Agregar cliente individual
spam_service.agregar_cliente("Juan Pérez", "+51999123456", "juan@email.com")

# Obtener clientes activos
clientes = spam_service.obtener_clientes_activos()
```

### 2. Gestión de Templates

```python
# Crear template personalizado
spam_service.crear_template(
    nombre="Mi Template",
    contenido="Hola {nombre}, mensaje personalizado aquí"
)

# Ver templates disponibles
templates = spam_service.obtener_templates_disponibles()
```

### 3. Envío Masivo

```python
# Iniciar envío masivo
result = spam_service.enviar_spam_masivo(
    template_nombre="Promoción SOAT",
    delay_min=5,    # 5 segundos mínimo
    delay_max=15    # 15 segundos máximo
)
```

### 4. Monitoreo

```python
# Ver estadísticas en tiempo real
stats = spam_service.obtener_estadisticas()

# Ver historial de envíos
historial = spam_service.obtener_historial_envios(limite=50)

# Cancelar envío en progreso
spam_service.cancelar_envio()
```

## 📱 Ejemplos de Uso

### Ejemplo 1: Campaña SOAT

```python
# 1. Agregar clientes objetivo
clientes_soat = [
    ("Carlos López", "+51999111111", "carlos@email.com"),
    ("María García", "+51999222222", "maria@email.com"),
    ("Pedro Sánchez", "+51999333333", "pedro@email.com")
]

for nombre, telefono, email in clientes_soat:
    spam_service.agregar_cliente(nombre, telefono, email)

# 2. Crear template específico
spam_service.crear_template(
    "SOAT Urgente",
    "🚨 {nombre}, tu SOAT vence en 7 días. Renueva ya y evita multas. Llama: +51999888777"
)

# 3. Enviar campaña
spam_service.enviar_spam_masivo("SOAT Urgente", delay_min=10, delay_max=20)
```

### Ejemplo 2: Seguros Vehiculares

```python
# Template promocional
spam_service.crear_template(
    "Seguro Promo",
    "🎁 {nombre}, oferta especial: Seguro vehicular con 40% descuento. Solo este mes. ¿Te interesa?"
)

# Envío con delays más largos para parecer más humano
spam_service.enviar_spam_masivo("Seguro Promo", delay_min=15, delay_max=30)
```

## ⚡ Características Avanzadas

### 1. **Delays Inteligentes**
- Tiempo aleatorio entre envíos para evitar detección
- Configurable por campaña (5-120 segundos)

### 2. **Personalización Automática**
- Variables: `{nombre}`, `{telefono}`, `{email}`
- Reemplazo automático en templates

### 3. **Control de Estado**
- Envíos en segundo plano
- Cancelación en tiempo real
- Estadísticas en vivo

### 4. **Historial Completo**
- Registro de todos los envíos
- Estados: enviado/fallido
- Timestamps precisos

### 5. **Manejo de Errores**
- Reconexión automática
- Logs detallados
- Fallbacks seguros

## 🛡️ Seguridad y Mejores Prácticas

### 1. **Límites de WhatsApp**
- **Máximo:** 1,000 mensajes/día en sandbox
- **Recomendado:** 50-100 mensajes/hora
- **Delays:** 10-30 segundos entre mensajes

### 2. **Templates Efectivos**
```
✅ Buenos:
- Mensajes cortos (< 160 caracteres)
- Llamada a la acción clara
- Personalización con {nombre}
- Emojis moderados

❌ Evitar:
- Mensajes muy largos
- Demasiadas mayúsculas
- Spam obvio
- Enlaces sospechosos
```

### 3. **Gestión de Listas**
```python
# Limpiar clientes inactivos
# Filtrar por respuestas negativas
# Respetar solicitudes de STOP
```

## 📊 Integración con tu Bot Principal

### Opción 1: Uso Independiente
El bot de spam funciona completamente independiente de tu bot principal `app_ddd.py`.

### Opción 2: Integración
```python
# En tu app_ddd.py
from spam_bot_service import spam_service

# Agregar endpoint para spam masivo
@app.route('/admin/spam', methods=['POST'])
def admin_spam():
    template = request.json['template']
    result = spam_service.enviar_spam_masivo(template)
    return jsonify(result)
```

## 🚨 Solución de Problemas

### Error: "Cliente Twilio no inicializado"
```bash
# Verificar credenciales en .environment
# Revisar conexión a internet
python test_spam_bot_simple.py
```

### Error: "Template no encontrado"
```python
# Ver templates disponibles
templates = spam_service.obtener_templates_disponibles()
print([t['nombre'] for t in templates])
```

### Error: "Base de datos bloqueada"
```bash
# Cerrar otras instancias del bot
# Reiniciar el servicio
```

## 📈 Métricas y Análisis

### Dashboard en Tiempo Real
```python
stats = spam_service.obtener_estadisticas()
print(f"Enviados: {stats['enviados']}")
print(f"Fallidos: {stats['fallidos']}")
print(f"Progreso: {stats['enviados'] + stats['fallidos']}/{stats['total']}")
```

### Análisis de Campañas
```python
historial = spam_service.obtener_historial_envios()
exitosos = [h for h in historial if h['estado'] == 'enviado']
tasa_exito = len(exitosos) / len(historial) * 100
print(f"Tasa de éxito: {tasa_exito:.1f}%")
```

## 🎯 Comandos Rápidos

```bash
# Iniciar bot con menú
python run_spam_bot.py

# Prueba rápida
python test_spam_bot_simple.py

# Ver base de datos (opcional)
sqlite3 clientes_spam.db ".tables"
sqlite3 clientes_spam.db "SELECT * FROM clientes LIMIT 5;"
```

## 📞 Soporte

Para dudas sobre el bot de spam:

1. **Revisar logs** en consola
2. **Ejecutar test** básico
3. **Verificar credenciales** Twilio
4. **Consultar historial** de envíos

---

## ⚡ Inicio Rápido (5 minutos)

```bash
# 1. Probar conexión
python test_spam_bot_simple.py

# 2. Iniciar interfaz
python run_spam_bot.py

# 3. En el menú:
#    - Opción 2: Agregar clientes
#    - Opción 3: Crear templates  
#    - Opción 4: Enviar spam masivo

# 4. ¡Listo! 🚀
```

**¡Tu bot de spam masivo está listo para generar leads y aumentar ventas!** 💰 