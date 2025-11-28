"""
Configuration de la base de données SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Création du moteur de base de données
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
)

# Session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()


def get_db():
    """
    Générateur de session de base de données pour les dépendances FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialise la base de données (création des tables).
    """
    from .models import Schedule, Config

    Base.metadata.create_all(bind=engine)

    # Créer la configuration par défaut si elle n'existe pas
    db = SessionLocal()
    try:
        config = db.query(Config).filter(Config.id == 1).first()
        if not config:
            config = Config(
                id=1,
                duree_travail_heures=7,
                duree_travail_minutes=10,
                seuil_pause_minutes=45
            )
            db.add(config)
            db.commit()
    finally:
        db.close()
