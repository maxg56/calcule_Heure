"""
Schémas Pydantic pour la configuration.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ConfigBase(BaseModel):
    """Schéma de base pour la configuration."""
    duree_travail_heures: int = Field(7, ge=0, le=12, description="Nombre d'heures de travail")
    duree_travail_minutes: int = Field(10, ge=0, le=59, description="Nombre de minutes de travail")
    seuil_pause_minutes: int = Field(45, ge=0, le=120, description="Durée minimale de pause recommandée")


class ConfigUpdate(BaseModel):
    """Schéma pour la mise à jour de la configuration."""
    duree_travail_heures: Optional[int] = Field(None, ge=0, le=12, description="Nombre d'heures de travail")
    duree_travail_minutes: Optional[int] = Field(None, ge=0, le=59, description="Nombre de minutes de travail")
    seuil_pause_minutes: Optional[int] = Field(None, ge=0, le=120, description="Durée minimale de pause recommandée")


class ConfigResponse(ConfigBase):
    """Schéma pour la réponse de configuration."""
    id: int
    updated_at: datetime

    class Config:
        from_attributes = True
