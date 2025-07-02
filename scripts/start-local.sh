#!/bin/bash

# 🚀 Script para iniciar todas las plataformas independientes de Alesse Connect
# Basado en arquitectura de plataformas separadas en ubicaciones diferentes

echo "🌟 INICIANDO PLATAFORMAS INDEPENDIENTES ALESSE CONNECT"
echo "=" * 60

# Verificar que estamos en el directorio correcto
if [[ ! -f "main.py" ]]; then
    echo "❌ Error: Este script debe ejecutarse desde el directorio del bot"
    echo "💡 Ejecuta: cd /ruta/a/bot && bash scripts/start-local.sh"
    exit 1
fi

# Función para verificar si un puerto está en uso
check_port() {
    local port=$1
    local service=$2
    
    if nc -z localhost $port 2>/dev/null; then
        echo "✅ Puerto $port ($service) está disponible"
        return 0
    else
        echo "⚠️ Puerto $port ($service) no responde - verificar si está iniciado"
        return 1
    fi
}

# Función para iniciar PostgreSQL si no está corriendo
start_postgresql() {
    echo "🗄️ Verificando PostgreSQL..."
    
    if ! pg_isready -q 2>/dev/null; then
        echo "🔧 PostgreSQL no está corriendo. Intentando iniciar..."
        
        # Intentar iniciar PostgreSQL según el OS
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo systemctl start postgresql
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            brew services start postgresql
        elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
            net start postgresql-x64-14
        fi
        
        sleep 3
        
        if pg_isready -q 2>/dev/null; then
            echo "✅ PostgreSQL iniciado correctamente"
        else
            echo "❌ No se pudo iniciar PostgreSQL automáticamente"
            echo "💡 Inicia PostgreSQL manualmente y ejecuta el script de nuevo"
            exit 1
        fi
    else
        echo "✅ PostgreSQL está corriendo"
    fi
}

# Función para verificar variables de entorno
check_environment() {
    echo "🔧 Verificando variables de entorno..."
    
    if [[ ! -f ".environment" ]]; then
        echo "❌ Archivo .environment no encontrado"
        echo "💡 Copia .environment.example a .environment y configúralo"
        exit 1
    fi
    
    source .environment
    
    # Verificar variables críticas
    if [[ -z "$TWILIO_ACCOUNT_SID" || -z "$TWILIO_AUTH_TOKEN" || -z "$API_GATEWAY_URL" ]]; then
        echo "❌ Variables de entorno faltantes en .environment"
        echo "💡 Configura: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, API_GATEWAY_URL"
        exit 1
    fi
    
    echo "✅ Variables de entorno configuradas"
}

# Función para instalar dependencias si es necesario
check_dependencies() {
    echo "📦 Verificando dependencias de Python..."
    
    if [[ ! -d "venv" && ! -d ".venv" ]]; then
        echo "🐍 Creando entorno virtual..."
        python3 -m venv venv
        source venv/bin/activate
    else
        echo "✅ Entorno virtual detectado"
        if [[ -d "venv" ]]; then
            source venv/bin/activate
        else
            source .venv/bin/activate
        fi
    fi
    
    echo "📥 Instalando/actualizando dependencias..."
    pip install -r requirements.txt --quiet
    
    echo "✅ Dependencias de Python listas"
}

# Función principal
main() {
    echo "🏁 FASE 1: VERIFICACIONES PREVIAS"
    echo "-" * 40
    
    check_environment
    start_postgresql
    check_dependencies
    
    # Verificar conexión a la base de datos
    echo "🗄️ Verificando conexión a base de datos alesse_connect..."
    if python scripts/verify-database.py --quiet; then
        echo "✅ Base de datos alesse_connect conectada correctamente"
    else
        echo "⚠️ Problemas con la base de datos - el bot puede funcionar con limitaciones"
        echo "💡 Ejecuta: python scripts/verify-database.py para más detalles"
    fi
    
    echo ""
    echo "🏁 FASE 2: VERIFICAR OTRAS PLATAFORMAS"
    echo "-" * 40
    
    # Verificar API Gateway (debe estar corriendo)
    if ! check_port 8080 "API Gateway"; then
        echo "⚠️ API Gateway (puerto 8080) no responde"
        echo "💡 Inicia el API Gateway primero:"
        echo "   cd /ruta/api-gateway && npm start"
        echo ""
    fi
    
    # Verificar Backend (debe estar corriendo)
    if ! check_port 9000 "Backend"; then
        echo "⚠️ Backend (puerto 9000) no responde"
        echo "💡 Inicia el Backend primero:"
        echo "   cd /ruta/backend && npm run dev"
        echo ""
    fi
    
    # Verificar Frontend (opcional)
    if ! check_port 3000 "Frontend"; then
        echo "ℹ️ Frontend (puerto 3000) no responde (opcional)"
        echo "💡 Para iniciar Frontend:"
        echo "   cd /ruta/frontend && npm run dev"
        echo ""
    fi
    
    echo "🏁 FASE 3: INICIAR BOT WHATSAPP"
    echo "-" * 40
    
    echo "🤖 Iniciando WhatsApp Microservice en puerto 5000..."
    echo "🔗 Configurado para comunicarse con API Gateway: $API_GATEWAY_URL"
    echo "📱 Twilio WhatsApp: $TWILIO_WHATSAPP_NUMBER"
    echo ""
    echo "🌟 LOGS DEL BOT:"
    echo "=" * 40
    
    # Ejecutar el bot
    python main.py
}

# Manejar señales de interrupción
trap 'echo -e "\n🛑 Deteniendo WhatsApp Microservice..."; exit 0' INT TERM

# Ejecutar función principal
main "$@" 