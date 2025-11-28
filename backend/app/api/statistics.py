"""
Routes API pour les statistiques.
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..services import statistics_service

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get("/", response_model=Dict[str, Any])
def get_statistics(db: Session = Depends(get_db)):
    """
    Récupère les statistiques sur les horaires.

    Args:
        db: Session de base de données

    Returns:
        Dictionnaire contenant les statistiques (moyennes)
    """
    return statistics_service.get_statistics(db)


@router.get("/charts", response_model=Dict[str, Any])
def get_charts_data(db: Session = Depends(get_db)):
    """
    Récupère les données pour générer les graphiques.

    Args:
        db: Session de base de données

    Returns:
        Dictionnaire contenant les données pour les graphiques
    """
    return statistics_service.get_charts_data(db)
