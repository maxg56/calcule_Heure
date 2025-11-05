#!/bin/bash
# Script de build Docker pour l'application Calcule Horaires

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="calcule-horaires"
IMAGE_TAG="${1:-latest}"
REGISTRY="${REGISTRY:-}"

echo -e "${GREEN}=== Build Docker Image ===${NC}"
echo "Image: ${IMAGE_NAME}:${IMAGE_TAG}"

# Vérifier que Docker est installé
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker n'est pas installé${NC}"
    exit 1
fi

# Build de l'image
echo -e "${YELLOW}🔨 Construction de l'image Docker...${NC}"
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Image construite avec succès${NC}"
else
    echo -e "${RED}❌ Échec de la construction${NC}"
    exit 1
fi

# Afficher les informations de l'image
echo -e "\n${GREEN}=== Informations de l'image ===${NC}"
docker images ${IMAGE_NAME}:${IMAGE_TAG}

# Si un registry est défini, pousser l'image
if [ -n "$REGISTRY" ]; then
    echo -e "\n${YELLOW}📤 Push vers le registry: ${REGISTRY}${NC}"

    # Tag avec le registry
    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}

    # Push
    docker push ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Image poussée avec succès vers ${REGISTRY}${NC}"
    else
        echo -e "${RED}❌ Échec du push${NC}"
        exit 1
    fi
fi

# Option pour tester l'image localement
read -p "Voulez-vous tester l'image localement ? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "\n${YELLOW}🚀 Lancement du conteneur...${NC}"
    docker run -d -p 8501:8501 --name calcule-horaires-test ${IMAGE_NAME}:${IMAGE_TAG}

    echo -e "${GREEN}✅ Conteneur démarré${NC}"
    echo "Accédez à l'application sur: http://localhost:8501"
    echo ""
    echo "Pour arrêter le conteneur:"
    echo "  docker stop calcule-horaires-test"
    echo "  docker rm calcule-horaires-test"
fi

echo -e "\n${GREEN}=== Build terminé ===${NC}"
