# 🚀 Quick Start - Backend FastAPI

## Démarrage Rapide (3 étapes)

### 1️⃣ Installer les dépendances

```bash
cd backend
pip install -r requirements.txt
```

### 2️⃣ Lancer le serveur

**Option A: Script automatique (recommandé)**
```bash
./run.sh
```

**Option B: Manuel**
```bash
uvicorn app.main:app --reload
```

**Option C: Docker**
```bash
docker-compose up
```

### 3️⃣ Accéder à l'API

- **API Root**: http://localhost:8000/
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/health

---

## 🧪 Tester l'API

### Script de Test Automatique

```bash
./test_api_manual.sh
```

### Tests Manuels avec curl

#### Créer un horaire
```bash
curl -X POST http://localhost:8000/api/schedules/ \
  -H "Content-Type: application/json" \
  -d '{
    "heure_debut": "08:00:00",
    "heure_pause_debut": "12:00:00",
    "heure_pause_fin": "12:45:00"
  }'
```

#### Récupérer les statistiques
```bash
curl http://localhost:8000/api/statistics/
```

---

## 📚 Endpoints Disponibles

### Horaires
- `GET /api/schedules/` - Liste tous les horaires
- `POST /api/schedules/` - Créer un horaire
- `GET /api/schedules/{id}` - Détail d'un horaire
- `PUT /api/schedules/{id}` - Modifier un horaire
- `DELETE /api/schedules/{id}` - Supprimer un horaire

### Statistiques
- `GET /api/statistics/` - Statistiques moyennes
- `GET /api/statistics/charts` - Données pour graphiques

### Configuration
- `GET /api/config/` - Configuration actuelle
- `PUT /api/config/` - Modifier la configuration
- `POST /api/config/reset` - Réinitialiser

### Santé
- `GET /api/health` - Health check

---

## 🎯 Exemple Complet

```bash
# 1. Vérifier que l'API est en ligne
curl http://localhost:8000/api/health

# 2. Créer un horaire
curl -X POST http://localhost:8000/api/schedules/ \
  -H "Content-Type: application/json" \
  -d '{
    "heure_debut": "08:00:00",
    "heure_pause_debut": "12:00:00",
    "heure_pause_fin": "12:45:00"
  }'
# Réponse: heure_depart_calculee = "15:55:00"

# 3. Récupérer tous les horaires
curl http://localhost:8000/api/schedules/

# 4. Voir les statistiques
curl http://localhost:8000/api/statistics/
```

---

## 🐛 Dépannage

### Le serveur ne démarre pas
```bash
# Vérifier que le port 8000 est libre
lsof -i :8000

# Vérifier les logs
cat /tmp/fastapi.log  # Si lancé en arrière-plan
```

### Erreur "Module not found"
```bash
# Réinstaller les dépendances
pip install -r requirements.txt
```

### Base de données verrouillée
```bash
# Supprimer et recréer la DB
rm horaires.db
# Redémarrer le serveur (la DB sera recréée)
```

---

## 📖 Documentation Complète

- **README.md** - Documentation détaillée du projet
- **TEST_RESULTS.md** - Résultats des tests complets
- **Swagger UI** - http://localhost:8000/docs (quand le serveur tourne)

---

## 🎉 C'est Tout!

Votre API FastAPI est maintenant opérationnelle et prête à gérer les horaires de travail avec calcul automatique de l'heure de départ !
