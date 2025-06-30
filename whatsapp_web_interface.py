#!/usr/bin/env python3
"""
🌐 Interfaz Web para WhatsApp Native Service
"""

from flask import Flask, render_template_string, request, jsonify
from whatsapp_native_service import whatsapp_native_service
import threading
import time

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>🚀 WhatsApp Native Bot</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
        .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .info { background: #cce6ff; color: #004085; border: 1px solid #99ccff; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
        input, select { padding: 8px; margin: 5px; border: 1px solid #ddd; border-radius: 4px; }
        .log { background: #f8f9fa; padding: 10px; margin: 10px 0; border-radius: 5px; font-family: monospace; max-height: 300px; overflow-y: auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 WhatsApp Native Bot - Bot de Spam</h1>
        
        <!-- Estado de conexión -->
        <div id="connection-status" class="status info">
            🔄 Verificando conexión...
        </div>
        
        <!-- Envío de mensajes -->
        <h3>📱 Enviar Mensaje de Prueba</h3>
        <div>
                         <input type="text" id="phone" placeholder="51965181346" value="51965181346">
                         <select id="template">
                 <option value="hello_world">Hello World (sin parámetros)</option>
             </select>
             <input type="text" id="parameter" placeholder="Parámetro (solo si aplica)" value=""  style="display:none;">
            <button onclick="sendMessage()">✉️ Enviar</button>
        </div>
        
        <!-- Resultados -->
        <div id="result" class="status" style="display: none;"></div>
        
        <!-- Logs -->
        <h3>📋 Logs</h3>
        <div id="logs" class="log">Iniciando...</div>
        
        <!-- Clientes -->
        <h3>👥 Clientes Activos</h3>
        <div id="clients"></div>
    </div>

    <script>
        let logs = [];
        
        function addLog(message) {
            logs.push(new Date().toLocaleTimeString() + ': ' + message);
            document.getElementById('logs').innerHTML = logs.slice(-10).join('\\n');
        }
        
        function checkConnection() {
            fetch('/api/test-connection')
                .then(response => response.json())
                .then(data => {
                    const status = document.getElementById('connection-status');
                    if (data.success) {
                        status.className = 'status success';
                        status.innerHTML = '✅ Conectado a WhatsApp Business API';
                    } else {
                        status.className = 'status error';
                        status.innerHTML = '❌ Error: ' + data.message;
                    }
                    addLog('Conexión verificada: ' + data.message);
                });
        }
        
        function sendMessage() {
            const phone = document.getElementById('phone').value;
            const template = document.getElementById('template').value;
            const parameter = document.getElementById('parameter').value;
            
            addLog('Enviando mensaje a ' + phone + '...');
            
            fetch('/api/send-message', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({phone, template, parameter})
            })
            .then(response => response.json())
            .then(data => {
                const result = document.getElementById('result');
                result.style.display = 'block';
                if (data.success) {
                    result.className = 'status success';
                    result.innerHTML = '✅ Mensaje enviado: ' + data.message_id;
                    addLog('✅ Mensaje enviado exitosamente');
                } else {
                    result.className = 'status error';
                    result.innerHTML = '❌ Error: ' + JSON.stringify(data.error);
                    addLog('❌ Error enviando mensaje');
                }
            });
        }
        
        function loadClients() {
            fetch('/api/clients')
                .then(response => response.json())
                .then(data => {
                    const clients = document.getElementById('clients');
                    clients.innerHTML = data.map(c => 
                        '<div>👤 ' + c.nombre + ' - ' + c.telefono + '</div>'
                    ).join('');
                });
        }
        
        // Inicializar
        checkConnection();
        loadClients();
        setInterval(checkConnection, 30000); // Verificar cada 30s
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/test-connection')
def test_connection():
    return jsonify(whatsapp_native_service.test_conexion())

@app.route('/api/send-message', methods=['POST'])
def send_message():
    data = request.json or {}
    phone = data.get('phone', '51965181346')
    template = data.get('template', 'hello_world')
    parameter = data.get('parameter', '')
    
    parameters = [parameter] if parameter and parameter.strip() else None
    result = whatsapp_native_service.send_template_message(phone, template, parameters)
    
    return jsonify(result)

@app.route('/api/clients')
def get_clients():
    return jsonify(whatsapp_native_service.obtener_clientes_activos())

if __name__ == '__main__':
    print("🌐 Iniciando WhatsApp Native Web Interface...")
    print("📱 Accede a: http://localhost:5002")
    app.run(host='0.0.0.0', port=5002, debug=True) 