#!/bin/bash
# Script de lancement de l'application web

echo "🚀 Démarrage de l'application de gestion des horaires..."
echo ""

# Vérifier si streamlit est installé
if ! command -v streamlit &> /dev/null
then
    echo "⚠️  Streamlit n'est pas installé. Installation en cours..."
    pip install -r requirements.txt
fi

# Lancer l'application
echo "📊 Ouverture de l'application web..."
streamlit run app.py
