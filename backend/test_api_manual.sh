#!/bin/bash

# Script de test manuel de l'API FastAPI
# Usage: ./test_api_manual.sh

BASE_URL="http://localhost:8000"

echo "🧪 Test de l'API Calcule Heure"
echo "================================"
echo ""

# Test 1: Health Check
echo "1️⃣  Test Health Check..."
curl -s ${BASE_URL}/api/health | python3 -m json.tool
echo ""
echo ""

# Test 2: Création d'horaire
echo "2️⃣  Test Création d'horaire..."
curl -s -X POST ${BASE_URL}/api/schedules/ \
  -H "Content-Type: application/json" \
  -d '{
    "heure_debut": "09:00:00",
    "heure_pause_debut": "12:30:00",
    "heure_pause_fin": "13:15:00"
  }' | python3 -m json.tool
echo ""
echo ""

# Test 3: Liste des horaires
echo "3️⃣  Test Liste des horaires..."
curl -s ${BASE_URL}/api/schedules/ | python3 -m json.tool
echo ""
echo ""

# Test 4: Statistiques
echo "4️⃣  Test Statistiques..."
curl -s ${BASE_URL}/api/statistics/ | python3 -m json.tool
echo ""
echo ""

# Test 5: Configuration
echo "5️⃣  Test Configuration..."
curl -s ${BASE_URL}/api/config/ | python3 -m json.tool
echo ""
echo ""

echo "✅ Tests terminés!"
echo ""
echo "📚 Documentation interactive: ${BASE_URL}/docs"
