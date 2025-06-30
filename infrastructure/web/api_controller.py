"""
Controlador Web API REST para el bot de WhatsApp
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Any

from config.settings import AppConfig
from infrastructure.persistence.postgresql_client_repository import PostgreSQLClientRepository
from infrastructure.external_services.twilio_service import TwilioWhatsAppService
from application.use_cases.add_client_use_case import AddClientUseCase
from application.use_cases.send_massive_campaign_use_case import SendMassiveCampaignUseCase


class WhatsAppBotAPI:
    """
    Controlador principal de la API REST del bot de WhatsApp
    """
    
    def __init__(self, config: AppConfig):
        self.config = config
        self.app = Flask(__name__)
        CORS(self.app)
        
        # Inicializar dependencias
        self.client_repository = PostgreSQLClientRepository(config.database.url)
        self.twilio_service = TwilioWhatsAppService(config.twilio)
        
        # Inicializar casos de uso
        self.add_client_use_case = AddClientUseCase(self.client_repository)
        self.send_campaign_use_case = SendMassiveCampaignUseCase(
            self.client_repository, 
            self.twilio_service
        )
        
        # Registrar rutas
        self._register_routes()
    
    def _register_routes(self):
        """Registra todas las rutas de la API"""
        
        @self.app.route('/', methods=['GET'])
        def home():
            """Página principal con interfaz interactiva"""
            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>🤖 Bot WhatsApp - Alesse Connect</title>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                    body {{ 
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        min-height: 100vh;
                    }}
                    .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
                    .header {{ 
                        text-align: center; 
                        background: rgba(37, 211, 102, 0.9); 
                        color: white; 
                        padding: 30px; 
                        border-radius: 15px; 
                        margin-bottom: 30px;
                        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    }}
                    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; }}
                    .card {{ 
                        background: rgba(255, 255, 255, 0.95); 
                        padding: 25px; 
                        border-radius: 15px; 
                        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
                        backdrop-filter: blur(10px);
                    }}
                    .status {{ 
                        display: inline-block; 
                        padding: 8px 15px; 
                        border-radius: 20px; 
                        margin: 5px;
                        font-size: 14px;
                        font-weight: 600;
                    }}
                    .success {{ background: #d4edda; color: #155724; }}
                    .info {{ background: #d1ecf1; color: #0c5460; }}
                    .warning {{ background: #fff3cd; color: #856404; }}
                    .form-group {{ margin-bottom: 20px; }}
                    .form-label {{ 
                        display: block; 
                        margin-bottom: 8px; 
                        font-weight: 600;
                        color: #333;
                    }}
                    .form-input {{ 
                        width: 100%; 
                        padding: 12px; 
                        border: 2px solid #e1e5e9; 
                        border-radius: 8px; 
                        font-size: 16px;
                        transition: border-color 0.3s;
                    }}
                    .form-input:focus {{ border-color: #25D366; outline: none; }}
                    .btn {{ 
                        background: #25D366; 
                        color: white; 
                        padding: 12px 25px; 
                        border: none; 
                        border-radius: 8px; 
                        cursor: pointer; 
                        font-size: 16px;
                        font-weight: 600;
                        transition: all 0.3s;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                    }}
                    .btn:hover {{ background: #128C7E; transform: translateY(-2px); }}
                    .btn:disabled {{ background: #ccc; cursor: not-allowed; transform: none; }}
                    .btn-danger {{ background: #dc3545; }}
                    .btn-danger:hover {{ background: #c82333; }}
                    .alert {{ 
                        padding: 15px; 
                        margin: 15px 0; 
                        border-radius: 8px; 
                        display: none;
                    }}
                    .alert-success {{ background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }}
                    .alert-error {{ background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }}
                    .stats {{ 
                        display: grid; 
                        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); 
                        gap: 15px; 
                        margin: 20px 0;
                    }}
                    .stat-item {{ 
                        text-align: center; 
                        padding: 15px; 
                        background: rgba(37, 211, 102, 0.1); 
                        border-radius: 10px;
                    }}
                    .stat-number {{ font-size: 24px; font-weight: bold; color: #25D366; }}
                    .stat-label {{ font-size: 12px; color: #666; margin-top: 5px; }}
                    .template-item {{ 
                        background: #f8f9fa; 
                        padding: 15px; 
                        margin: 10px 0; 
                        border-radius: 8px; 
                        border-left: 4px solid #25D366;
                    }}
                    .loading {{ display: none; }}
                    h2 {{ color: #333; margin-bottom: 20px; display: flex; align-items: center; }}
                    h2::before {{ content: attr(data-emoji); margin-right: 10px; font-size: 1.2em; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🤖 Bot de WhatsApp - Alesse Connect</h1>
                        <p>Sistema de Envío Masivo con Domain-Driven Design</p>
                    </div>
                    
                    <div class="card">
                        <h2 data-emoji="📊">Estado del Sistema</h2>
                        <div id="systemStatus">
                            <div class="loading">⏳ Cargando estado...</div>
                        </div>
                        <div class="stats" id="systemStats"></div>
                    </div>
                    
                    <div class="grid">
                        <div class="card">
                            <h2 data-emoji="👥">Agregar Cliente</h2>
                            <form id="addClientForm">
                                <div class="form-group">
                                    <label class="form-label">Nombre Completo *</label>
                                    <input type="text" class="form-input" id="clientName" required>
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Teléfono (con código país) *</label>
                                    <input type="tel" class="form-input" id="clientPhone" placeholder="+51999123456" required>
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Email (opcional)</label>
                                    <input type="email" class="form-input" id="clientEmail">
                                </div>
                                <button type="submit" class="btn">Agregar Cliente</button>
                            </form>
                            <div id="clientAlert" class="alert"></div>
                        </div>
                        
                        <div class="card">
                            <h2 data-emoji="🚀">Enviar Campaña Masiva</h2>
                            <div id="templatesContainer">
                                <div class="loading">⏳ Cargando templates...</div>
                            </div>
                            <form id="campaignForm" style="display: none;">
                                <div class="form-group">
                                    <label class="form-label">Seleccionar Template</label>
                                    <select class="form-input" id="templateSelect" required>
                                        <option value="">-- Selecciona un template --</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Retraso entre mensajes (segundos)</label>
                                    <input type="number" class="form-input" id="delaySeconds" value="3" min="1" max="10">
                                </div>
                                <button type="submit" class="btn btn-danger" id="sendCampaignBtn">
                                    🚀 ENVIAR CAMPAÑA MASIVA
                                </button>
                            </form>
                            <div id="campaignAlert" class="alert"></div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h2 data-emoji="📋">Clientes Activos</h2>
                        <div id="clientsList">
                            <div class="loading">⏳ Cargando clientes...</div>
                        </div>
                    </div>
                </div>
                
                <script>
                    // Función para mostrar alertas
                    function showAlert(containerId, message, isSuccess = true) {{
                        const alert = document.getElementById(containerId);
                        alert.className = isSuccess ? 'alert alert-success' : 'alert alert-error';
                        alert.textContent = message;
                        alert.style.display = 'block';
                        setTimeout(() => alert.style.display = 'none', 5000);
                    }}
                    
                    // Cargar estado del sistema
                    async function loadSystemStatus() {{
                        try {{
                            const response = await fetch('/api/status');
                            const data = await response.json();
                            
                            const statusDiv = document.getElementById('systemStatus');
                            const statsDiv = document.getElementById('systemStats');
                            
                            if (data.success) {{
                                statusDiv.innerHTML = `
                                    <span class="status success">✅ API Funcionando</span>
                                    <span class="status info">🗄️ PostgreSQL Conectado</span>
                                    <span class="status ${{data.services.twilio.status === 'ok' ? 'success' : 'warning'}}">
                                        📱 Twilio: ${{data.services.twilio.message}}
                                    </span>
                                `;
                                
                                statsDiv.innerHTML = `
                                    <div class="stat-item">
                                        <div class="stat-number">${{data.stats.active_clients}}</div>
                                        <div class="stat-label">Clientes Activos</div>
                                    </div>
                                `;
                            }}
                        }} catch (error) {{
                            document.getElementById('systemStatus').innerHTML = 
                                '<span class="status warning">⚠️ Error al cargar estado</span>';
                        }}
                    }}
                    
                    // Cargar templates disponibles
                    async function loadTemplates() {{
                        try {{
                            const response = await fetch('/api/templates');
                            const data = await response.json();
                            
                            const container = document.getElementById('templatesContainer');
                            const select = document.getElementById('templateSelect');
                            
                            if (data.success && data.data.length > 0) {{
                                container.innerHTML = data.data.map(template => `
                                    <div class="template-item">
                                        <strong>${{template.name}}</strong><br>
                                        <small>${{template.description || 'Sin descripción'}}</small>
                                    </div>
                                `).join('');
                                
                                select.innerHTML = '<option value="">-- Selecciona un template --</option>' +
                                    data.data.map(template => 
                                        `<option value="${{template.key}}">${{template.name}}</option>`
                                    ).join('');
                                
                                document.getElementById('campaignForm').style.display = 'block';
                            }} else {{
                                container.innerHTML = '<p>⚠️ No hay templates disponibles</p>';
                            }}
                        }} catch (error) {{
                            document.getElementById('templatesContainer').innerHTML = 
                                '<p>❌ Error al cargar templates</p>';
                        }}
                    }}
                    
                    // Cargar lista de clientes
                    async function loadClients() {{
                        try {{
                            const response = await fetch('/api/clients');
                            const data = await response.json();
                            
                            const container = document.getElementById('clientsList');
                            
                            if (data.success && data.data.length > 0) {{
                                container.innerHTML = `
                                    <p><strong>Total: ${{data.total}} clientes</strong></p>
                                    <div style="max-height: 300px; overflow-y: auto;">
                                        ${{data.data.map(client => `
                                            <div class="template-item" style="border-left-color: #007bff;">
                                                <strong>${{client.nombre}}</strong> - ${{client.telefono}}<br>
                                                <small>
                                                    📧 ${{client.email || 'Sin email'}} | 
                                                    📊 ${{client.total_enviados}} mensajes enviados
                                                    ${{client.ultimo_envio ? ' | 🕒 Último: ' + new Date(client.ultimo_envio).toLocaleDateString() : ''}}
                                                </small>
                                            </div>
                                        `).join('')}}
                                    </div>
                                `;
                            }} else {{
                                container.innerHTML = '<p>📭 No hay clientes registrados</p>';
                            }}
                        }} catch (error) {{
                            document.getElementById('clientsList').innerHTML = 
                                '<p>❌ Error al cargar clientes</p>';
                        }}
                    }}
                    
                    // Agregar cliente
                    document.getElementById('addClientForm').addEventListener('submit', async (e) => {{
                        e.preventDefault();
                        
                        const name = document.getElementById('clientName').value;
                        const phone = document.getElementById('clientPhone').value;
                        const email = document.getElementById('clientEmail').value;
                        
                        try {{
                            const response = await fetch('/api/clients', {{
                                method: 'POST',
                                headers: {{ 'Content-Type': 'application/json' }},
                                body: JSON.stringify({{ nombre: name, telefono: phone, email: email }})
                            }});
                            
                            const data = await response.json();
                            
                            if (data.success) {{
                                showAlert('clientAlert', '✅ Cliente agregado exitosamente');
                                document.getElementById('addClientForm').reset();
                                loadClients();
                                loadSystemStatus();
                            }} else {{
                                showAlert('clientAlert', '❌ ' + data.message, false);
                            }}
                        }} catch (error) {{
                            showAlert('clientAlert', '❌ Error de conexión', false);
                        }}
                    }});
                    
                    // Enviar campaña masiva
                    document.getElementById('campaignForm').addEventListener('submit', async (e) => {{
                        e.preventDefault();
                        
                        const templateKey = document.getElementById('templateSelect').value;
                        const delaySeconds = parseInt(document.getElementById('delaySeconds').value);
                        const btn = document.getElementById('sendCampaignBtn');
                        
                        if (!confirm('¿Estás seguro de enviar la campaña masiva a todos los clientes activos?')) {{
                            return;
                        }}
                        
                        btn.disabled = true;
                        btn.textContent = '⏳ Enviando...';
                        
                        try {{
                            const response = await fetch('/api/campaigns', {{
                                method: 'POST',
                                headers: {{ 'Content-Type': 'application/json' }},
                                body: JSON.stringify({{ template_key: templateKey, delay_seconds: delaySeconds }})
                            }});
                            
                            const data = await response.json();
                            
                            if (data.success) {{
                                showAlert('campaignAlert', `✅ ${{data.message || 'Campaña enviada exitosamente'}}`);
                                loadClients();
                                loadSystemStatus();
                            }} else {{
                                showAlert('campaignAlert', '❌ ' + data.message, false);
                            }}
                        }} catch (error) {{
                            showAlert('campaignAlert', '❌ Error de conexión', false);
                        }} finally {{
                            btn.disabled = false;
                            btn.textContent = '🚀 ENVIAR CAMPAÑA MASIVA';
                        }}
                    }});
                    
                    // Cargar datos al inicio
                    document.addEventListener('DOMContentLoaded', () => {{
                        loadSystemStatus();
                        loadTemplates();
                        loadClients();
                        
                        // Actualizar cada 30 segundos
                        setInterval(() => {{
                            loadSystemStatus();
                            loadClients();
                        }}, 30000);
                    }});
                </script>
            </body>
            </html>
            """.format(webhook_url=self.config.web.webhook_url or "http://localhost:5000")
        
        @self.app.route('/api/status', methods=['GET'])
        def api_status():
            """Estado de la API"""
            try:
                # Verificar conexión Twilio
                twilio_ok, twilio_msg = self.twilio_service.test_connection()
                
                # Contar clientes activos
                active_clients = self.client_repository.count_active()
                
                return jsonify({
                    'success': True,
                    'status': 'operational',
                    'services': {
                        'api': {'status': 'ok', 'message': 'API funcionando correctamente'},
                        'database': {'status': 'ok', 'message': f'{active_clients} clientes activos'},
                        'twilio': {'status': 'ok' if twilio_ok else 'error', 'message': twilio_msg}
                    },
                    'stats': {
                        'active_clients': active_clients
                    }
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'status': 'error',
                    'message': str(e)
                }), 500
        
        @self.app.route('/api/clients', methods=['GET'])
        def get_clients():
            """Obtener lista de clientes activos"""
            try:
                clients = self.client_repository.find_all_active()
                
                return jsonify({
                    'success': True,
                    'data': [
                        {
                            'id': client.id,
                            'nombre': client.nombre,
                            'telefono': client.telefono,
                            'email': client.email,
                            'total_enviados': client.total_enviados,
                            'ultimo_envio': client.ultimo_envio.isoformat() if client.ultimo_envio else None,
                            'fecha_registro': client.fecha_registro.isoformat() if client.fecha_registro else None
                        }
                        for client in clients
                    ],
                    'total': len(clients)
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': str(e)
                }), 500
        
        @self.app.route('/api/clients', methods=['POST'])
        def add_client():
            """Agregar nuevo cliente"""
            try:
                data = request.get_json()
                
                if not data:
                    return jsonify({
                        'success': False,
                        'message': 'No se proporcionaron datos'
                    }), 400
                
                nombre = data.get('nombre')
                telefono = data.get('telefono')
                email = data.get('email')
                
                if not nombre or not telefono:
                    return jsonify({
                        'success': False,
                        'message': 'Nombre y teléfono son requeridos'
                    }), 400
                
                # Ejecutar caso de uso
                result = self.add_client_use_case.execute(nombre, telefono, email)
                
                status_code = 200 if result['success'] else 400
                return jsonify(result), status_code
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': f'Error interno: {str(e)}'
                }), 500
        
        @self.app.route('/api/templates', methods=['GET'])
        def get_templates():
            """Obtener templates disponibles"""
            try:
                templates = self.send_campaign_use_case.get_available_templates()
                
                return jsonify({
                    'success': True,
                    'data': templates,
                    'total': len(templates)
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': str(e)
                }), 500
        
        @self.app.route('/api/campaigns', methods=['POST'])
        def send_campaign():
            """Enviar campaña masiva"""
            try:
                data = request.get_json()
                
                if not data:
                    return jsonify({
                        'success': False,
                        'message': 'No se proporcionaron datos'
                    }), 400
                
                template_key = data.get('template_key')
                delay_seconds = data.get('delay_seconds', 3)
                
                if not template_key:
                    return jsonify({
                        'success': False,
                        'message': 'template_key es requerido'
                    }), 400
                
                # Ejecutar caso de uso
                result = self.send_campaign_use_case.execute(template_key, delay_seconds)
                
                status_code = 200 if result['success'] else 400
                return jsonify(result), status_code
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': f'Error interno: {str(e)}'
                }), 500
        
        @self.app.route('/whatsapp/webhook', methods=['POST'])
        def whatsapp_webhook():
            """Webhook para recibir mensajes de WhatsApp"""
            try:
                # Aquí se procesarían los mensajes entrantes
                # Por ahora solo confirmamos recepción
                return jsonify({
                    'success': True,
                    'message': 'Webhook recibido'
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': str(e)
                }), 500
    
    def run(self):
        """Ejecuta el servidor Flask"""
        self.app.run(
            host='0.0.0.0',
            port=self.config.web.port,
            debug=self.config.web.debug
        ) 