#!/usr/bin/env python3
"""
Startup script for Back4App deployment
Coordinates all ISO Standards Games servers
"""

import os
import sys
import asyncio
import threading
import time
from pathlib import Path

# Añadir el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

def start_main_server():
    """Iniciar el servidor principal (llm_game_server.py)"""
    try:
        print("🚀 Starting main ISO Standards Games server...")
        
        # Importar y ejecutar el servidor principal
        exec(open('llm_game_server.py').read())
        
    except Exception as e:
        print(f"❌ Error starting main server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def check_health():
    """Verificar que el servidor esté funcionando"""
    import time
    import requests
    
    port = int(os.environ.get('PORT', 8000))
    health_url = f"http://localhost:{port}/"
    
    for attempt in range(10):  # 10 intentos
        try:
            time.sleep(2)  # Esperar 2 segundos
            response = requests.get(health_url, timeout=5)
            if response.status_code == 200:
                print(f"✅ Server is healthy at port {port}")
                return True
        except Exception as e:
            print(f"⏳ Health check attempt {attempt + 1}/10 failed: {e}")
    
    print("❌ Server health check failed")
    return False

def main():
    """Función principal para Back4App"""
    print("🎮 ISO Standards Games - Back4App Startup")
    print("=" * 50)
    
    # Variables de entorno
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    
    print(f"📊 Configuration:")
    print(f"  Port: {port}")
    print(f"  Debug: {debug}")
    print(f"  Python: {sys.version}")
    print(f"  Working directory: {os.getcwd()}")
    
    # Verificar archivos importantes
    required_files = [
        'llm_game_server.py',
        'quality_scenarios_db.py',
        'requirements_scenarios_db.py',
        'usability_scenarios_db.py'
    ]
    
    print(f"\n🔍 Checking required files:")
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file}")
    
    # Iniciar el servidor principal
    print(f"\n🚀 Starting main server on port {port}...")
    start_main_server()

if __name__ == "__main__":
    main()