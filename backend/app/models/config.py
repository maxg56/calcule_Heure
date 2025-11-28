"""
Modèle SQLAlchemy pour la table de configuration.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, CheckConstraint
from ..database import Base


class Config(Base):
    """
    Modèle représentant la configuration de l'application.
    Il ne peut y avoir qu'une seule ligne dans cette table (id=1).
    """
    __tablename__ = "config"

    id = Column(Integer, primary_key=True)
    duree_travail_heures = Column(Integer, nullable=False, default=7)
    duree_travail_minutes = Column(Integer, nullable=False, default=10)
    seuil_pause_minutes = Column(Integer, nullable=False, default=45)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    __table_args__ = (
        CheckConstraint('id = 1', name='single_row_check'),
    )

    def __repr__(self):
        return f"<Config(duree_travail={self.duree_travail_heures}h{self.duree_travail_minutes:02d}, seuil_pause={self.seuil_pause_minutes}min)>"
