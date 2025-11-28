"""
Tests d'intégration pour l'API.
"""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models.config import Config

# Base de données de test en mémoire
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créer les tables de test
Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override de la dépendance get_db pour les tests."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_health_check():
    """Test du health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root():
    """Test de l'endpoint racine."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_create_schedule():
    """Test de création d'un horaire."""
    # D'abord, créer la configuration par défaut
    db = TestingSessionLocal()
    config = db.query(Config).filter(Config.id == 1).first()
    if not config:
        config = Config(id=1, duree_travail_heures=7, duree_travail_minutes=10, seuil_pause_minutes=45)
        db.add(config)
        db.commit()
    db.close()

    # Créer un horaire
    response = client.post(
        "/api/schedules/",
        json={
            "heure_debut": "08:00:00",
            "heure_pause_debut": "12:00:00",
            "heure_pause_fin": "12:45:00"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["heure_debut"] == "08:00:00"
    assert "heure_depart_calculee" in data


def test_get_schedules():
    """Test de récupération des horaires."""
    response = client.get("/api/schedules/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_statistics():
    """Test de récupération des statistiques."""
    response = client.get("/api/statistics/")
    assert response.status_code == 200
    data = response.json()
    assert "nombre_entrees" in data


def test_get_config():
    """Test de récupération de la configuration."""
    # Créer la configuration si elle n'existe pas
    db = TestingSessionLocal()
    config = db.query(Config).filter(Config.id == 1).first()
    if not config:
        config = Config(id=1, duree_travail_heures=7, duree_travail_minutes=10, seuil_pause_minutes=45)
        db.add(config)
        db.commit()
    db.close()

    response = client.get("/api/config/")
    assert response.status_code == 200
    data = response.json()
    assert "duree_travail_heures" in data
    assert "duree_travail_minutes" in data
