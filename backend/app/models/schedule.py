"""
Modèle SQLAlchemy pour la table des horaires.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, Time, DateTime
from ..database import Base


class Schedule(Base):
    """
    Modèle représentant un horaire de travail.
    """
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date_saisie = Column(DateTime, default=datetime.utcnow, nullable=False)
    heure_debut = Column(Time, nullable=False)
    heure_debut_pause = Column(Time, nullable=False)
    heure_fin_pause = Column(Time, nullable=False)
    heure_depart_calculee = Column(Time, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Schedule(id={self.id}, date_saisie={self.date_saisie}, heure_debut={self.heure_debut})>"
