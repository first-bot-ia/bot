#!/usr/bin/env python3
"""
🌐 Interfaz Web para Bot de Spam Masivo
Sistema de gestión completo para envío de templates
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
from spam_bot_service import spam_service

app = Flask(__name__)
CORS(app)

# Template HTML para la interfaz web
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Bot de Spam Masivo - Alesse Connect</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #ff6b6b, #ffa726);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .tabs {
            display: flex;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
        }
        
        .tab {
            flex: 1;
            padding: 15px;
            background: #f8f9fa;
            border: none;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .tab.active {
            background: white;
            border-bottom: 3px solid #ff6b6b;
            color: #ff6b6b;
        }
        
        .tab:hover:not(.active) {
            background: #e9ecef;
        }
        
        .tab-content {
            display: none;
            padding: 30px;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .card {
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .card h3 {
            color: #495057;
            margin-bottom: 15px;
            font-size: 1.3rem;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #495057;
        }
        
        .form-control {
            width: 100%;
            padding: 12px;
            border: 2px solid #dee2e6;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s ease;
        }
        
        .form-control:focus {
            outline: none;
            border-color: #ff6b6b;
            box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.1);
        }
        
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-right: 10px;
            margin-bottom: 10px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #ff6b6b, #ffa726);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(255, 107, 107, 0.3);
        }
        
        .btn-danger {
            background: linear-gradient(135deg, #e74c3c, #c0392b);
            color: white;
        }
        
        .btn-success {
            background: linear-gradient(135deg, #2ecc71, #27ae60);
            color: white;
        }
        
        .btn-info {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 0.9rem;
            opacity: 0.9;
        }
        
        .progress-bar {
            width: 100%;
            height: 20px;
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(135deg, #2ecc71, #27ae60);
            transition: width 0.3s ease;
        }
        
        .table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        .table th,
        .table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #dee2e6;
        }
        
        .table th {
            background: #f8f9fa;
            font-weight: 600;
            color: #495057;
        }
        
        .badge {
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        .badge-success {
            background: #d4edda;
            color: #155724;
        }
        
        .badge-danger {
            background: #f8d7da;
            color: #721c24;
        }
        
        .template-preview {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 15px;
            margin-top: 10px;
            font-style: italic;
        }
        
        .log {
            background: #212529;
            color: #28a745;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            height: 300px;
            overflow-y: auto;
            margin-top: 20px;
        }
        
        .alert {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .alert-danger {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .alert-info {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        
        .sending-indicator {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #ff6b6b;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .responsive-table {
            overflow-x: auto;
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            .tabs {
                flex-direction: column;
            }
            
            .container {
                margin: 10px;
                border-radius: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Bot de Spam Masivo</h1>
            <p>Sistema de envío masivo de templates para Alesse Connect</p>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="showTab('dashboard')">📊 Dashboard</button>
            <button class="tab" onclick="showTab('clientes')">👥 Clientes</button>
            <button class="tab" onclick="showTab('templates')">📝 Templates</button>
            <button class="tab" onclick="showTab('envios')">🚀 Enviar Spam</button>
            <button class="tab" onclick="showTab('historial')">📈 Historial</button>
        </div>
        
        <!-- Dashboard -->
        <div id="dashboard" class="tab-content active">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value" id="total-clientes">0</div>
                    <div class="stat-label">Total Clientes</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="total-templates">0</div>
                    <div class="stat-label">Templates Activos</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="enviados-hoy">0</div>
                    <div class="stat-label">Enviados Hoy</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="exito-rate">0%</div>
                    <div class="stat-label">Tasa de Éxito</div>
                </div>
            </div>
            
            <div class="card">
                <h3>🔧 Test de Conexión</h3>
                <button class="btn btn-info" onclick="testConnection()">Probar Conexión Twilio</button>
                <div id="connection-result"></div>
            </div>
            
            <div class="card">
                <h3>📊 Estado del Envío Actual</h3>
                <div id="current-stats"></div>
                <div class="progress-bar">
                    <div class="progress-fill" id="progress-fill" style="width: 0%"></div>
                </div>
                <button class="btn btn-danger" onclick="cancelSending()" id="cancel-btn" style="display: none;">Cancelar Envío</button>
            </div>
        </div>
        
        <!-- Clientes -->
        <div id="clientes" class="tab-content">
            <div class="card">
                <h3>➕ Agregar Cliente</h3>
                <form id="add-client-form">
                    <div class="form-group">
                        <label>Nombre Completo</label>
                        <input type="text" class="form-control" name="nombre" required>
                    </div>
                    <div class="form-group">
                        <label>Teléfono (formato: +51999123456)</label>
                        <input type="tel" class="form-control" name="telefono" required>
                    </div>
                    <div class="form-group">
                        <label>Email (opcional)</label>
                        <input type="email" class="form-control" name="email">
                    </div>
                    <button type="submit" class="btn btn-primary">Agregar Cliente</button>
                </form>
            </div>
            
            <div class="card">
                <h3>👥 Lista de Clientes</h3>
                <button class="btn btn-info" onclick="loadClients()">Recargar Lista</button>
                <div class="responsive-table">
                    <table class="table" id="clients-table">
                        <thead>
                            <tr>
                                <th>Nombre</th>
                                <th>Teléfono</th>
                                <th>Email</th>
                                <th>Total Enviados</th>
                                <th>Último Envío</th>
                            </tr>
                        </thead>
                        <tbody id="clients-tbody">
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <!-- Templates -->
        <div id="templates" class="tab-content">
            <div class="card">
                <h3>➕ Crear Template</h3>
                <form id="add-template-form">
                    <div class="form-group">
                        <label>Nombre del Template</label>
                        <input type="text" class="form-control" name="nombre" required>
                    </div>
                    <div class="form-group">
                        <label>Contenido del Mensaje</label>
                        <textarea class="form-control" name="contenido" rows="4" required 
                                  placeholder="Usa {nombre} para personalizar con el nombre del cliente"></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">Crear Template</button>
                </form>
                
                <div class="template-preview" id="template-preview">
                    Ejemplo: ¡Hola Juan! Tu SOAT está por vencer...
                </div>
            </div>
            
            <div class="card">
                <h3>📝 Templates Disponibles</h3>
                <button class="btn btn-info" onclick="loadTemplates()">Recargar Templates</button>
                <div id="templates-list"></div>
            </div>
        </div>
        
        <!-- Envíos -->
        <div id="envios" class="tab-content">
            <div class="card">
                <h3>🚀 Envío Masivo</h3>
                <form id="send-spam-form">
                    <div class="form-group">
                        <label>Seleccionar Template</label>
                        <select class="form-control" name="template" id="template-select" required>
                            <option value="">-- Selecciona un template --</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Delay Mínimo entre Envíos (segundos)</label>
                        <input type="number" class="form-control" name="delay_min" value="5" min="1" max="60">
                    </div>
                    <div class="form-group">
                        <label>Delay Máximo entre Envíos (segundos)</label>
                        <input type="number" class="form-control" name="delay_max" value="15" min="1" max="120">
                    </div>
                    <button type="submit" class="btn btn-primary">🚀 Iniciar Envío Masivo</button>
                </form>
                
                <div class="sending-indicator" id="sending-indicator">
                    <div class="spinner"></div>
                    <p>Enviando mensajes... Por favor espera</p>
                </div>
            </div>
            
            <div class="card">
                <h3>📊 Progreso del Envío</h3>
                <div id="sending-progress"></div>
            </div>
        </div>
        
        <!-- Historial -->
        <div id="historial" class="tab-content">
            <div class="card">
                <h3>📈 Historial de Envíos</h3>
                <button class="btn btn-info" onclick="loadHistory()">Recargar Historial</button>
                <div class="responsive-table">
                    <table class="table" id="history-table">
                        <thead>
                            <tr>
                                <th>Cliente</th>
                                <th>Template</th>
                                <th>Estado</th>
                                <th>Fecha</th>
                                <th>Mensaje</th>
                            </tr>
                        </thead>
                        <tbody id="history-tbody">
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Variables globales
        let progressInterval;
        
        // Funciones de navegación
        function showTab(tabName) {
            // Ocultar todas las pestañas
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.remove('active'));
            
            const tabs = document.querySelectorAll('.tab');
            tabs.forEach(tab => tab.classList.remove('active'));
            
            // Mostrar la pestaña seleccionada
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
            
            // Cargar datos según la pestaña
            if (tabName === 'dashboard') {
                loadDashboard();
            } else if (tabName === 'clientes') {
                loadClients();
            } else if (tabName === 'templates') {
                loadTemplates();
                loadTemplateOptions();
            } else if (tabName === 'envios') {
                loadTemplateOptions();
            } else if (tabName === 'historial') {
                loadHistory();
            }
        }
        
        // Funciones de API
        async function apiCall(endpoint, method = 'GET', data = null) {
            const options = {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                }
            };
            
            if (data) {
                options.body = JSON.stringify(data);
            }
            
            try {
                const response = await fetch(endpoint, options);
                return await response.json();
            } catch (error) {
                console.error('Error en API:', error);
                return { success: false, error: error.message };
            }
        }
        
        // Dashboard
        async function loadDashboard() {
            const stats = await apiCall('/api/stats');
            if (stats.success) {
                document.getElementById('total-clientes').textContent = stats.total_clientes;
                document.getElementById('total-templates').textContent = stats.total_templates;
                document.getElementById('enviados-hoy').textContent = stats.enviados_hoy;
                document.getElementById('exito-rate').textContent = stats.tasa_exito + '%';
            }
            
            // Cargar estado actual
            loadCurrentStats();
        }
        
        async function loadCurrentStats() {
            const stats = await apiCall('/api/current-stats');
            const container = document.getElementById('current-stats');
            const progressFill = document.getElementById('progress-fill');
            const cancelBtn = document.getElementById('cancel-btn');
            
            if (stats.en_progreso) {
                const progress = stats.total > 0 ? ((stats.enviados + stats.fallidos) / stats.total) * 100 : 0;
                progressFill.style.width = progress + '%';
                
                container.innerHTML = `
                    <div class="alert alert-info">
                        <strong>Envío en progreso:</strong> ${stats.template}<br>
                        Progreso: ${stats.enviados + stats.fallidos}/${stats.total} 
                        (${stats.enviados} exitosos, ${stats.fallidos} fallidos)<br>
                        Duración: ${stats.duracion_formateada || '0:00:00'}
                    </div>
                `;
                cancelBtn.style.display = 'inline-block';
                
                // Actualizar cada 2 segundos
                if (!progressInterval) {
                    progressInterval = setInterval(loadCurrentStats, 2000);
                }
            } else {
                if (stats.fin) {
                    container.innerHTML = `
                        <div class="alert alert-success">
                            <strong>Último envío completado:</strong> ${stats.template}<br>
                            Total: ${stats.total} | Exitosos: ${stats.enviados} | Fallidos: ${stats.fallidos}<br>
                            Duración: ${stats.duracion_formateada || '0:00:00'}
                        </div>
                    `;
                    progressFill.style.width = '100%';
                } else {
                    container.innerHTML = '<p>No hay envíos en progreso</p>';
                    progressFill.style.width = '0%';
                }
                cancelBtn.style.display = 'none';
                
                // Limpiar intervalo
                if (progressInterval) {
                    clearInterval(progressInterval);
                    progressInterval = null;
                }
            }
        }
        
        async function testConnection() {
            const result = await apiCall('/api/test-connection');
            const container = document.getElementById('connection-result');
            
            if (result.success) {
                container.innerHTML = `
                    <div class="alert alert-success">
                        <strong>✅ Conexión exitosa</strong><br>
                        Cuenta: ${result.account_name}<br>
                        SID: ${result.account_sid}<br>
                        WhatsApp: ${result.whatsapp_number}
                    </div>
                `;
            } else {
                container.innerHTML = `
                    <div class="alert alert-danger">
                        <strong>❌ Error de conexión</strong><br>
                        ${result.message}
                    </div>
                `;
            }
        }
        
        async function cancelSending() {
            const result = await apiCall('/api/cancel-sending', 'POST');
            if (result.success) {
                alert('Envío cancelado exitosamente');
                loadCurrentStats();
            } else {
                alert('Error cancelando envío: ' + result.message);
            }
        }
        
        // Clientes
        async function loadClients() {
            const clients = await apiCall('/api/clients');
            const tbody = document.getElementById('clients-tbody');
            
            if (clients.success) {
                tbody.innerHTML = clients.data.map(client => `
                    <tr>
                        <td>${client.nombre}</td>
                        <td>${client.telefono}</td>
                        <td>${client.email || '-'}</td>
                        <td>${client.total_enviados}</td>
                        <td>${client.ultimo_envio || 'Nunca'}</td>
                    </tr>
                `).join('');
            } else {
                tbody.innerHTML = '<tr><td colspan="5">Error cargando clientes</td></tr>';
            }
        }
        
        // Templates
        async function loadTemplates() {
            const templates = await apiCall('/api/templates');
            const container = document.getElementById('templates-list');
            
            if (templates.success) {
                container.innerHTML = templates.data.map(template => `
                    <div class="card">
                        <h4>${template.nombre}</h4>
                        <p>${template.contenido}</p>
                        <small>Creado: ${template.fecha_creacion}</small>
                    </div>
                `).join('');
            }
        }
        
        async function loadTemplateOptions() {
            const templates = await apiCall('/api/templates');
            const select = document.getElementById('template-select');
            
            if (templates.success) {
                select.innerHTML = '<option value="">-- Selecciona un template --</option>' +
                    templates.data.map(template => 
                        `<option value="${template.nombre}">${template.nombre}</option>`
                    ).join('');
            }
        }
        
        // Historial
        async function loadHistory() {
            const history = await apiCall('/api/history');
            const tbody = document.getElementById('history-tbody');
            
            if (history.success) {
                tbody.innerHTML = history.data.map(item => `
                    <tr>
                        <td>${item.cliente}</td>
                        <td>${item.template}</td>
                        <td><span class="badge badge-${item.estado === 'enviado' ? 'success' : 'danger'}">${item.estado}</span></td>
                        <td>${item.fecha}</td>
                        <td>${item.mensaje}</td>
                    </tr>
                `).join('');
            }
        }
        
        // Formularios
        document.getElementById('add-client-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            const result = await apiCall('/api/clients', 'POST', data);
            if (result.success) {
                alert('Cliente agregado exitosamente');
                e.target.reset();
                loadClients();
                loadDashboard();
            } else {
                alert('Error: ' + result.message);
            }
        });
        
        document.getElementById('add-template-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            const result = await apiCall('/api/templates', 'POST', data);
            if (result.success) {
                alert('Template creado exitosamente');
                e.target.reset();
                loadTemplates();
                loadTemplateOptions();
                loadDashboard();
            } else {
                alert('Error: ' + result.message);
            }
        });
        
        document.getElementById('send-spam-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            if (!confirm(`¿Estás seguro de iniciar el envío masivo con el template "${data.template}"?`)) {
                return;
            }
            
            document.getElementById('sending-indicator').style.display = 'block';
            
            const result = await apiCall('/api/send-spam', 'POST', data);
            
            document.getElementById('sending-indicator').style.display = 'none';
            
            if (result.success) {
                alert(`Envío iniciado: ${result.message}`);
                showTab('dashboard');
                loadCurrentStats();
            } else {
                alert('Error: ' + result.message);
            }
        });
        
        // Preview de template
        document.querySelector('textarea[name="contenido"]').addEventListener('input', (e) => {
            const preview = document.getElementById('template-preview');
            const content = e.target.value || 'Escribe tu mensaje aquí...';
            preview.textContent = content.replace('{nombre}', 'Juan');
        });
        
        // Cargar dashboard al inicio
        document.addEventListener('DOMContentLoaded', () => {
            loadDashboard();
        });
    </script>
</body>
</html>
"""

