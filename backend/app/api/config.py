"""
Routes API pour la gestion de la configuration.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.config import Config
from ..schemas.config import ConfigUpdate, ConfigResponse

router = APIRouter(prefix="/config", tags=["config"])


@router.get("/", response_model=ConfigResponse)
def get_config(db: Session = Depends(get_db)):
    """
    Récupère la configuration actuelle.

    Args:
        db: Session de base de données

    Returns:
        Configuration actuelle
    """
    config = db.query(Config).filter(Config.id == 1).first()

    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuration non trouvée"
        )

    return config


@router.put("/", response_model=ConfigResponse)
def update_config(
    config_update: ConfigUpdate,
    db: Session = Depends(get_db)
):
    """
    Met à jour la configuration.

    Args:
        config_update: Données de configuration à mettre à jour
        db: Session de base de données

    Returns:
        Configuration mise à jour
    """
    config = db.query(Config).filter(Config.id == 1).first()

    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuration non trouvée"
        )

    # Mettre à jour les champs fournis
    update_data = config_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(config, field, value)

    db.commit()
    db.refresh(config)

    return config


@router.post("/reset", response_model=ConfigResponse)
def reset_config(db: Session = Depends(get_db)):
    """
    Réinitialise la configuration aux valeurs par défaut.

    Args:
        db: Session de base de données

    Returns:
        Configuration réinitialisée
    """
    config = db.query(Config).filter(Config.id == 1).first()

    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuration non trouvée"
        )

    # Réinitialiser aux valeurs par défaut
    config.duree_travail_heures = 7
    config.duree_travail_minutes = 10
    config.seuil_pause_minutes = 45

    db.commit()
    db.refresh(config)

    return config
