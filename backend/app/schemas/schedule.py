"""
Schémas Pydantic pour les horaires.
"""

from datetime import datetime, time, timedelta
from typing import Optional
from pydantic import BaseModel, Field, computed_field


class ScheduleBase(BaseModel):
    """Schéma de base pour un horaire."""
    heure_debut: time = Field(..., description="Heure de début de travail")
    heure_debut_pause: time = Field(..., description="Heure de début de pause", serialization_alias="heure_debut_pause", validation_alias="heure_debut_pause")
    heure_fin_pause: time = Field(..., description="Heure de fin de pause", serialization_alias="heure_fin_pause", validation_alias="heure_fin_pause")


class ScheduleCreate(BaseModel):
    """Schéma pour la création d'un horaire."""
    heure_debut: time = Field(..., description="Heure de début de travail")
    heure_debut_pause: time = Field(..., description="Heure de début de pause")
    heure_fin_pause: time = Field(..., description="Heure de fin de pause")


class ScheduleUpdate(BaseModel):
    """Schéma pour la mise à jour d'un horaire."""
    heure_debut: Optional[time] = Field(None, description="Heure de début de travail")
    heure_debut_pause: Optional[time] = Field(None, description="Heure de début de pause")
    heure_fin_pause: Optional[time] = Field(None, description="Heure de fin de pause")


class ScheduleResponse(BaseModel):
    """Schéma pour la réponse d'un horaire."""
    id: int
    date_saisie: datetime
    heure_debut: time
    heure_debut_pause: time
    heure_fin_pause: time
    heure_depart_calculee: time
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def duree_pause_minutes(self) -> int:
        """Calcule la durée de la pause en minutes."""
        debut = timedelta(hours=self.heure_debut_pause.hour, minutes=self.heure_debut_pause.minute)
        fin = timedelta(hours=self.heure_fin_pause.hour, minutes=self.heure_fin_pause.minute)
        duree = fin - debut
        return int(duree.total_seconds() / 60)

    class Config:
        from_attributes = True
