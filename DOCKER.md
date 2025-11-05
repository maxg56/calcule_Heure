# Guide Docker - Application Calcule Horaires

Ce guide vous explique comment construire, exécuter et déployer l'application avec Docker.

## Table des Matières

- [Prérequis](#prérequis)
- [Build de l'Image](#build-de-limage)
- [Exécution Locale](#exécution-locale)
- [Docker Compose](#docker-compose)
- [Configuration](#configuration)
- [Déploiement Kubernetes](#déploiement-kubernetes)
- [Dépannage](#dépannage)

## Prérequis

- Docker >= 20.10
- Docker Compose >= 2.0 (optionnel)
- 1 Go d'espace disque disponible

### Installation de Docker

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**macOS:**
```bash
brew install --cask docker
```

**Windows:**
Téléchargez [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Build de l'Image

### Méthode 1: Script Automatique (Recommandé)

```bash
chmod +x build.sh
./build.sh [TAG]

# Exemples:
./build.sh latest
./build.sh v1.0.0
```

### Méthode 2: Commande Manuelle

```bash
# Build simple
docker build -t calcule-horaires:latest .

# Build avec cache désactivé
docker build --no-cache -t calcule-horaires:latest .

# Build multi-plateformes (pour ARM et x86)
docker buildx build --platform linux/amd64,linux/arm64 -t calcule-horaires:latest .
```

### Vérifier l'Image

```bash
# Lister les images
docker images calcule-horaires

# Inspecter l'image
docker inspect calcule-horaires:latest

# Voir l'historique de construction
docker history calcule-horaires:latest
```

## Exécution Locale

### Lancement Rapide

```bash
docker run -d \
  --name calcule-horaires \
  -p 8501:8501 \
  calcule-horaires:latest
```

Accédez à: http://localhost:8501

### Lancement avec Volumes (Persistance des Données)

```bash
docker run -d \
  --name calcule-horaires \
  -p 8501:8501 \
  -v $(pwd)/calcule_Heure/horaires.csv:/app/calcule_Heure/horaires.csv \
  -v $(pwd)/calcule_Heure/config.json:/app/calcule_Heure/config.json \
  calcule-horaires:latest
```

### Lancement avec Variables d'Environnement

```bash
docker run -d \
  --name calcule-horaires \
  -p 8501:8501 \
  -e STREAMLIT_SERVER_PORT=8501 \
  -e STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
  calcule-horaires:latest
```

### Commandes Utiles

```bash
# Voir les logs
docker logs calcule-horaires

# Logs en temps réel
docker logs -f calcule-horaires

# Arrêter le conteneur
docker stop calcule-horaires

# Redémarrer le conteneur
docker restart calcule-horaires

# Supprimer le conteneur
docker rm calcule-horaires

# Entrer dans le conteneur
docker exec -it calcule-horaires bash
```

## Docker Compose

### Lancement

```bash
# Démarrer l'application
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter l'application
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v
```

### Configuration docker-compose.yml

Le fichier `docker-compose.yml` inclut:
- Mapping de ports (8501:8501)
- Volumes pour la persistance
- Restart automatique
- Health checks
- Network dédié

### Personnalisation

Créez un fichier `docker-compose.override.yml`:

```yaml
version: '3.8'

services:
  horaires-app:
    ports:
      - "9000:8501"  # Changer le port local
    environment:
      - MY_CUSTOM_VAR=value
```

## Configuration

### Variables d'Environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| `STREAMLIT_SERVER_PORT` | Port du serveur | 8501 |
| `STREAMLIT_SERVER_ADDRESS` | Adresse d'écoute | 0.0.0.0 |
| `STREAMLIT_SERVER_HEADLESS` | Mode headless | true |
| `STREAMLIT_BROWSER_GATHER_USAGE_STATS` | Statistiques | false |

### Volumes

| Chemin dans le conteneur | Description |
|--------------------------|-------------|
| `/app/calcule_Heure/horaires.csv` | Données des horaires |
| `/app/calcule_Heure/config.json` | Configuration de l'app |
| `/app/.streamlit/config.toml` | Config Streamlit |

### Ports

| Port | Description |
|------|-------------|
| 8501 | Interface web Streamlit |

## Déploiement Kubernetes

### Prérequis

1. Cluster Kubernetes fonctionnel
2. kubectl configuré
3. Image Docker disponible dans un registry

### Push vers un Registry

```bash
# Docker Hub
docker tag calcule-horaires:latest username/calcule-horaires:latest
docker push username/calcule-horaires:latest

# GitHub Container Registry
docker tag calcule-horaires:latest ghcr.io/username/calcule-horaires:latest
docker push ghcr.io/username/calcule-horaires:latest

# Google Container Registry
docker tag calcule-horaires:latest gcr.io/project-id/calcule-horaires:latest
docker push gcr.io/project-id/calcule-horaires:latest
```

### Déploiement

```bash
# Appliquer les manifestes Kubernetes
kubectl apply -f k8s/

# Vérifier le déploiement
kubectl get all -n horaires-app

# Accéder à l'application (port-forward)
kubectl port-forward -n horaires-app svc/calcule-horaires-service 8501:8501
```

Consultez [argocd/README.md](argocd/README.md) pour le déploiement avec ArgoCD.

## Optimisations

### Réduire la Taille de l'Image

```dockerfile
# Utiliser une image de base plus petite
FROM python:3.11-alpine

# Multi-stage build
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
COPY . .
CMD ["streamlit", "run", "app.py"]
```

### Build Cache

```bash
# Utiliser BuildKit pour de meilleures performances
DOCKER_BUILDKIT=1 docker build -t calcule-horaires:latest .
```

### Sécurité

```bash
# Scanner les vulnérabilités
docker scan calcule-horaires:latest

# Ou avec Trivy
trivy image calcule-horaires:latest
```

## Dépannage

### L'application ne démarre pas

```bash
# Vérifier les logs
docker logs calcule-horaires

# Vérifier le health check
docker inspect calcule-horaires | grep -A 10 Health
```

### Port déjà utilisé

```bash
# Trouver le processus utilisant le port 8501
lsof -i :8501
# ou
netstat -tulpn | grep 8501

# Utiliser un autre port
docker run -p 9000:8501 calcule-horaires:latest
```

### Problèmes de permissions

```bash
# Vérifier les permissions des volumes
ls -la calcule_Heure/

# Corriger si nécessaire
sudo chown -R $USER:$USER calcule_Heure/
```

### Le conteneur redémarre en boucle

```bash
# Voir pourquoi il redémarre
docker inspect calcule-horaires | grep -A 20 State

# Désactiver le restart pour déboguer
docker update --restart=no calcule-horaires
```

### Problèmes de réseau

```bash
# Vérifier les réseaux Docker
docker network ls

# Inspecter le réseau
docker network inspect bridge

# Recréer le réseau
docker-compose down
docker network prune
docker-compose up -d
```

## Monitoring

### Métriques Docker

```bash
# Statistiques en temps réel
docker stats calcule-horaires

# Utilisation des ressources
docker inspect calcule-horaires | grep -A 10 Memory
```

### Logs Centralisés

Avec Docker Compose et un driver de logs:

```yaml
services:
  horaires-app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## Mise en Production

### Checklist

- [ ] Image testée localement
- [ ] Variables d'environnement configurées
- [ ] Volumes configurés pour la persistance
- [ ] Health checks activés
- [ ] Limites de ressources définies
- [ ] Logs configurés
- [ ] Monitoring en place
- [ ] Backups configurés

### Limites de Ressources

```bash
docker run -d \
  --name calcule-horaires \
  --memory="512m" \
  --cpus="0.5" \
  -p 8501:8501 \
  calcule-horaires:latest
```

### Stratégie de Mise à Jour

```bash
# 1. Pull la nouvelle version
docker pull calcule-horaires:v2.0.0

# 2. Arrêter l'ancienne version
docker stop calcule-horaires

# 3. Démarrer la nouvelle version
docker run -d \
  --name calcule-horaires-v2 \
  -p 8501:8501 \
  calcule-horaires:v2.0.0

# 4. Si OK, supprimer l'ancienne
docker rm calcule-horaires
docker rename calcule-horaires-v2 calcule-horaires

# 5. Nettoyer les anciennes images
docker image prune -a
```

## Ressources Utiles

- [Documentation Docker](https://docs.docker.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)

## Support

Pour toute question ou problème :
- Consultez les logs : `docker logs calcule-horaires`
- Ouvrez une issue sur GitHub
- Consultez la documentation complète dans [README.md](README.md)
