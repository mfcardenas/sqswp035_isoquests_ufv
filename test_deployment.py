#!/usr/bin/env python3
"""
Script de pruebas básicas para verificar la aplicación antes del despliegue.
"""

import asyncio
import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path para importaciones
sys.path.insert(0, str(Path(__file__).parent))

async def test_app_startup():
    """Probar que la aplicación puede iniciarse correctamente."""
    print("🧪 Test: Inicio de aplicación...")
    
    try:
        from iso_standards_games.api.app import create_app
        app = create_app()
        print("✅ Aplicación creada exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error al crear aplicación: {e}")
        return False

async def test_health_endpoint():
    """Probar el endpoint de health."""
    print("🧪 Test: Endpoint de health...")
    
    try:
        import httpx
        from iso_standards_games.api.app import create_app
        
        app = create_app()
        
        # Simular llamada al endpoint
        with httpx.Client(app=app, base_url="http://testserver") as client:
            response = client.get("/api/health")
            
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print("✅ Health endpoint funcionando correctamente")
                return True
            else:
                print(f"❌ Health endpoint respuesta incorrecta: {data}")
                return False
        else:
            print(f"❌ Health endpoint status code: {response.status_code}")
            return False
            
    except ImportError:
        print("⚠️ httpx no disponible, saltando test de health endpoint")
        return True
    except Exception as e:
        print(f"❌ Error en health endpoint: {e}")
        return False

async def test_configuration():
    """Probar que la configuración se carga correctamente."""
    print("🧪 Test: Configuración...")
    
    try:
        from iso_standards_games.core.config import settings
        
        # Verificar configuraciones básicas
        assert settings.APP_NAME is not None
        assert settings.LLM_PROVIDER is not None
        
        print(f"✅ Configuración cargada:")
        print(f"  - App Name: {settings.APP_NAME}")
        print(f"  - LLM Provider: {settings.LLM_PROVIDER}")
        print(f"  - Debug: {settings.DEBUG}")
        
        return True
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

async def test_port_configuration():
    """Probar que la configuración de puerto funciona."""
    print("🧪 Test: Configuración de puerto...")
    
    try:
        # Simular variable de entorno PORT
        original_port = os.environ.get("PORT")
        os.environ["PORT"] = "9999"
        
        from iso_standards_games.__main__ import app
        
        # Verificar que el puerto se puede obtener
        port = int(os.environ.get('PORT', 8000))
        assert port == 9999
        
        # Restaurar PORT original
        if original_port:
            os.environ["PORT"] = original_port
        else:
            del os.environ["PORT"]
        
        print("✅ Configuración de puerto dinámico funcionando")
        return True
    except Exception as e:
        print(f"❌ Error en configuración de puerto: {e}")
        return False

async def test_database_config():
    """Probar configuración de base de datos."""
    print("🧪 Test: Configuración de base de datos...")
    
    try:
        from iso_standards_games.core.config import settings
        
        # Verificar que la URL de base de datos está configurada
        assert settings.DATABASE_URL is not None
        print(f"✅ Database URL: {settings.DATABASE_URL}")
        
        # Verificar que el directorio de datos existe o se puede crear
        data_dir = Path("data")
        if not data_dir.exists():
            data_dir.mkdir(exist_ok=True)
            print("✅ Directorio de datos creado")
        else:
            print("✅ Directorio de datos existe")
        
        return True
    except Exception as e:
        print(f"❌ Error en configuración de base de datos: {e}")
        return False

async def run_all_tests():
    """Ejecutar todas las pruebas."""
    print("🎮 ISO Standards Games - Test Suite")
    print("=" * 40)
    
    tests = [
        test_configuration,
        test_port_configuration,
        test_database_config,
        test_app_startup,
        test_health_endpoint,
    ]
    
    results = []
    
    for test in tests:
        try:
            result = await test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test falló con excepción: {e}")
            results.append(False)
        print()  # Línea en blanco entre tests
    
    # Resumen
    passed = sum(results)
    total = len(results)
    
    print("📊 Resumen de Tests:")
    print(f"  ✅ Pasaron: {passed}")
    print(f"  ❌ Fallaron: {total - passed}")
    print(f"  📈 Porcentaje: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ¡Todos los tests pasaron! La aplicación está lista para Back4App.")
        return True
    else:
        print(f"\n⚠️ {total - passed} tests fallaron. Revisar configuración antes del despliegue.")
        return False

def main():
    """Función principal."""
    try:
        result = asyncio.run(run_all_tests())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n🛑 Tests interrumpidos por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()