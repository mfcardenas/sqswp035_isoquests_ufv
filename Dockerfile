# Dockerfile optimizado para Back4App (versión simplificada)
# ISO Standards Games - FastAPI Application

FROM python:3.9-slim

# Información del mantenedor
LABEL maintainer="UFV Software Quality <sqs@ufv.es>"
LABEL description="ISO Standards Educational Games - FastAPI Application"
LABEL version="1.0"

# Establecer directorio de trabajo
WORKDIR /app

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copiar requirements.txt y instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código fuente de la aplicación
COPY . .

# Crear directorio de base de datos SQLite
RUN mkdir -p /app/data && \
    chmod 755 /app/data

# Exponer puerto 8000 para Back4App
EXPOSE 8000

# Variables de entorno para producción
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
# Usar script de inicio que configura dinámicamente el servidor
CMD ["python", "start_server.py"]