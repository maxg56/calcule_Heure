"""
Schémas Pydantic pour les horaires.
"""

from datetime import datetime, time
from typing import Optional
from pydantic import BaseModel, Field


class ScheduleBase(BaseModel):
    """Schéma de base pour un horaire."""
    heure_debut: time = Field(..., description="Heure de début de travail")
    heure_pause_debut: time = Field(..., description="Heure de début de pause")
    heure_pause_fin: time = Field(..., description="Heure de fin de pause")


class ScheduleCreate(ScheduleBase):
    """Schéma pour la création d'un horaire."""
    pass


class ScheduleUpdate(BaseModel):
    """Schéma pour la mise à jour d'un horaire."""
    heure_debut: Optional[time] = Field(None, description="Heure de début de travail")
    heure_pause_debut: Optional[time] = Field(None, description="Heure de début de pause")
    heure_pause_fin: Optional[time] = Field(None, description="Heure de fin de pause")


class ScheduleResponse(ScheduleBase):
    """Schéma pour la réponse d'un horaire."""
    id: int
    date_saisie: datetime
    heure_depart_calculee: time
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
