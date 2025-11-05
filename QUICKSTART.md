# 🚀 Guide de Démarrage Rapide

## Installation en 3 étapes

### 1. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 2. Lancer l'application
**Linux/Mac:**
```bash
./run.sh
```

**Windows:**
```bash
run.bat
```

**Ou directement:**
```bash
streamlit run app.py
```

### 3. Utiliser l'application
L'application s'ouvre automatiquement dans votre navigateur à l'adresse: `http://localhost:8501`

## Première utilisation

### Ajouter une saisie
1. Allez dans l'onglet "📝 Ajouter une Saisie"
2. Sélectionnez vos horaires:
   - Heure de début de travail (ex: 08:00)
   - Heure de début de pause (ex: 12:00)
   - Heure de fin de pause (ex: 12:45)
3. Cliquez sur "💾 Enregistrer et Calculer"
4. L'application vous indique à quelle heure vous devez partir

### Analyser vos données
1. Allez dans l'onglet "📊 Analyser les Données"
2. Consultez:
   - Les statistiques moyennes (arrivée, départ, pause)
   - Les graphiques d'évolution
   - Le tableau complet de vos données

## Astuces

- **Durée de travail**: L'application calcule automatiquement une journée de 7h10 de travail effectif
- **Code couleur des pauses**:
  - 🟢 Vert = pause ≥ 45 minutes (recommandé)
  - 🔴 Rouge = pause < 45 minutes
- **Données persistantes**: Toutes vos saisies sont sauvegardées dans `calcule_Heure/horaires.csv`

## Support

Pour toute question, consultez le [README.md](README.md) complet ou ouvrez une issue sur GitHub.

---

Bon calcul d'horaires! ⏰
