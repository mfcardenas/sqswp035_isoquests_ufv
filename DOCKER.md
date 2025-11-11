# ISO Standards Games - Docker Deployment

## 🎮 Proyecto Original Respetado

Este Dockerfile **NO MODIFICA** el proyecto base. Ejecuta la aplicación exactamente como fue diseñada:

```bash
python -m iso_standards_games
```

## 🐳 Build & Deploy

### Local Testing
```bash
docker build -t iso-standards-games .
docker run -p 8000:8000 iso-standards-games
```

### Back4App Deployment
1. El Dockerfile está optimizado para Back4App
2. Usa el puerto 8000 como requiere la plataforma
3. Incluye health check en `/api/health`

## 🎯 Funcionalidad

La aplicación incluye:
- ✅ **QualityQuest**: Juego principal implementado
- ⚠️  **Otros juegos**: Mencionados en README pero no implementados aún

## 📁 Estructura Mantenida

```
iso_standards_games/
├── __main__.py          # Punto de entrada oficial
├── api/                 # API FastAPI
├── frontend/dist/       # Frontend compilado incluido
├── games/               # Solo QualityQuest implementado
└── ...                 # Resto del proyecto intacto
```

## 🔧 Configuración Back4App

- **Puerto**: 8000 (automático vía PORT env var)
- **Health Check**: `/api/health`
- **Base de Datos**: SQLite local (data/ directory)
- **Frontend**: Servido automáticamente desde `/`

## ⚠️  Notas Importantes

1. El proyecto original **SOLO incluye QualityQuest**
2. Los archivos `requirement_rally_server.py` y `usability_universe_server.py` son **desarrollos separados**
3. No se modificó ningún archivo del proyecto base
4. El Dockerfile respeta completamente la arquitectura original

## 🚀 Resultado

Una aplicación Docker funcional que ejecuta ISO Standards Games exactamente como fue diseñada, sin modificaciones ni dependencias adicionales.