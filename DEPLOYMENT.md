# ISO Standards Games - Deployment Guide

## 🐳 Docker Deployment para Back4App

Este proyecto incluye múltiples aplicaciones educativas independientes:

- **QualityQuest**: Juego principal de estándares ISO (puerto 8000)
- **RequirementRally**: Juego de clasificación de requisitos (puerto 8001)  
- **UsabilityUniverse**: Juego de usabilidad ISO 9241 (puerto 8003)

### Arquitectura Multi-Servidor

Debido a que cada aplicación es independiente, el Dockerfile utiliza un enfoque multi-servidor:

```bash
# Ejecutar localmente con Docker
docker build -t iso-standards-games .
docker run -p 8000:8000 -p 8001:8001 -p 8003:8003 iso-standards-games
```

### Archivos de Configuración

- `Dockerfile`: Imagen Docker optimizada para múltiples servidores
- `multi_server_startup.py`: Script que coordina todos los servidores
- `requirements.txt`: Dependencias unificadas (generado desde pyproject.toml)

### Scripts de Gestión

#### `multi_server_startup.py`
- Modifica dinámicamente puertos para evitar conflictos
- Ejecuta los 3 servidores en paralelo
- Proporciona logging consolidado
- Maneja la terminación graceful

### Back4App Deployment

Para desplegar en Back4App:

1. El puerto principal expositorà el puerto 8000 (QualityQuest)
2. Los otros juegos estarán disponibles a través de:
   - RequirementRally: `https://tu-app.back4app.io:8001`
   - UsabilityUniverse: `https://tu-app.back4app.io:8003`

### Variables de Entorno

```env
PORT=8000                    # Puerto principal para Back4App
DEBUG=false                  # Modo producción
DATABASE_URL=sqlite:///./data/iso_standards_games.db
LLM_PROVIDER=ollama         # Proveedor LLM
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3
DEFAULT_LOCALE=en
```

### Health Check

El contenedor incluye health check en el puerto 8000:
```bash
curl -f http://localhost:8000/ || exit 1
```

### Logs

Cada servidor genera logs con formato:
- `[QualityQuest] ...`
- `[RequirementRally] ...`
- `[UsabilityUniverse] ...`

### Desarrollo Local

Para desarrollo local sin Docker:

```bash
# Terminal 1: QualityQuest
python -m iso_standards_games

# Terminal 2: RequirementRally  
python requirement_rally_server.py

# Terminal 3: UsabilityUniverse
python usability_universe_server.py
```

O usar el script unificado:
```bash
python multi_server_startup.py
```

### Troubleshooting

1. **Puerto ocupado**: El script verifica automáticamente puertos disponibles
2. **Módulo no encontrado**: Ejecutar desde el directorio raíz del proyecto
3. **Base de datos**: SQLite se crea automáticamente en `/app/data/`
4. **LLM Connection**: Configurar variables OLLAMA_* según necesidades

### Diferencias con Versión Original

- ✅ Mantiene la funcionalidad original intacta
- ✅ No modifica la lógica de negocio
- ✅ Preserva la estructura de archivos
- 🔧 Añade configuración de puertos dinámicos
- 🔧 Unifica dependencias en requirements.txt
- 🔧 Script de coordinación multi-servidor