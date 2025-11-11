# Dockerfile para ISO Standards Games Multi-Server
# Ejecuta QualityQuest, RequirementRally y UsabilityUniverse

FROM python:3.9-slim

# Información del mantenedor
LABEL maintainer="UFV Software Quality <sqs@ufv.es>"
LABEL description="ISO Standards Educational Games - Multi-Server Application"
LABEL version="2.0"

# Establecer directorio de trabajo
WORKDIR /app

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copiar requirements.txt e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar todo el código fuente
COPY . .

# Crear directorios necesarios
RUN mkdir -p /app/data /var/log && \
    chmod 755 /app/data /var/log

# Exponer puertos principales
EXPOSE 8000 8001 8003

# Variables de entorno para producción
ENV DEBUG=false
ENV APP_NAME="ISO Standards Games"
ENV DATABASE_URL=sqlite:///./data/iso_standards_games.db
ENV LLM_PROVIDER=ollama
ENV OLLAMA_BASE_URL=http://localhost:11434
ENV OLLAMA_MODEL=qwen3
ENV DEFAULT_LOCALE=en

# Health check para el servidor principal
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Ejecutar el script multi-servidor
CMD ["python", "multi_server_startup.py"]