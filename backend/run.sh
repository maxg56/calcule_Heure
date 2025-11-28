#!/bin/bash

# Script de démarrage du backend FastAPI

echo "🚀 Démarrage du backend FastAPI..."

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
echo "🔌 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "📥 Installation des dépendances..."
pip install -r requirements.txt

# Démarrer l'application
echo "✅ Lancement de l'application..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
