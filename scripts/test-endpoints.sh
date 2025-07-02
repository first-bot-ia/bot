#!/bin/bash

# 🧪 Script de testing para WhatsApp Microservice
# Prueba todos los endpoints y comunicación con API Gateway

BOT_URL="http://localhost:5000"
API_GATEWAY_URL="http://localhost:8080"

echo "🧪 TESTING WHATSAPP MICROSERVICE - ALESSE CONNECT"
echo "=" * 60
echo "🤖 Bot URL: $BOT_URL"
echo "🌐 API Gateway URL: $API_GATEWAY_URL"
echo ""

# Función para hacer requests HTTP
make_request() {
    local method=$1
    local url=$2
    local data=$3
    local description=$4
    
    echo "🔍 Testing: $description"
    echo "📡 $method $url"
    
    if [[ -n "$data" ]]; then
        response=$(curl -s -w "\n%{http_code}" -X $method \
            -H "Content-Type: application/json" \
            -d "$data" \
            "$url" 2>/dev/null)
    else
        response=$(curl -s -w "\n%{http_code}" -X $method "$url" 2>/dev/null)
    fi
    
    # Separar body y status code
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n -1)
    
    if [[ $http_code -ge 200 && $http_code -lt 300 ]]; then
        echo "✅ Status: $http_code"
        echo "📄 Response: $(echo "$body" | head -c 200)..."
    elif [[ $http_code -ge 400 && $http_code -lt 500 ]]; then
        echo "⚠️ Status: $http_code (Client Error)"
        echo "📄 Response: $body"
    elif [[ $http_code -ge 500 ]]; then
        echo "❌ Status: $http_code (Server Error)"
        echo "📄 Response: $body"
    else
        echo "🔌 Sin respuesta del servidor"
    fi
    
    echo "-" * 40
    echo ""
}

# Función para verificar si el servicio está corriendo
check_service() {
    local url=$1
    local name=$2
    
    echo "🔍 Verificando $name..."
    
    if curl -s --connect-timeout 5 "$url/health" > /dev/null 2>&1; then
        echo "✅ $name está corriendo"
        return 0
    else
        echo "❌ $name no responde"
        return 1
    fi
}

main() {
    echo "🏁 FASE 1: VERIFICAR SERVICIOS"
    echo "-" * 40
    
    # Verificar que el bot esté corriendo
    if ! check_service "$BOT_URL" "WhatsApp Bot"; then
        echo "💡 Inicia el bot con: python main.py"
        exit 1
    fi
    
    # Verificar API Gateway (opcional para algunos tests)
    api_gateway_running=false
    if check_service "$API_GATEWAY_URL" "API Gateway"; then
        api_gateway_running=true
    else
        echo "⚠️ API Gateway no responde - algunos tests serán omitidos"
    fi
    
    echo ""
    echo "🏁 FASE 2: TESTING ENDPOINTS PÚBLICOS"
    echo "-" * 40
    
    # Test 1: Health check básico
    make_request "GET" "$BOT_URL/health" "" "Health check básico"
    
    # Test 2: Endpoint de envío directo de mensaje
    test_message='{
        "phone": "+51999123456",
        "message": "🧪 Mensaje de prueba desde testing script",
        "media_url": null
    }'
    make_request "POST" "$BOT_URL/send/message" "$test_message" "Envío directo de mensaje"
    
    # Test 3: Simulación de webhook de Twilio
    webhook_data='{
        "From": "whatsapp:+51999123456",
        "Body": "Hola, esto es una prueba",
        "MessageSid": "SMtesting123456789",
        "AccountSid": "ACtest123",
        "NumMedia": "0"
    }'
    make_request "POST" "$BOT_URL/whatsapp/webhook" "$webhook_data" "Webhook de Twilio (simulado)"
    
    echo "🏁 FASE 3: TESTING ENDPOINTS INTERNOS"
    echo "-" * 40
    
    # Test 4: Health check detallado
    make_request "GET" "$BOT_URL/internal/health/detailed" "" "Health check detallado"
    
    # Test 5: Envío desde Backend (simulado)
    backend_message='{
        "phone": "+51999123456",
        "message": "Mensaje desde asesor de prueba",
        "advisor_id": "asesor-test-001",
        "conversation_id": "conv-test-123"
    }'
    make_request "POST" "$BOT_URL/internal/send-message-to-user" "$backend_message" "Envío desde Backend (simulado)"
    
    echo "🏁 FASE 4: TESTING INTEGRACIÓN API GATEWAY"
    echo "-" * 40
    
    if [[ "$api_gateway_running" == true ]]; then
        # Test 6: Health check del API Gateway
        make_request "GET" "$API_GATEWAY_URL/health" "" "Health check API Gateway"
        
        # Test 7: Endpoint que debería existir en API Gateway
        gateway_test='{
            "source": "bot-testing",
            "message": "Test de comunicación bot -> API Gateway"
        }'
        make_request "POST" "$API_GATEWAY_URL/webhook/test" "$gateway_test" "Test comunicación con API Gateway"
    else
        echo "⚠️ Omitiendo tests de API Gateway (no está corriendo)"
    fi
    
    echo "🏁 FASE 5: TESTING CASOS EDGE"
    echo "-" * 40
    
    # Test 8: Request sin datos
    make_request "POST" "$BOT_URL/send/message" "" "Request sin JSON (debe fallar)"
    
    # Test 9: Request con datos inválidos
    invalid_data='{"phone": "", "message": ""}'
    make_request "POST" "$BOT_URL/send/message" "$invalid_data" "Request con datos vacíos (debe fallar)"
    
    # Test 10: Endpoint inexistente
    make_request "GET" "$BOT_URL/endpoint-inexistente" "" "Endpoint inexistente (debe fallar)"
    
    echo "📊 RESUMEN DE TESTING"
    echo "=" * 60
    echo "✅ Testing completado"
    echo "🤖 Bot Status: Funcionando"
    echo "🌐 API Gateway Status: $(if [[ "$api_gateway_running" == true ]]; then echo "Funcionando"; else echo "No disponible"; fi)"
    echo ""
    echo "💡 PRÓXIMOS PASOS:"
    echo "   1. Verifica los logs del bot para detalles"
    echo "   2. Si hay errores, revisa la configuración en .environment"
    echo "   3. Asegúrate de que PostgreSQL esté corriendo"
    echo "   4. Para testing real, configura un número de teléfono válido en Twilio"
    echo ""
    echo "📝 COMANDOS ÚTILES:"
    echo "   • Ver logs: tail -f bot.log"
    echo "   • Restart bot: Ctrl+C && python main.py"
    echo "   • Check PostgreSQL: pg_isready"
}

# Ejecutar testing
main "$@" 