#!/usr/bin/env python3
"""
🔄 Script para actualizar token rápidamente
Cuando el panel se resetee, ejecuta este script
"""

import os

def update_token():
    """Actualiza el token en el archivo"""
    
    print("🔄 Actualizador de Token WhatsApp")
    print("=" * 40)
    
    print("Cuando tu token se resetee:")
    print("1. Copia el nuevo token del panel Meta")
    print("2. Pégalo aquí abajo")
    print("3. El script actualizará automáticamente el código")
    
    new_token = input("\n📝 Pega tu nuevo token aquí: ").strip()
    
    if len(new_token) < 50:
        print("❌ Token parece incorrecto (muy corto)")
        return False
    
    # Leer archivo actual
    with open('whatsapp_native_service.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar y reemplazar token
    if 'self.access_token = "' in content:
        # Encontrar la línea del token
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'self.access_token = "' in line:
                # Reemplazar con nuevo token
                lines[i] = f'        self.access_token = "{new_token}"'
                break
        
        # Guardar archivo actualizado
        with open('whatsapp_native_service.py', 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"✅ Token actualizado exitosamente!")
        print(f"🔑 Nuevos últimos 10 caracteres: ...{new_token[-10:]}")
        
        # Probar nuevo token
        print("\n🧪 Probando nuevo token...")
        os.system("python test_new_token.py")
        
        return True
    else:
        print("❌ No se pudo encontrar la línea del token")
        return False

if __name__ == "__main__":
    update_token() 