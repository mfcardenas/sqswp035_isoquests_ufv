"""Main API routes for the application."""

from fastapi import APIRouter

from iso_standards_games.api.v1.games import router as games_router
from iso_standards_games.api.v1.users import router as users_router

# Main router
router = APIRouter()

# Health check endpoint for Back4App
@router.get("/health")
async def health_check():
    """Health check endpoint for container monitoring."""
    return {"status": "healthy", "service": "iso-standards-games"}

# Root endpoint
@router.get("/")
async def root():
    """Root API endpoint."""
    return {"message": "ISO Standards Games API", "version": "1.0"}

# Include versioned API routes
router.include_router(games_router, prefix="/v1/games", tags=["Games"])
router.include_router(users_router, prefix="/v1/users", tags=["Users"])