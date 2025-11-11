# Dockerfile para ISO Standards Games - Proyecto Original Intacto
# Solo ejecuta QualityQuest usando el método oficial del proyecto

FROM python:3.9-slim

# Información del mantenedor
LABEL maintainer="UFV Software Quality <sqs@ufv.es>"
LABEL description="ISO Standards Games - QualityQuest (Proyecto Original)"
LABEL version="1.0.0"

# Establecer directorio de trabajo
WORKDIR /app

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Instalar dependencias del sistema mínimas
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copiar requirements.txt e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar COMPLETAMENTE el código fuente (sin modificar nada)
COPY . .

# Crear directorio de datos
RUN mkdir -p /app/data && \
    chmod 755 /app/data

# Exponer puerto estándar Back4App
EXPOSE 8000

# Variables de entorno básicas para Back4App
ENV DEBUG=false
ENV DATABASE_URL=sqlite:///./data/iso_standards_games.db

# Health check básico
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# COMANDO OFICIAL DEL PROYECTO - CERO MODIFICACIONES
CMD ["python", "-m", "iso_standards_games"]