#!/usr/bin/env python3
"""
Script para generar config.js dinámico para Back4App
"""

import os

def generate_config_js():
    """Generar config.js con la configuración correcta para Back4App"""
    
    # Obtener puerto de Back4App o usar 8000 por defecto
    port = os.environ.get('PORT', '8000')
    
    config_content = f"""// Configuration file for ISO Standards Games - Back4App Version
// Generated dynamically for deployment

const CONFIG = {{
  // Server configuration (Back4App)
  SERVER: {{
    PORT: {port},
    HOST: '0.0.0.0'
  }},
  
  // API endpoints - all relative for Back4App deployment
  API: {{
    BASE_URL: '',  // Empty = relative URLs work in Back4App
    ENDPOINTS: {{
      GAMES: '/api/v1/games',
      SESSIONS: '/api/v1/games/quality_quest/sessions',
      RESPONSE: '/api/v1/games/quality_quest/sessions/{{sessionId}}/response',
      
      // RequirementRally endpoints
      RALLY_STATS: '/rally/stats',
      RALLY_SESSION: '/rally/session',
      RALLY_SUBMIT: '/rally/session/{{sessionId}}/submit',
      
      // UsabilityUniverse endpoints
      UNIVERSE_SESSION: '/universe/session',
      UNIVERSE_SUBMIT: '/universe/session/{{sessionId}}/submit',
      UNIVERSE_HEALTH: '/universe/health'
    }}
  }},
  
  // Frontend paths
  FRONTEND: {{
    STATIC_DIR: './iso_standards_games/frontend/dist',
    INDEX_FILE: './iso_standards_games/frontend/dist/index.html'
  }},
  
  // Game settings
  GAME: {{
    TOTAL_SCENARIOS: 5,
    LLM_TIMEOUT: 15,
    SESSION_CLEANUP_INTERVAL: 3600 // 1 hour
  }},
  
  // Back4App deployment settings
  DEPLOYMENT: {{
    PLATFORM: 'back4app',
    PORT: {port},
    BASE_URL: window.location.origin // Dinámico según el dominio de Back4App
  }}
}};

// Export for both Node.js and browser
if (typeof module !== 'undefined' && module.exports) {{
  module.exports = CONFIG;
}} else {{
  window.CONFIG = CONFIG;
  
  // Para RequirementRally: Override de la URL hardcodeada
  if (typeof RequirementRallyGame !== 'undefined' && RequirementRallyGame.prototype) {{
    RequirementRallyGame.prototype.apiUrl = CONFIG.DEPLOYMENT.BASE_URL;
  }}
}}
"""
    
    # Escribir el archivo
    with open('config.js', 'w') as f:
        f.write(config_content)
    
    print(f"✅ Generated config.js for Back4App (port {port})")
    return config_content

if __name__ == "__main__":
    generate_config_js()