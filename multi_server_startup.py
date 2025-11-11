#!/usr/bin/env python3
"""
Multi-server startup script for ISO Standards Games
Ejecuta QualityQuest, RequirementRally y UsabilityUniverse en puertos separados
para uso en Back4App donde solo se puede exponer un puerto principal.
"""

import os
import sys
import time
import signal
import subprocess
import re
from threading import Thread
from pathlib import Path

def modify_requirement_rally_port(port=8001):
    """Modifica el puerto en requirement_rally_server.py"""
    file_path = "requirement_rally_server.py"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar: uvicorn.run(app, host="0.0.0.0", port=8002)
        pattern = r'uvicorn\.run\(app,\s*host="[^"]*",\s*port=\d+\)'
        replacement = f'uvicorn.run(app, host="0.0.0.0", port={port})'
        content = re.sub(pattern, replacement, content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ RequirementRally configurado para puerto {port}")
        return True
        
    except Exception as e:
        print(f"✗ Error modificando RequirementRally: {e}")
        return False

def modify_usability_universe_port(port=8003):
    """Modifica el puerto en usability_universe_server.py"""
    file_path = "usability_universe_server.py"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar el bloque uvicorn.run completo
        pattern = r'uvicorn\.run\(\s*app,\s*host="[^"]*",\s*port=\d+,[\s\S]*?\)'
        replacement = f'''uvicorn.run(
        app, 
        host="0.0.0.0", 
        port={port},
        log_level="info",
        reload=False
    )'''
        content = re.sub(pattern, replacement, content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ UsabilityUniverse configurado para puerto {port}")
        return True
        
    except Exception as e:
        print(f"✗ Error modificando UsabilityUniverse: {e}")
        return False

def run_server_with_logging(command, name, port):
    """Ejecuta un servidor en un hilo separado con logging mejorado"""
    try:
        print(f"🚀 Iniciando {name} en puerto {port}")
        
        # Configurar environment
        env = os.environ.copy()
        env['PORT'] = str(port)
        env['PYTHONUNBUFFERED'] = '1'
        
        # Crear el proceso
        process = subprocess.Popen(
            command,
            shell=True,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Combinar stderr con stdout
            universal_newlines=True,
            bufsize=1  # Line buffered
        )
        
        # Log output en tiempo real
        try:
            for line in iter(process.stdout.readline, ''):
                line = line.strip()
                if line:
                    print(f"[{name}] {line}")
                    
        except Exception as e:
            print(f"[{name}] Error leyendo output: {e}")
        
        # Esperar a que termine
        return_code = process.wait()
        print(f"[{name}] Proceso terminado con código {return_code}")
        
    except Exception as e:
        print(f"✗ Error ejecutando {name}: {e}")

def check_port_availability(port):
    """Verifica si un puerto está disponible"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('', port))
            return True
        except OSError:
            return False

def main():
    """Función principal que coordina todos los servidores"""
    print("🎮 ISO Standards Games - Multi-Server Startup v2.0")
    print("=" * 55)
    
    # Verificar que estamos en el directorio correcto
    if not Path("iso_standards_games").exists():
        print("✗ Error: No se encuentra el módulo iso_standards_games")
        print("  Asegúrate de ejecutar este script desde el directorio raíz del proyecto")
        sys.exit(1)
    
    # Configuración de servidores
    servers = [
        {
            'name': 'QualityQuest',
            'command': 'python -m iso_standards_games',
            'port': 8000,
            'modifier': None
        },
        {
            'name': 'RequirementRally',
            'command': 'python requirement_rally_server.py',
            'port': 8001,
            'modifier': modify_requirement_rally_port
        },
        {
            'name': 'UsabilityUniverse', 
            'command': 'python usability_universe_server.py',
            'port': 8003,
            'modifier': modify_usability_universe_port
        }
    ]
    
    # Verificar disponibilidad de puertos
    print("\n🔍 Verificando puertos...")
    for server in servers:
        if not check_port_availability(server['port']):
            print(f"⚠️  Puerto {server['port']} ocupado, {server['name']} podría fallar")
        else:
            print(f"✓ Puerto {server['port']} disponible para {server['name']}")
    
    # Modificar archivos de configuración si es necesario
    print("\n⚙️  Configurando servidores...")
    for server in servers:
        if server['modifier']:
            server['modifier'](server['port'])
    
    # Crear hilos para cada servidor
    print("\n🚀 Iniciando servidores...")
    threads = []
    
    for server in servers:
        thread = Thread(
            target=run_server_with_logging,
            args=(server['command'], server['name'], server['port']),
            daemon=True
        )
        threads.append((thread, server))
        thread.start()
        time.sleep(3)  # Esperar entre arranques
    
    print("\n🌐 Estado de servidores:")
    print("   • QualityQuest:      http://localhost:8000")
    print("   • RequirementRally:  http://localhost:8001") 
    print("   • UsabilityUniverse: http://localhost:8003")
    print("\n⚠️  Presiona Ctrl+C para detener todos los servidores")
    print("📊 Monitoreando servidores...")
    
    # Mantener el script ejecutándose y monitorear threads
    try:
        while True:
            # Verificar que todos los threads siguen activos
            active_servers = []
            for thread, server in threads:
                if thread.is_alive():
                    active_servers.append(server['name'])
            
            if active_servers:
                print(f"\r⚡ Servidores activos: {', '.join(active_servers)}", end="", flush=True)
            else:
                print("\n⚠️  Todos los servidores han terminado")
                break
                
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Recibida señal de interrupción, deteniendo servidores...")
        
    # Cleanup
    print("🧹 Limpiando procesos...")
    for thread, server in threads:
        if thread.is_alive():
            print(f"   Esperando a {server['name']}...")
    
    print("✅ Todos los servidores han sido detenidos correctamente")

if __name__ == "__main__":
    main()