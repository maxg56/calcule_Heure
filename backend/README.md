# Backend FastAPI - Calcule Heure

API REST moderne pour la gestion des horaires de travail.

## 🚀 Démarrage Rapide

### Installation

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Linux/Mac:
source venv/bin/activate
# Sur Windows:
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### Configuration

Créer un fichier `.env` à partir de `.env.example`:

```bash
cp .env.example .env
```

### Lancement

```bash
# Développement (avec rechargement automatique)
uvicorn app.main:app --reload

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

L'API sera disponible sur: http://localhost:8000

La documentation interactive (Swagger) sera disponible sur: http://localhost:8000/docs

## 🐳 Docker

### Construction de l'image

```bash
docker build -t calcule-heure-api .
```

### Lancement du conteneur

```bash
docker run -p 8000:8000 calcule-heure-api
```

## 📚 Documentation API

### Endpoints Disponibles

#### Horaires

- `GET /api/schedules` - Liste tous les horaires
- `POST /api/schedules` - Créer un nouvel horaire
- `GET /api/schedules/{id}` - Détail d'un horaire
- `PUT /api/schedules/{id}` - Modifier un horaire
- `DELETE /api/schedules/{id}` - Supprimer un horaire

#### Statistiques

- `GET /api/statistics` - Statistiques globales (moyennes)
- `GET /api/statistics/charts` - Données pour les graphiques

#### Configuration

- `GET /api/config` - Configuration actuelle
- `PUT /api/config` - Mettre à jour la configuration
- `POST /api/config/reset` - Réinitialiser la configuration

#### Santé

- `GET /api/health` - Health check

### Exemple de Requête

#### Créer un horaire

```bash
curl -X POST "http://localhost:8000/api/schedules" \
  -H "Content-Type: application/json" \
  -d '{
    "heure_debut": "08:00:00",
    "heure_pause_debut": "12:00:00",
    "heure_pause_fin": "12:45:00"
  }'
```

#### Récupérer les statistiques

```bash
curl -X GET "http://localhost:8000/api/statistics"
```

## 🏗️ Structure du Projet

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Point d'entrée FastAPI
│   ├── config.py            # Configuration
│   ├── database.py          # Connexion DB
│   │
│   ├── models/              # Modèles SQLAlchemy
│   │   ├── __init__.py
│   │   ├── schedule.py
│   │   └── config.py
│   │
│   ├── schemas/             # Schémas Pydantic
│   │   ├── __init__.py
│   │   ├── schedule.py
│   │   └── config.py
│   │
│   ├── api/                 # Routes API
│   │   ├── __init__.py
│   │   ├── schedules.py
│   │   ├── statistics.py
│   │   ├── config.py
│   │   └── health.py
│   │
│   └── services/            # Logique métier
│       ├── __init__.py
│       ├── schedule_service.py
│       └── statistics_service.py
│
├── tests/
├── requirements.txt
├── Dockerfile
└── README.md
```

## 🛠️ Technologies

- **FastAPI** - Framework web moderne et rapide
- **SQLAlchemy** - ORM pour la gestion de la base de données
- **Pydantic** - Validation des données
- **Uvicorn** - Serveur ASGI
- **SQLite** - Base de données (par défaut)

## 📝 Notes

- La base de données SQLite est créée automatiquement au premier lancement
- La configuration par défaut (7h10 de travail, 45min de pause) est initialisée automatiquement
- L'API supporte CORS pour permettre les requêtes depuis le frontend