# API Endpoints

@app.route('/')
def index():
    """Página principal con interfaz web"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Obtener estadísticas generales"""
    try:
        clientes = spam_service.obtener_clientes_activos()
        templates = spam_service.obtener_templates_disponibles()
        historial = spam_service.obtener_historial_envios(limite=100)
        
        # Calcular estadísticas
        enviados_hoy = len([h for h in historial if h.get('fecha', '').startswith('2024')])
        total_enviados = len([h for h in historial if h.get('estado') == 'enviado'])
        total_fallidos = len([h for h in historial if h.get('estado') == 'fallido'])
        
        tasa_exito = 0
        if total_enviados + total_fallidos > 0:
            tasa_exito = round((total_enviados / (total_enviados + total_fallidos)) * 100, 1)
        
        return jsonify({
            'success': True,
            'total_clientes': len(clientes),
            'total_templates': len(templates),
            'enviados_hoy': enviados_hoy,
            'tasa_exito': tasa_exito
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/current-stats', methods=['GET'])
def get_current_stats():
    """Obtener estadísticas del envío actual"""
    try:
        stats = spam_service.obtener_estadisticas()
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/test-connection', methods=['GET'])
def test_connection():
    """Probar conexión con Twilio"""
    try:
        result = spam_service.test_conexion()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

@app.route('/api/cancel-sending', methods=['POST'])
def cancel_sending():
    """Cancelar envío en progreso"""
    try:
        success = spam_service.cancelar_envio()
        return jsonify({
            'success': success,
            'message': 'Envío cancelado' if success else 'No hay envío en progreso'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

@app.route('/api/clients', methods=['GET', 'POST'])
def handle_clients():
    """Gestionar clientes"""
    try:
        if request.method == 'GET':
            clientes = spam_service.obtener_clientes_activos()
            return jsonify({
                'success': True,
                'data': clientes
            })
        
        elif request.method == 'POST':
            data = request.get_json()
            success = spam_service.agregar_cliente(
                nombre=data['nombre'],
                telefono=data['telefono'],
                email=data.get('email')
            )
            
            return jsonify({
                'success': success,
                'message': 'Cliente agregado' if success else 'Error agregando cliente'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/templates', methods=['GET', 'POST'])
def handle_templates():
    """Gestionar templates"""
    try:
        if request.method == 'GET':
            templates = spam_service.obtener_templates_disponibles()
            return jsonify({
                'success': True,
                'data': templates
            })
        
        elif request.method == 'POST':
            data = request.get_json()
            success = spam_service.crear_template(
                nombre=data['nombre'],
                contenido=data['contenido']
            )
            
            return jsonify({
                'success': success,
                'message': 'Template creado' if success else 'Error creando template'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/history', methods=['GET'])
def get_history():
    """Obtener historial de envíos"""
    try:
        historial = spam_service.obtener_historial_envios()
        return jsonify({
            'success': True,
            'data': historial
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/send-spam', methods=['POST'])
def send_spam():
    """Iniciar envío masivo"""
    try:
        data = request.get_json()
        result = spam_service.enviar_spam_masivo(
            template_nombre=data['template'],
            delay_min=int(data.get('delay_min', 5)),
            delay_max=int(data.get('delay_max', 15))
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

if __name__ == '__main__':
    print("🌐 Iniciando servidor web del Bot de Spam...")
    print("📱 Accede a: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001) 