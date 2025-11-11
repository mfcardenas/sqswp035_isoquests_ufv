#!/usr/bin/env python3
"""
Startup script for Back4App deployment
Configures and starts the ISO Standards Games server
"""

import os
import sys
import time
from pathlib import Path

# Añadir el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

def generate_config_js():
    """Generar config.js dinámico para Back4App"""
    port = os.environ.get('PORT', '8000')
    
    config_content = f"""// Configuration for ISO Standards Games - Back4App
const CONFIG = {{
  API: {{
    BASE_URL: '',  // Relative URLs for Back4App
  }},
  DEPLOYMENT: {{
    PLATFORM: 'back4app',
    PORT: {port},
    BASE_URL: window.location.origin
  }}
}};

// Make available globally
if (typeof module !== 'undefined' && module.exports) {{
  module.exports = CONFIG;
}} else {{
  window.CONFIG = CONFIG;
}}
"""
    
    with open('config.js', 'w') as f:
        f.write(config_content)
    
    print(f"✅ Generated config.js for port {port}")

def start_main_server():
    """Iniciar el servidor principal"""
    print("🚀 Starting ISO Standards Games server...")
    
    # Generar configuración dinámica
    generate_config_js()
    
    # Aplicar parches al frontend
    apply_frontend_patches()
    
    # Verificar archivos críticos
    required_files = [
        'llm_game_server.py',
        'quality_scenarios_db.py', 
        'requirements_scenarios_db.py',
        'usability_scenarios_db.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        sys.exit(1)
    
    print("✅ All required files present")
    
    # Importar y ejecutar el servidor principal
    try:
        import subprocess
        result = subprocess.run([sys.executable, 'llm_game_server.py'], 
                              check=True, 
                              capture_output=False)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed with exit code {e.returncode}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

def apply_frontend_patches():
    """Aplicar parches al frontend para Back4App"""
    print("🔧 Applying frontend patches...")
    
    # Parchear requirement-rally.js
    js_file = 'requirement-rally-frontend/requirement-rally.js'
    if os.path.exists(js_file):
        try:
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Reemplazar URL hardcodeada
            old_url = "this.apiUrl = 'http://127.0.0.1:8001';"
            new_url = "this.apiUrl = window.location.origin; // Back4App dynamic"
            
            if old_url in content:
                content = content.replace(old_url, new_url)
                with open(js_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print("✅ Patched requirement-rally.js")
            else:
                print("✅ requirement-rally.js already patched or doesn't need patching")
                
        except Exception as e:
            print(f"⚠️ Could not patch {js_file}: {e}")
    
    print("✅ Frontend patches applied")

def main():
    """Función principal"""
    print("🎮 ISO Standards Games - Back4App Startup")
    print("=" * 50)
    
    port = int(os.environ.get('PORT', 8000))
    print(f"📊 Port: {port}")
    print(f"🐍 Python: {sys.version}")
    print(f"� Directory: {os.getcwd()}")
    
    start_main_server()

if __name__ == "__main__":
    main()