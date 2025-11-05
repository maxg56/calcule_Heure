# ⏰ Application de Gestion des Horaires

Application web interactive pour gérer et analyser vos horaires de travail. Calculez automatiquement votre heure de départ en fonction de vos heures d'arrivée et de pause, et visualisez vos statistiques avec des graphiques interactifs.

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=flat&logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![ArgoCD](https://img.shields.io/badge/ArgoCD-EF7B4D?style=flat&logo=argo&logoColor=white)](https://argo-cd.readthedocs.io/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)

## 🚀 Fonctionnalités

### Interface Web
- **Saisie intuitive des horaires** : Interface web simple pour enregistrer vos heures
- **Calcul automatique** : Calcule l'heure de départ basée sur la durée de travail configurée
- **Configuration personnalisable** : Ajustez la durée de travail et le seuil de pause via l'interface
- **Statistiques détaillées** : Moyennes d'arrivée, de départ et de durée de pause
- **Graphiques interactifs** :
  - Évolution des heures d'arrivée avec ligne de moyenne
  - Évolution des heures de départ avec ligne de moyenne
  - Durée des pauses avec code couleur dynamique (vert/rouge)
- **Tableau de données** : Visualisation complète de l'historique
- **Persistance des données** : Toutes les données sont sauvegardées automatiquement

### Onglet Configuration
- **Durée de travail personnalisable** : Définissez votre temps de travail quotidien (heures et minutes)
- **Seuil de pause configurable** : Ajustez la durée minimale de pause recommandée
- **Réinitialisation aux valeurs par défaut** : Retour rapide à la configuration initiale
- **Aide intégrée** : Explications détaillées de chaque paramètre

### Déploiement
- **Docker** : Conteneurisation complète de l'application
- **Kubernetes** : Manifestes prêts pour le déploiement
- **ArgoCD** : Configuration GitOps pour le déploiement continu
- **Haute disponibilité** : Health checks et probes configurés

## 📋 Prérequis

**Pour l'exécution locale:**
- Python 3.11 ou supérieur
- pip (gestionnaire de paquets Python)

**Pour Docker:**
- Docker >= 20.10
- Docker Compose >= 2.0 (optionnel)

**Pour Kubernetes:**
- Cluster Kubernetes fonctionnel
- kubectl configuré
- ArgoCD installé (optionnel)

## 🔧 Installation

### Option 1: Installation Locale

```bash
# 1. Cloner le projet
git clone https://github.com/maxg56/calcule_Heure.git
cd calcule_Heure

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
streamlit run app.py
# ou utiliser le Makefile
make run
```

### Option 2: Docker

```bash
# Méthode 1: Docker simple
docker build -t calcule-horaires .
docker run -d -p 8501:8501 calcule-horaires

# Méthode 2: Docker Compose (recommandé)
docker-compose up -d

# Méthode 3: Utiliser le Makefile
make docker-build
make docker-run

# Méthode 4: Script automatique
chmod +x build.sh
./build.sh
```

### Option 3: Kubernetes

Consultez le guide détaillé: [DOCKER.md](DOCKER.md) et [argocd/README.md](argocd/README.md)

```bash
# Déploiement simple
kubectl apply -f k8s/

# Avec ArgoCD
kubectl apply -f argocd/project.yaml
kubectl apply -f argocd/application.yaml

# Utiliser le Makefile
make k8s-deploy
```

## 🎯 Utilisation

### Interface Web

L'application s'ouvre automatiquement dans votre navigateur à `http://localhost:8501`

#### Onglet 1: "📝 Ajouter une Saisie"
1. Sélectionnez votre heure de début de travail
2. Sélectionnez votre heure de début de pause
3. Sélectionnez votre heure de fin de pause
4. Cliquez sur "💾 Enregistrer et Calculer"
5. L'application affiche automatiquement l'heure de départ calculée

#### Onglet 2: "📊 Analyser les Données"
- Consultez les statistiques moyennes (arrivée, départ, pause)
- Visualisez les graphiques d'évolution
- Accédez au tableau complet de vos données
- Exportez vos données si nécessaire

#### Onglet 3: "⚙️ Configuration"
- **Modifier la durée de travail**: Ajustez les heures et minutes de travail quotidien
- **Modifier le seuil de pause**: Définissez la durée minimale recommandée
- **Enregistrer les modifications**: Les changements s'appliquent immédiatement aux nouvelles saisies
- **Réinitialiser**: Retour aux valeurs par défaut (7h10 de travail, 45min de pause)

### Version Ligne de Commande

```bash
python main.py
```

Options du menu :
- **1** : Ajouter une nouvelle saisie
- **2** : Analyser les données et générer les graphiques
- **3** : Quitter

### Utilisation du Makefile

```bash
# Voir toutes les commandes disponibles
make help

# Commandes courantes
make install          # Installer les dépendances
make run             # Lancer l'application
make docker-build    # Build Docker
make docker-run      # Lancer avec Docker
make k8s-deploy      # Déployer sur Kubernetes
make argocd-deploy   # Déployer avec ArgoCD
make clean           # Nettoyer les fichiers temporaires
```

## 📁 Structure du Projet

```
calcule_Heure/
├── app.py                      # Application web Streamlit (PRINCIPALE)
├── main.py                     # Version ligne de commande
├── requirements.txt            # Dépendances Python
├── Dockerfile                  # Image Docker
├── docker-compose.yml          # Orchestration Docker
├── .dockerignore              # Exclusions Docker
├── Makefile                   # Commandes automatisées
├── build.sh                   # Script de build Docker
├── run.sh / run.bat          # Scripts de lancement
│
├── calcule_Heure/             # Module principal
│   ├── __init__.py
│   ├── config.py              # Module de configuration
│   ├── add_data.py            # Ajout de données
│   ├── colcul.py              # Calcul des moyennes
│   ├── graphique.py           # Génération des graphiques
│   ├── open_csv.py            # Lecture du CSV
│   ├── utiles.py              # Fonctions utilitaires
│   ├── horaires.csv           # Fichier de données
│   └── config.json            # Configuration de l'app
│
├── k8s/                       # Manifestes Kubernetes
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── pvc.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── kustomization.yaml
│
├── argocd/                    # Configuration ArgoCD
│   ├── application.yaml
│   ├── project.yaml
│   └── README.md
│
├── .streamlit/                # Configuration Streamlit
│   └── config.toml
│
└── docs/                      # Documentation
    ├── README.md              # Ce fichier
    ├── QUICKSTART.md          # Guide de démarrage rapide
    └── DOCKER.md              # Guide Docker complet
```

## 📊 Configuration

### Fichier config.json

Le fichier `calcule_Heure/config.json` contient les paramètres de l'application:

```json
{
  "duree_travail_heures": 7,
  "duree_travail_minutes": 10,
  "seuil_pause_minutes": 45,
  "format_heure": "%H:%M",
  "format_date": "%Y-%m-%d %H:%M:%S"
}
```

**Modification via l'interface web (recommandé):**
- Allez dans l'onglet "⚙️ Configuration"
- Modifiez les valeurs
- Cliquez sur "💾 Enregistrer"

**Modification manuelle:**
- Éditez directement le fichier `config.json`
- Redémarrez l'application

### Variables d'Environnement Docker

```bash
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

## 🐳 Docker

### Build et Exécution

```bash
# Build
docker build -t calcule-horaires:latest .

# Run simple
docker run -d -p 8501:8501 calcule-horaires:latest

# Run avec volumes (persistance)
docker run -d -p 8501:8501 \
  -v $(pwd)/calcule_Heure/horaires.csv:/app/calcule_Heure/horaires.csv \
  -v $(pwd)/calcule_Heure/config.json:/app/calcule_Heure/config.json \
  calcule-horaires:latest
```

### Docker Compose

```bash
# Démarrer
docker-compose up -d

# Logs
docker-compose logs -f

# Arrêter
docker-compose down
```

Consultez le guide complet: [DOCKER.md](DOCKER.md)

## ☸️ Kubernetes & ArgoCD

### Déploiement Kubernetes

```bash
# Déployer toutes les ressources
kubectl apply -f k8s/

# Vérifier le déploiement
kubectl get all -n horaires-app

# Accéder à l'application (port-forward)
kubectl port-forward -n horaires-app svc/calcule-horaires-service 8501:8501
```

### Déploiement ArgoCD

```bash
# Créer le projet et l'application
kubectl apply -f argocd/project.yaml
kubectl apply -f argocd/application.yaml

# Synchroniser
argocd app sync calcule-horaires

# Voir le statut
argocd app get calcule-horaires
```

**Guide complet:** [argocd/README.md](argocd/README.md)

## 🔧 Configuration Avancée

### Personnalisation de la Durée de Travail

La durée de travail par défaut est **7h10**. Pour la modifier:

**Via l'interface (recommandé):**
1. Allez dans l'onglet "⚙️ Configuration"
2. Modifiez "Durée de travail quotidienne"
3. Cliquez sur "💾 Enregistrer"

**Via le code:**
- Éditez `calcule_Heure/config.py`
- Modifiez `DEFAULT_CONFIG["duree_travail_heures"]` et `DEFAULT_CONFIG["duree_travail_minutes"]`

### Personnalisation du Seuil de Pause

Le seuil de pause par défaut est **45 minutes**. Pour le modifier:

**Via l'interface (recommandé):**
1. Allez dans l'onglet "⚙️ Configuration"
2. Modifiez "Durée minimale de pause recommandée"
3. Cliquez sur "💾 Enregistrer"

**Via le code:**
- Éditez `calcule_Heure/config.py`
- Modifiez `DEFAULT_CONFIG["seuil_pause_minutes"]`

## 📝 Format des Données

Les données sont stockées dans `calcule_Heure/horaires.csv`:

| Colonne | Description | Format |
|---------|-------------|--------|
| Date de saisie | Date et heure de la saisie | YYYY-MM-DD HH:MM:SS |
| Heure début | Heure de début de travail | HH:MM |
| Heure début pause | Heure de début de pause | HH:MM |
| Heure fin pause | Heure de fin de pause | HH:MM |
| Heure départ calculée | Heure de départ calculée | HH:MM |

## 🎨 Thème et Personnalisation

Le thème Streamlit est configurable dans `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

## 🧪 Tests

```bash
# Exécuter les tests
make test

# Avec couverture
python -m pytest tests/ -v --cov=calcule_Heure

# Lint
make lint
```

## 🚀 Déploiement en Production

### Checklist

- [ ] Configuration personnalisée définie
- [ ] Données de test supprimées
- [ ] Image Docker buildée et testée
- [ ] Variables d'environnement configurées
- [ ] Volumes configurés pour la persistance
- [ ] Health checks testés
- [ ] Limites de ressources définies
- [ ] Monitoring configuré
- [ ] Backups configurés
- [ ] Documentation à jour

### Bonnes Pratiques

1. **Sécurité**:
   - Ne pas exposer directement l'application (utiliser un reverse proxy)
   - Activer HTTPS via Ingress avec cert-manager
   - Limiter les ressources (CPU, mémoire)

2. **Persistance**:
   - Utiliser des PersistentVolumes pour les données
   - Configurer des backups réguliers
   - Tester les procédures de restauration

3. **Monitoring**:
   - Configurer des alertes sur les health checks
   - Surveiller l'utilisation des ressources
   - Logger les erreurs importantes

## 🐛 Dépannage

### L'application ne démarre pas

```bash
# Vérifier les logs
docker logs calcule-horaires
# ou
kubectl logs -n horaires-app -l app=calcule-horaires

# Vérifier les dépendances
pip list
```

### Le fichier CSV n'est pas trouvé

- Le fichier `horaires.csv` est créé automatiquement lors de la première saisie
- Vérifiez les permissions d'écriture: `ls -la calcule_Heure/`

### Les graphiques ne s'affichent pas

- Vérifiez que matplotlib est installé: `pip list | grep matplotlib`
- Assurez-vous d'avoir au moins une entrée de données
- Vérifiez les logs pour les erreurs

### Problèmes de configuration

```bash
# Réinitialiser la configuration
rm calcule_Heure/config.json
# Redémarrer l'application

# Ou via l'interface
# Allez dans Configuration → Réinitialiser
```

## 📚 Documentation

- [Guide de Démarrage Rapide](QUICKSTART.md)
- [Guide Docker Complet](DOCKER.md)
- [Guide ArgoCD](argocd/README.md)
- [Documentation Streamlit](https://docs.streamlit.io/)

## 🤝 Contribution

Les contributions sont les bienvenues! Pour contribuer:

1. Forkez le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est open source et disponible sous licence MIT.

## 👥 Auteurs

- **Développement initial** - [maxg56](https://github.com/maxg56)

## 🙏 Remerciements

- Streamlit pour le framework d'interface web
- La communauté Python pour les bibliothèques
- ArgoCD pour le déploiement GitOps

## 📧 Support

Pour toute question ou problème:
- 📖 Consultez la [documentation](DOCKER.md)
- 🐛 Ouvrez une [issue sur GitHub](https://github.com/maxg56/calcule_Heure/issues)
- 📝 Consultez les [logs](#dépannage)

---

**Bon calcul d'horaires!** ⏰✨
