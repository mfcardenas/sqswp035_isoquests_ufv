"""Main module for ISO Standards Games application."""

import os
import uvicorn

from iso_standards_games.api.app import create_app

app = create_app()

if __name__ == "__main__":
    # Para Back4App: usar puerto dinámico
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(
        "iso_standards_games.__main__:app", 
        host="0.0.0.0", 
        port=port, 
        reload=False
    )