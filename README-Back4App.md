# 🎮 ISO Standards Games - Despliegue en Back4App

## 🚀 Aplicación Educativa de Estándares ISO

Una aplicación FastAPI interactiva que enseña estándares ISO/IEC 25010, ISO/IEC/IEEE 29148 e ISO 9241 mediante gamificación.

## 🎯 Juegos Incluidos

1. **QualityQuest** - Aprende sobre los 8 atributos de calidad de ISO/IEC 25010
2. **ReqRally** - Comprende principios de especificación de requisitos de ISO/IEC/IEEE 29148
3. **UXplorer** - Explora principios de usabilidad de ISO 9241
4. **StandardShowdown** - Integra conocimientos de los tres estándares
5. **QualityArchitect** - Aplica estándares en escenarios de diseño de software

## ✅ Configuración para Back4App

### Archivos de Despliegue Incluidos:

- ✅ **`Dockerfile`** - Configurado para Back4App con puerto 8000
- ✅ **`docker-compose.yml`** - Para desarrollo local
- ✅ **`.dockerignore`** - Optimizado para reducir tamaño de imagen
- ✅ **`__main__.py`** - Modificado para puerto dinámico de Back4App

### Tecnologías:

- **Backend**: FastAPI + Python 3.9
- **Frontend**: React (construido automáticamente)
- **Base de datos**: SQLite (persistente)
- **Gestión de dependencias**: Poetry
- **LLM**: Integración con Ollama/Azure OpenAI

## 🐳 Configuración Docker para Back4App

### Dockerfile Optimizado:
```dockerfile
FROM python:3.9-slim

# Instalar Node.js para construir frontend React
RUN apt-get update && apt-get install -y nodejs npm

# Instalar Poetry y dependencias
RUN pip install poetry
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-dev

# Construir frontend automáticamente
COPY . .
RUN cd iso_standards_games/frontend && npm install && npm run build

# Exponer puerto 8000 para Back4App
EXPOSE 8000

# Comando optimizado para Back4App
CMD ["python", "-m", "uvicorn", "iso_standards_games.__main__:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Puerto Dinámico Configurado:
```python
# __main__.py
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run("iso_standards_games.__main__:app", host="0.0.0.0", port=port)
```

## 📋 Pasos de Despliegue en Back4App

### 1. Preparar Proyecto
```bash
# Comprimir todo el directorio iso-standards-games en un ZIP
# O subir a repositorio Git
```

### 2. Crear App en Back4App
1. **Ir a** [Back4App](https://www.back4app.com/)
2. **Crear nueva app** → "Container as a Service"
3. **Subir código** → ZIP o conectar repositorio Git

### 3. Configuración Automática
- ✅ **Puerto**: 8000 (detectado automáticamente por `EXPOSE 8000`)
- ✅ **Dockerfile**: Detectado en la raíz del proyecto
- ✅ **Build**: Automático con Poetry + npm

### 4. Variables de Entorno (Opcionales)
En Back4App Dashboard → Environment Variables:

```
DEBUG=false
APP_NAME=ISO Standards Games
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen3
DATABASE_URL=sqlite:///./data/iso_standards_games.db
DEFAULT_LOCALE=en
```

### 5. Deploy
1. **Click "Deploy"**
2. **Esperar build** (5-10 minutos por primera vez)
3. **Obtener URL** → `https://tu-app.back4app.io`

## 🌐 Endpoints Disponibles

Una vez desplegado:

- **🏠 Aplicación Principal**: `https://tu-app.back4app.io/`
- **⚕️ Health Check**: `https://tu-app.back4app.io/api/health`
- **🎮 API Games**: `https://tu-app.back4app.io/api/v1/games/`
- **👤 API Users**: `https://tu-app.back4app.io/api/v1/users/`
- **📚 Documentación API**: `https://tu-app.back4app.io/docs`

## 🔧 Funcionalidades Principales

### Sistema de Gamificación:
- **Puntuación y progreso** tracking
- **Feedback inteligente** con LLM
- **Escenarios adaptativos** por nivel

### Soporte Multiidioma:
- **Inglés y Español** integrados
- **Localización dinámica** de contenido
- **Archivos i18n** incluidos

### Integración LLM:
- **Agentes inteligentes** para cada juego
- **Retroalimentación personalizada**
- **Generación de escenarios** dinámicos

## 🧪 Testing Local

### Usando Docker:
```bash
# Construir imagen
docker build -t iso-games .

# Ejecutar localmente
docker run -p 8000:8000 iso-games

# Acceder a http://localhost:8000
```

### Usando Docker Compose:
```bash
# Iniciar todos los servicios
docker-compose up --build

# Acceder a http://localhost:8000
```

### Desarrollo sin Docker:
```bash
# Instalar dependencias
poetry install

# Ejecutar aplicación
poetry run python -m iso_standards_games

# Acceder a http://localhost:8000
```

## 📊 Estructura del Proyecto

```
iso-standards-games/
├── iso_standards_games/         # Código principal
│   ├── api/                     # FastAPI routes
│   ├── games/                   # Lógica de juegos
│   ├── agents/                  # Agentes LLM
│   ├── frontend/               # React frontend
│   └── __main__.py             # Punto de entrada
├── Dockerfile                  # Configuración Docker
├── docker-compose.yml         # Desarrollo local
├── pyproject.toml            # Dependencias Poetry
└── README-Back4App.md        # Esta documentación
```

## ⚠️ Troubleshooting

### Error: "Build failed"
**Verificar:**
- `pyproject.toml` tiene todas las dependencias
- Frontend React se construye correctamente
- No hay errores de sintaxis Python

### Error: "Container failed to start"
**Revisar en Back4App logs:**
- Puerto 8000 está siendo usado
- Base de datos SQLite se crea correctamente
- Variables de entorno están configuradas

### Error: "Frontend not loading"
**Posibles causas:**
- Build de React falló durante Docker build
- Archivos estáticos no montados correctamente
- CORS mal configurado

**Solución:**
```python
# En api/app.py - CORS ya configurado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🔐 Configuración de Producción

### Para Back4App:
- ✅ **Debug mode**: Desactivado
- ✅ **CORS**: Configurado permisivo para desarrollo (ajustar en producción)
- ✅ **Health checks**: Endpoint `/api/health` disponible
- ✅ **Static files**: Frontend React servido automáticamente

### Seguridad:
- **SQLite database**: Persistente en volumen `/app/data`
- **Environment variables**: Manejadas por Back4App
- **LLM credentials**: Configurar en variables de entorno

## 📈 Escalabilidad

### Back4App Features:
- **Auto-scaling**: Basado en demanda
- **Load balancing**: Automático
- **Persistent storage**: Para base de datos SQLite
- **Monitoring**: Dashboard integrado

## 📞 Soporte

**Para problemas técnicos:**
- **Logs**: Back4App Dashboard → Logs
- **Health**: Verificar `/api/health` endpoint
- **API Docs**: Acceder a `/docs` para testing

**Contacto:** sqs@ufv.es

---

## 🎉 ¡Tu aplicación está lista para Back4App!

Con FastAPI + React, tu aplicación educativa de estándares ISO se desplegará automáticamente en Back4App.