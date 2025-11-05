# Configuration ArgoCD pour Calcule Horaires

Ce répertoire contient les configurations ArgoCD pour déployer l'application de gestion des horaires.

## Prérequis

1. **Cluster Kubernetes** fonctionnel
2. **ArgoCD** installé sur le cluster
3. **kubectl** configuré pour accéder au cluster
4. Accès au repository Git contenant les manifestes

## Installation d'ArgoCD

Si ArgoCD n'est pas encore installé sur votre cluster :

```bash
# Créer le namespace ArgoCD
kubectl create namespace argocd

# Installer ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Attendre que tous les pods soient prêts
kubectl wait --for=condition=ready pod --all -n argocd --timeout=300s

# Exposer l'interface web ArgoCD (port-forward)
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Accédez à ArgoCD : https://localhost:8080

## Configuration Initiale

### 1. Récupérer le mot de passe admin

```bash
# Le mot de passe admin initial
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### 2. Se connecter à ArgoCD

```bash
# Installer l'outil CLI ArgoCD
brew install argocd  # macOS
# ou
curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
chmod +x /usr/local/bin/argocd

# Se connecter
argocd login localhost:8080
```

## Déploiement de l'Application

### Méthode 1 : Via kubectl (Recommandé)

```bash
# Créer le projet ArgoCD (optionnel)
kubectl apply -f argocd/project.yaml

# Créer l'application ArgoCD
kubectl apply -f argocd/application.yaml
```

### Méthode 2 : Via l'interface web ArgoCD

1. Connectez-vous à l'interface web ArgoCD
2. Cliquez sur "+ NEW APP"
3. Remplissez les champs :
   - **Application Name**: calcule-horaires
   - **Project**: default (ou horaires-project si créé)
   - **Sync Policy**: Automatic
   - **Repository URL**: https://github.com/maxg56/calcule_Heure.git
   - **Revision**: main
   - **Path**: k8s
   - **Cluster**: https://kubernetes.default.svc
   - **Namespace**: horaires-app
4. Cochez "Auto-Create Namespace"
5. Cliquez sur "CREATE"

### Méthode 3 : Via ArgoCD CLI

```bash
argocd app create calcule-horaires \
  --repo https://github.com/maxg56/calcule_Heure.git \
  --path k8s \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace horaires-app \
  --sync-policy automated \
  --auto-prune \
  --self-heal
```

## Vérification du Déploiement

```bash
# Vérifier le statut de l'application ArgoCD
argocd app get calcule-horaires

# Vérifier les ressources Kubernetes
kubectl get all -n horaires-app

# Vérifier les logs
kubectl logs -n horaires-app -l app=calcule-horaires --tail=100

# Vérifier la synchronisation
argocd app sync calcule-horaires
```

## Accès à l'Application

### Via Port-Forward

```bash
kubectl port-forward -n horaires-app svc/calcule-horaires-service 8501:8501
```

Accédez à : http://localhost:8501

### Via Ingress

Si vous avez configuré un Ingress :

1. Modifiez `k8s/ingress.yaml` avec votre domaine
2. Assurez-vous qu'un Ingress Controller est installé (NGINX, Traefik, etc.)
3. Accédez à : http://horaires.example.com

## Gestion de l'Application

### Synchronisation Manuelle

```bash
# Synchroniser l'application
argocd app sync calcule-horaires

# Synchronisation avec force (en cas de conflit)
argocd app sync calcule-horaires --force
```

### Voir les Différences

```bash
# Voir les différences entre Git et le cluster
argocd app diff calcule-horaires
```

### Rollback

```bash
# Lister l'historique
argocd app history calcule-horaires

# Rollback à une révision spécifique
argocd app rollback calcule-horaires <REVISION_ID>
```

### Suppression

```bash
# Supprimer l'application (garde les ressources)
argocd app delete calcule-horaires

# Supprimer l'application et ses ressources
argocd app delete calcule-horaires --cascade
```

## Configuration Avancée

### Activer les Notifications

Ajoutez cette annotation à `application.yaml` :

```yaml
metadata:
  annotations:
    notifications.argoproj.io/subscribe.on-sync-succeeded.slack: my-channel
```

### Webhooks GitHub

Pour activer la synchronisation automatique sur push :

1. Configurez un webhook dans GitHub pointant vers ArgoCD
2. URL : `https://<argocd-server>/api/webhook`
3. Secret : Configuré dans ArgoCD

### Health Checks Personnalisés

Ajoutez à `application.yaml` :

```yaml
spec:
  ignoreDifferences:
  - group: apps
    kind: Deployment
    jsonPointers:
    - /spec/replicas
```

## Dépannage

### L'application ne se synchronise pas

```bash
# Vérifier les logs ArgoCD
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-application-controller

# Forcer la synchronisation
argocd app sync calcule-horaires --force --prune
```

### Erreur de permissions

Vérifiez que le ServiceAccount ArgoCD a les permissions nécessaires :

```bash
kubectl describe clusterrole argocd-application-controller
```

### Problèmes de santé

```bash
# Vérifier la santé de l'application
argocd app get calcule-horaires --refresh

# Vérifier les événements Kubernetes
kubectl get events -n horaires-app --sort-by='.lastTimestamp'
```

## Bonnes Pratiques

1. **Utilisez des branches Git** pour les environnements (dev, staging, prod)
2. **Activez la synchronisation automatique** pour des déploiements continus
3. **Configurez des health checks** pour surveiller l'état de l'application
4. **Utilisez des secrets Kubernetes** pour les données sensibles
5. **Activez les notifications** pour être alerté des changements
6. **Documentez les changements** dans les commits Git
7. **Testez dans un environnement de staging** avant la production

## Ressources Utiles

- [Documentation ArgoCD](https://argo-cd.readthedocs.io/)
- [ArgoCD Best Practices](https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/)
- [GitOps Principles](https://www.gitops.tech/)

## Support

Pour toute question ou problème :
- Consultez la [documentation ArgoCD](https://argo-cd.readthedocs.io/)
- Ouvrez une issue sur GitHub
- Contactez l'équipe DevOps
