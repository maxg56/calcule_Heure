"""
Routes API pour le health check.
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    """
    Health check endpoint.

    Returns:
        Statut de santé de l'API
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Calcule Heure API"
    }
