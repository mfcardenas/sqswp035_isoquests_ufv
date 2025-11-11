# Dockerfile optimizado para Back4App
# ISO Standards Games - FastAPI Application with React Frontend

FROM python:3.9-slim

# Información del mantenedor
LABEL maintainer="UFV Software Quality <sqs@ufv.es>"
LABEL description="ISO Standards Educational Games - FastAPI Application"
LABEL version="1.0"

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    make \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Instalar Poetry
RUN pip install --no-cache-dir poetry

# Configurar Poetry para no crear entornos virtuales
RUN poetry config virtualenvs.create false

# Copiar archivos de configuración de Python
COPY pyproject.toml poetry.lock* ./

# Instalar dependencias Python
RUN poetry install --no-dev --no-interaction --no-ansi

# Copiar código fuente de la aplicación
COPY . .

# Construir el frontend React si existe
RUN if [ -d "iso_standards_games/frontend" ]; then \
        echo "Building React frontend..." && \
        cd iso_standards_games/frontend && \
        npm ci --only=production && \
        npm run build && \
        echo "Frontend built successfully"; \
    else \
        echo "No frontend directory found, skipping build"; \
    fi

# Crear directorio de base de datos SQLite
RUN mkdir -p /app/data && \
    chmod 755 /app/data

# Exponer puerto 8000 para Back4App
EXPOSE 8000

# Variables de entorno para producción
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV DEBUG=false
ENV APP_NAME="ISO Standards Games"
ENV DATABASE_URL=sqlite:///./data/iso_standards_games.db
ENV LLM_PROVIDER=ollama
ENV OLLAMA_BASE_URL=http://localhost:11434
ENV OLLAMA_MODEL=qwen3
ENV DEFAULT_LOCALE=en

# Health check para Back4App
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Comando para ejecutar la aplicación
CMD ["python", "-m", "uvicorn", "iso_standards_games.__main__:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]