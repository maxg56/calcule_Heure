.PHONY: help install run test docker-build docker-run docker-stop docker-clean k8s-deploy k8s-delete argocd-deploy

# Variables
IMAGE_NAME := calcule-horaires
IMAGE_TAG := latest
REGISTRY ?=
NAMESPACE := horaires-app

help: ## Affiche cette aide
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# === Installation et Exécution Locale ===

install: ## Installe les dépendances Python
	pip install -r requirements.txt

run: ## Lance l'application en local
	streamlit run app.py

run-cli: ## Lance la version CLI
	python main.py

# === Docker ===

docker-build: ## Build l'image Docker
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

docker-run: ## Lance le conteneur Docker
	docker run -d --name $(IMAGE_NAME) -p 8501:8501 \
		-v $$(pwd)/calcule_Heure/horaires.csv:/app/calcule_Heure/horaires.csv \
		-v $$(pwd)/calcule_Heure/config.json:/app/calcule_Heure/config.json \
		$(IMAGE_NAME):$(IMAGE_TAG)

docker-stop: ## Arrête le conteneur Docker
	docker stop $(IMAGE_NAME) || true

docker-clean: docker-stop ## Nettoie les conteneurs et images
	docker rm $(IMAGE_NAME) || true
	docker rmi $(IMAGE_NAME):$(IMAGE_TAG) || true

docker-logs: ## Affiche les logs du conteneur
	docker logs -f $(IMAGE_NAME)

docker-shell: ## Ouvre un shell dans le conteneur
	docker exec -it $(IMAGE_NAME) bash

# === Docker Compose ===

compose-up: ## Lance avec Docker Compose
	docker-compose up -d

compose-down: ## Arrête Docker Compose
	docker-compose down

compose-logs: ## Affiche les logs Docker Compose
	docker-compose logs -f

compose-restart: ## Redémarre les services
	docker-compose restart

# === Kubernetes ===

k8s-deploy: ## Déploie sur Kubernetes
	kubectl apply -f k8s/

k8s-delete: ## Supprime de Kubernetes
	kubectl delete -f k8s/

k8s-status: ## Affiche le statut Kubernetes
	kubectl get all -n $(NAMESPACE)

k8s-logs: ## Affiche les logs Kubernetes
	kubectl logs -n $(NAMESPACE) -l app=calcule-horaires --tail=100 -f

k8s-port-forward: ## Port-forward pour accéder à l'app
	kubectl port-forward -n $(NAMESPACE) svc/calcule-horaires-service 8501:8501

# === ArgoCD ===

argocd-deploy: ## Déploie avec ArgoCD
	kubectl apply -f argocd/project.yaml
	kubectl apply -f argocd/application.yaml

argocd-sync: ## Synchronise l'application ArgoCD
	argocd app sync calcule-horaires

argocd-status: ## Affiche le statut ArgoCD
	argocd app get calcule-horaires

argocd-delete: ## Supprime l'application ArgoCD
	kubectl delete -f argocd/application.yaml
	kubectl delete -f argocd/project.yaml

# === Tests et Validation ===

test: ## Teste l'application
	python -m pytest tests/ -v

lint: ## Vérifie le code avec flake8
	flake8 calcule_Heure/ --max-line-length=120

format: ## Formate le code avec black
	black calcule_Heure/ app.py main.py

validate-k8s: ## Valide les manifestes Kubernetes
	kubectl apply --dry-run=client -f k8s/

# === Nettoyage ===

clean: ## Nettoie les fichiers temporaires
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete

clean-all: clean docker-clean ## Nettoyage complet

# === Push Registry ===

docker-tag: ## Tag l'image pour un registry
	@if [ -z "$(REGISTRY)" ]; then \
		echo "Erreur: REGISTRY n'est pas défini"; \
		echo "Usage: make docker-tag REGISTRY=ghcr.io/username"; \
		exit 1; \
	fi
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)

docker-push: docker-tag ## Push l'image vers un registry
	docker push $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)

# === Utilitaires ===

version: ## Affiche la version
	@echo "Application: Calcule Horaires"
	@echo "Version: $(IMAGE_TAG)"
	@git describe --tags --always 2>/dev/null || echo "No git tags"

deps-check: ## Vérifie les dépendances
	pip list --outdated

backup-data: ## Sauvegarde les données
	@mkdir -p backups
	@cp calcule_Heure/horaires.csv backups/horaires_$$(date +%Y%m%d_%H%M%S).csv
	@cp calcule_Heure/config.json backups/config_$$(date +%Y%m%d_%H%M%S).json 2>/dev/null || true
	@echo "Backup créé dans backups/"

# === CI/CD ===

ci-build: ## Build pour CI/CD
	@echo "Building Docker image..."
	docker build --no-cache -t $(IMAGE_NAME):$(IMAGE_TAG) .

ci-test: ## Tests pour CI/CD
	@echo "Running tests..."
	python -m pytest tests/ -v --cov=calcule_Heure

ci-publish: docker-push ## Publie l'image
	@echo "Image published to $(REGISTRY)"
