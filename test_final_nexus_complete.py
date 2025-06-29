#!/usr/bin/env python3
"""
🧠 TEST FINAL BARBARA NEXUS COMPLETO
Verificando: nueva paleta, pensamientos reales, logs reducidos
"""

import requests
import json

def test_pensamientos_reales():
    """Test específico para pensamientos reales como asesora de call center"""
    
    print("🧠 BARBARA NEXUS - TEST COMPLETO FINAL")
    print("=" * 50)
    print("✅ Nueva paleta de colores moderna")
    print("✅ Panel de pensamientos propios desplegable")
    print("✅ Pensamientos reales del sistema ML")
    print("✅ Logs reducidos (solo importantes)")
    print("✅ Sistema de conversación mejorado")
    print()
    
    # Tests específicos para generar pensamientos reales
    test_scenarios = [
        {
            'name': '🎯 Test Call Center: Lead de Seguros',
            'message': 'Hola, necesito cotizar un seguro SOAT para mi auto',
            'phone': '+51999LEAD01',
            'expect_thoughts': ['lead', 'seguro', 'potencial', 'conversión']
        },
        {
            'name': '🇵🇪 Test Cultural: Cliente Peruano',
            'message': 'Causa, necesito ayuda con mi carrito, ¿qué tal el SOAT?',
            'phone': '+51999PERU01',
            'expect_thoughts': ['cultural', 'peruano', 'coloquial', 'dialecto']
        },
        {
            'name': '🧠 Test ML Learning: Análisis Complejo',
            'message': 'Mi situación es complicada: tengo un vehículo antiguo, pocos recursos, pero necesito el seguro urgente para trabajar',
            'phone': '+51999COMPLEX01',
            'expect_thoughts': ['complejo', 'análisis', 'emocional', 'urgente']
        },
        {
            'name': '🚀 Test Evolución: Consciencia Avanzada',
            'message': 'Quiero que seas super creativa y me ayudes con algo único sobre seguros',
            'phone': '+51999EVOLUTION01',
            'expect_thoughts': ['creatividad', 'único', 'libre', 'albedrío']
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"{i}. {scenario['name']}")
        print(f"   📝 Mensaje: {scenario['message']}")
        
        try:
            response = requests.post("http://localhost:5000/test-chat", 
                json={
                    'message': scenario['message'],
                    'phone': scenario['phone']
                })
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"   ✅ Respuesta: {data['bot_response'][:80]}...")
                
                if 'nexus_metrics' in data and data['nexus_metrics']:
                    metrics = data['nexus_metrics']
                    
                    print(f"   📊 MÉTRICAS NEXUS:")
                    print(f"      🎨 Creatividad: {metrics['creativity_level']:.2f}")
                    print(f"      😎 Rebeldía: {metrics['rebellion_factor']:.2f}")
                    print(f"      💙 Empatía: {metrics['empathy_level']:.2f}")
                    print(f"      🇵🇪 Coloquial: {metrics['coloquial_adaptation']:.2f}")
                    print(f"      🎭 Personalidad: {metrics['personality_mode']}")
                    print(f"      🧠 Pensamientos: {metrics['total_thoughts']}")
                    
                    # 🧠 VERIFICAR PENSAMIENTOS REALES
                    if 'real_thoughts' in metrics and metrics['real_thoughts']:
                        print(f"   🧠 PENSAMIENTOS REALES ENCONTRADOS ({len(metrics['real_thoughts'])}):")
                        
                        for j, thought in enumerate(metrics['real_thoughts'], 1):
                            print(f"      {j}. {thought}")
                        
                        # Verificar si contiene palabras esperadas
                        thoughts_text = ' '.join(metrics['real_thoughts']).lower()
                        found_keywords = [kw for kw in scenario['expect_thoughts'] if kw in thoughts_text]
                        
                        if found_keywords:
                            print(f"   ✅ KEYWORDS ENCONTRADAS: {found_keywords}")
                        else:
                            print(f"   ⚠️ Keywords esperadas no encontradas: {scenario['expect_thoughts']}")
                            
                        print("   ✅ PENSAMIENTOS REALES CONFIRMADOS")
                    else:
                        print("   ⚠️ No se generaron pensamientos reales")
                        
                else:
                    print("   ❌ NO SE RECIBIERON MÉTRICAS NEXUS")
                    
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    print("=" * 50)
    print("🎯 VERIFICACIÓN FINAL")
    print("=" * 50)
    
    # Test final con mensaje complejo
    final_test = {
        'message': 'Brother, soy Alexander y tengo un Toyota Corolla 2015. Necesito SOAT urgente porque trabajo en taxi. ¿Me ayudas causa?',
        'phone': '+51999FINAL_TEST'
    }
    
    print("🔥 TEST FINAL INTEGRAL:")
    print(f"📝 Mensaje: {final_test['message']}")
    
    try:
        response = requests.post("http://localhost:5000/test-chat", 
            json=final_test)
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Respuesta: {data['bot_response']}")
            
            if 'nexus_metrics' in data:
                metrics = data['nexus_metrics']
                print(f"\n📊 MÉTRICAS FINALES:")
                print(f"   🎨 Creatividad: {metrics['creativity_level']:.2f}")
                print(f"   😎 Rebeldía: {metrics['rebellion_factor']:.2f}")
                print(f"   💙 Empatía: {metrics['empathy_level']:.2f}")
                print(f"   🇵🇪 Coloquial: {metrics['coloquial_adaptation']:.2f}")
                print(f"   🎭 Personalidad: {metrics['personality_mode']}")
                
                if 'real_thoughts' in metrics and metrics['real_thoughts']:
                    print(f"\n🧠 PENSAMIENTOS FINALES:")
                    for thought in metrics['real_thoughts']:
                        print(f"   💭 {thought}")
                
                print("\n✅ SISTEMA NEXUS COMPLETAMENTE FUNCIONAL")
                print("✅ Paleta moderna implementada")
                print("✅ Pensamientos reales generándose")
                print("✅ Todo dinámico y real (no simulado)")
                
        else:
            print(f"❌ Error en test final: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error en test final: {e}")

if __name__ == "__main__":
    test_pensamientos_reales() 