#!/usr/bin/env python3
"""
Script de verificación e inicio para Back4App deployment.
Verifica la configuración y inicia la aplicación.
"""

import os
import sys
from pathlib import Path

def check_environment():
    """Verificar que el entorno esté configurado correctamente."""
    print("🔍 Verificando configuración del entorno...")
    
    # Verificar Python
    python_version = sys.version_info
    if python_version.major != 3 or python_version.minor < 9:
        print(f"❌ Python 3.9+ requerido. Versión actual: {python_version.major}.{python_version.minor}")
        return False
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Verificar estructura de archivos
    required_files = [
        "pyproject.toml",
        "iso_standards_games/__main__.py",
        "iso_standards_games/api/app.py",
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"❌ Archivo requerido no encontrado: {file_path}")
            return False
        print(f"✅ {file_path}")
    
    # Verificar variables de entorno importantes
    env_vars = {
        "PORT": os.environ.get("PORT", "8000"),
        "DEBUG": os.environ.get("DEBUG", "false"),
        "APP_NAME": os.environ.get("APP_NAME", "ISO Standards Games"),
        "LLM_PROVIDER": os.environ.get("LLM_PROVIDER", "ollama"),
    }
    
    print("\n🔧 Variables de entorno:")
    for var, value in env_vars.items():
        print(f"  {var} = {value}")
    
    return True

def check_dependencies():
    """Verificar que las dependencias estén instaladas."""
    print("\n📦 Verificando dependencias...")
    
    required_packages = ["fastapi", "uvicorn", "pydantic"]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Faltan dependencias: {missing_packages}")
        print("💡 Ejecutar: poetry install")
        return False
    
    return True

def create_data_directory():
    """Crear directorio de datos para SQLite si no existe."""
    data_dir = Path("data")
    if not data_dir.exists():
        data_dir.mkdir(exist_ok=True)
        print(f"✅ Directorio de datos creado: {data_dir.absolute()}")
    else:
        print(f"✅ Directorio de datos existe: {data_dir.absolute()}")

def start_application():
    """Iniciar la aplicación."""
    print("\n🚀 Iniciando aplicación ISO Standards Games...")
    
    # Obtener puerto de Back4App o usar 8000 por defecto
    port = int(os.environ.get('PORT', 8000))
    
    print(f"🌐 Puerto configurado: {port}")
    print("📍 Endpoints disponibles:")
    print(f"  - Aplicación principal: http://0.0.0.0:{port}/")
    print(f"  - API Health: http://0.0.0.0:{port}/api/health")
    print(f"  - API Docs: http://0.0.0.0:{port}/docs")
    
    # Importar y ejecutar la aplicación
    try:
        from iso_standards_games.__main__ import app
        import uvicorn
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            workers=1,
            access_log=True,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Error al iniciar la aplicación: {e}")
        sys.exit(1)

def main():
    """Función principal."""
    print("🎮 ISO Standards Games - Back4App Startup Script")
    print("=" * 50)
    
    # Verificaciones previas
    if not check_environment():
        print("\n❌ Verificación del entorno fallida.")
        sys.exit(1)
    
    if not check_dependencies():
        print("\n❌ Verificación de dependencias fallida.")
        sys.exit(1)
    
    # Preparar entorno
    create_data_directory()
    
    # Iniciar aplicación
    start_application()

if __name__ == "__main__":
    main()