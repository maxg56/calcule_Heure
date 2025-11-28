# Guide Docker - Application Calcule Horaires

Ce guide vous explique comment construire, exécuter et déployer l'application avec Docker.

## Table des Matières

- [Prérequis](#prérequis)
- [Build de l'Image](#build-de-limage)
- [Exécution Locale](#exécution-locale)
- [Docker Compose](#docker-compose)
- [Configuration](#configuration)
- [Optimisations](#optimisations)
- [Dépannage](#dépannage)
- [Monitoring](#monitoring)
- [Mise en Production](#mise-en-production)

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

# Voir la taille de l'image
docker images calcule-horaires --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
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

### Lancement avec Limites de Ressources

```bash
docker run -d \
  --name calcule-horaires \
  -p 8501:8501 \
  --memory="512m" \
  --cpus="0.5" \
  calcule-horaires:latest
```

### Commandes Utiles

```bash
# Voir les logs
docker logs calcule-horaires

# Logs en temps réel
docker logs -f calcule-horaires

# Logs des 100 dernières lignes
docker logs --tail 100 calcule-horaires

# Arrêter le conteneur
docker stop calcule-horaires

# Redémarrer le conteneur
docker restart calcule-horaires

# Supprimer le conteneur
docker stop calcule-horaires
docker rm calcule-horaires

# Entrer dans le conteneur
docker exec -it calcule-horaires bash

# Voir les statistiques en temps réel
docker stats calcule-horaires

# Inspecter le conteneur
docker inspect calcule-horaires

# Voir les processus dans le conteneur
docker top calcule-horaires
```

## Docker Compose

### Lancement

```bash
# Démarrer l'application
docker-compose up -d

# Démarrer avec rebuild
docker-compose up -d --build

# Voir les logs
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs -f horaires-app

# Arrêter l'application
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v

# Redémarrer un service
docker-compose restart horaires-app

# Voir l'état des services
docker-compose ps

# Voir les statistiques
docker-compose stats
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
    volumes:
      - ./custom-data:/app/data
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

### Fichier .env (optionnel)

Créez un fichier `.env` à la racine du projet:

```bash
# Configuration Streamlit
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Configuration application
DUREE_TRAVAIL_HEURES=7
DUREE_TRAVAIL_MINUTES=10
SEUIL_PAUSE_MINUTES=45
```

Puis modifiez `docker-compose.yml`:

```yaml
services:
  horaires-app:
    env_file:
      - .env
```

## Optimisations

### Réduire la Taille de l'Image

Le Dockerfile actuel utilise `python:3.11-slim` qui est déjà optimisé.

Pour une optimisation supplémentaire, utilisez Alpine:

```dockerfile
FROM python:3.11-alpine

# Installer les dépendances de compilation
RUN apk add --no-cache gcc musl-dev linux-headers

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

### Multi-stage Build

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

### Build Cache avec BuildKit

```bash
# Activer BuildKit pour de meilleures performances
DOCKER_BUILDKIT=1 docker build -t calcule-horaires:latest .

# Avec cache depuis une image existante
docker build --cache-from calcule-horaires:latest -t calcule-horaires:v2 .
```

### Compression d'Image

```bash
# Utiliser docker-squash pour compresser les layers
pip install docker-squash
docker-squash calcule-horaires:latest -t calcule-horaires:squashed
```

## Dépannage

### L'application ne démarre pas

```bash
# Vérifier les logs
docker logs calcule-horaires

# Vérifier le health check
docker inspect calcule-horaires | grep -A 10 Health

# Vérifier les variables d'environnement
docker exec calcule-horaires env

# Tester manuellement le démarrage
docker run -it --rm calcule-horaires:latest bash
streamlit run app.py
```

### Port déjà utilisé

```bash
# Trouver le processus utilisant le port 8501
lsof -i :8501
# ou
netstat -tulpn | grep 8501

# Utiliser un autre port
docker run -p 9000:8501 calcule-horaires:latest

# Ou modifier docker-compose.yml
ports:
  - "9000:8501"
```

### Problèmes de permissions

```bash
# Vérifier les permissions des volumes
ls -la calcule_Heure/

# Corriger si nécessaire
sudo chown -R $USER:$USER calcule_Heure/

# Vérifier l'utilisateur dans le conteneur
docker exec calcule-horaires whoami
docker exec calcule-horaires id
```

### Le conteneur redémarre en boucle

```bash
# Voir pourquoi il redémarre
docker inspect calcule-horaires | grep -A 20 State

# Vérifier les logs d'erreur
docker logs --tail 50 calcule-horaires

# Désactiver le restart pour déboguer
docker update --restart=no calcule-horaires

# Lancer en mode interactif
docker run -it --rm calcule-horaires:latest bash
```

### Problèmes de réseau

```bash
# Vérifier les réseaux Docker
docker network ls

# Inspecter le réseau
docker network inspect bridge

# Créer un réseau personnalisé
docker network create horaires-net
docker run -d --network horaires-net --name calcule-horaires calcule-horaires:latest

# Tester la connectivité
docker exec calcule-horaires ping google.com
```

### Volumes ne se montent pas

```bash
# Vérifier les volumes
docker volume ls

# Inspecter un volume
docker volume inspect <volume-name>

# Créer un volume nommé
docker volume create horaires-data

# Utiliser le volume
docker run -d -v horaires-data:/app/calcule_Heure calcule-horaires:latest

# Supprimer les volumes non utilisés
docker volume prune
```

### Image trop grande

```bash
# Analyser les layers de l'image
docker history calcule-horaires:latest

# Utiliser dive pour une analyse détaillée
brew install dive  # macOS
dive calcule-horaires:latest

# Nettoyer les images
docker image prune -a
```

## Monitoring

### Métriques Docker

```bash
# Statistiques en temps réel
docker stats calcule-horaires

# Statistiques formatées
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Utilisation des ressources
docker inspect calcule-horaires | grep -A 10 Memory

# Voir les événements Docker
docker events --filter container=calcule-horaires
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

### Health Checks

Le Dockerfile inclut déjà un health check. Pour le vérifier:

```bash
# Voir l'état du health check
docker inspect calcule-horaires | grep -A 10 Health

# Logs du health check
docker inspect calcule-horaires --format='{{json .State.Health}}' | jq
```

### Exportation des Logs

```bash
# Exporter les logs dans un fichier
docker logs calcule-horaires > app.log 2>&1

# Exporter avec timestamp
docker logs calcule-horaires --timestamps > app.log 2>&1
```

## Push vers un Registry

### Docker Hub

```bash
# Se connecter
docker login

# Tag l'image
docker tag calcule-horaires:latest username/calcule-horaires:latest

# Push
docker push username/calcule-horaires:latest
```

### GitHub Container Registry

```bash
# Se connecter
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Tag l'image
docker tag calcule-horaires:latest ghcr.io/username/calcule-horaires:latest

# Push
docker push ghcr.io/username/calcule-horaires:latest
```

### Registry Privé

```bash
# Se connecter à un registry privé
docker login registry.example.com

# Tag
docker tag calcule-horaires:latest registry.example.com/calcule-horaires:latest

# Push
docker push registry.example.com/calcule-horaires:latest
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
- [ ] Reverse proxy configuré (Nginx/Traefik)
- [ ] HTTPS activé
- [ ] Documentation à jour

### Exemple de Configuration Production

**docker-compose.prod.yml:**

```yaml
version: '3.8'

services:
  horaires-app:
    image: calcule-horaires:latest
    container_name: calcule-horaires-prod
    restart: unless-stopped

    ports:
      - "127.0.0.1:8501:8501"  # Seulement local, exposé via reverse proxy

    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
      - STREAMLIT_SERVER_HEADLESS=true

    volumes:
      - horaires-data:/app/calcule_Heure

    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M

    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

    networks:
      - horaires-network

volumes:
  horaires-data:
    driver: local

networks:
  horaires-network:
    driver: bridge
```

### Reverse Proxy avec Nginx

**nginx.conf:**

```nginx
upstream streamlit {
    server localhost:8501;
}

server {
    listen 80;
    server_name horaires.example.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name horaires.example.com;

    # SSL Configuration
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    location / {
        proxy_pass http://streamlit;
        proxy_http_version 1.1;

        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

### Stratégie de Mise à Jour

#### Blue-Green Deployment

```bash
# 1. Lancer la nouvelle version (green)
docker run -d --name calcule-horaires-green -p 8502:8501 calcule-horaires:v2

# 2. Tester la nouvelle version
curl http://localhost:8502/_stcore/health

# 3. Basculer le trafic (modifier reverse proxy ou port mapping)
docker stop calcule-horaires
docker run -d --name calcule-horaires-new -p 8501:8501 calcule-horaires:v2

# 4. Si OK, supprimer l'ancienne version
docker rm calcule-horaires-green
docker rm calcule-horaires
```

#### Rolling Update

```bash
# Avec docker-compose
docker-compose pull
docker-compose up -d --no-deps --build horaires-app
```

### Sauvegardes

```bash
# Script de backup automatique
#!/bin/bash
BACKUP_DIR="/backups/horaires"
DATE=$(date +%Y%m%d_%H%M%S)

# Créer le répertoire de backup
mkdir -p $BACKUP_DIR

# Backup des données
docker cp calcule-horaires:/app/calcule_Heure/horaires.csv \
  $BACKUP_DIR/horaires_${DATE}.csv

docker cp calcule-horaires:/app/calcule_Heure/config.json \
  $BACKUP_DIR/config_${DATE}.json

# Compresser
tar -czf $BACKUP_DIR/backup_${DATE}.tar.gz \
  $BACKUP_DIR/horaires_${DATE}.csv \
  $BACKUP_DIR/config_${DATE}.json

# Nettoyer les backups de plus de 30 jours
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +30 -delete

echo "Backup completed: backup_${DATE}.tar.gz"
```

Ajoutez ce script dans un cron:

```bash
# Backup quotidien à 2h du matin
0 2 * * * /path/to/backup.sh
```

## Sécurité

### Scanner les Vulnérabilités

```bash
# Avec Docker scan
docker scan calcule-horaires:latest

# Avec Trivy
trivy image calcule-horaires:latest

# Avec Snyk
snyk container test calcule-horaires:latest
```

### Bonnes Pratiques

1. **Utilisateur non-root**: Le Dockerfile utilise déjà un utilisateur non-root
2. **Pas de secrets dans l'image**: Utilisez des variables d'environnement
3. **Mettre à jour régulièrement**: Rebuild l'image avec les dernières dépendances
4. **Limiter les ressources**: Définir des limites CPU/mémoire
5. **Réseau isolé**: Utiliser des réseaux Docker personnalisés

## Ressources Utiles

- [Documentation Docker](https://docs.docker.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Docker Security](https://docs.docker.com/engine/security/)

## Support

Pour toute question ou problème :
- Consultez les logs : `docker logs calcule-horaires`
- Ouvrez une issue sur GitHub
- Consultez la documentation complète dans [README.md](README.md)

---

**Happy Dockerizing!** 🐳
