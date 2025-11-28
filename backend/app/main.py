"""
Point d'entrée principal de l'application FastAPI.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import init_db
from .api import schedules, statistics, config, health

# Créer l'application FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API REST pour la gestion des horaires de travail",
    debug=settings.DEBUG
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(health.router, prefix=settings.API_V1_PREFIX)
app.include_router(schedules.router, prefix=settings.API_V1_PREFIX)
app.include_router(statistics.router, prefix=settings.API_V1_PREFIX)
app.include_router(config.router, prefix=settings.API_V1_PREFIX)


@app.on_event("startup")
async def startup_event():
    """
    Événement de démarrage de l'application.
    Initialise la base de données.
    """
    init_db()


@app.get("/")
def root():
    """
    Route racine de l'API.
    """
    return {
        "message": "Bienvenue sur l'API Calcule Heure",
        "version": settings.APP_VERSION,
        "documentation": "/docs"
    }
