# ⏰ Application de Gestion des Horaires

Application web interactive pour gérer et analyser vos horaires de travail. Calculez automatiquement votre heure de départ en fonction de vos heures d'arrivée et de pause, et visualisez vos statistiques avec des graphiques interactifs.

## 🚀 Fonctionnalités

- **Saisie intuitive des horaires** : Interface web simple pour enregistrer vos heures
- **Calcul automatique** : Calcule l'heure de départ basée sur 7h10 de travail effectif
- **Statistiques détaillées** : Moyennes d'arrivée, de départ et de durée de pause
- **Graphiques interactifs** :
  - Évolution des heures d'arrivée
  - Évolution des heures de départ
  - Durée des pauses avec code couleur (vert = ≥45min, rouge = <45min)
- **Tableau de données** : Visualisation complète de l'historique

## 📋 Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

## 🔧 Installation

1. **Cloner le projet**
```bash
git clone <votre-repo>
cd calcule_Heure
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

## 🎯 Utilisation

### Version Web (recommandée)

Lancez l'application web avec Streamlit :

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

#### Interface Web

**Onglet "Ajouter une Saisie"**
1. Sélectionnez votre heure de début de travail
2. Sélectionnez votre heure de début de pause
3. Sélectionnez votre heure de fin de pause
4. Cliquez sur "Enregistrer et Calculer"
5. L'application affiche automatiquement l'heure de départ calculée

**Onglet "Analyser les Données"**
- Consultez les statistiques moyennes (arrivée, départ, pause)
- Visualisez les graphiques d'évolution
- Accédez au tableau complet de vos données

### Version Ligne de Commande

Pour utiliser la version en ligne de commande :

```bash
python main.py
```

Options du menu :
- **1** : Ajouter une nouvelle saisie
- **2** : Analyser les données et générer les graphiques
- **3** : Quitter

## 📁 Structure du Projet

```
calcule_Heure/
├── app.py                      # Application web Streamlit
├── main.py                     # Version ligne de commande
├── requirements.txt            # Dépendances Python
├── README.md                   # Ce fichier
├── calcule_Heure/
│   ├── __init__.py
│   ├── add_data.py            # Ajout de données
│   ├── colcul.py              # Calcul des moyennes
│   ├── graphique.py           # Génération des graphiques
│   ├── open_csv.py            # Lecture du CSV
│   ├── utiles.py              # Fonctions utilitaires
│   └── horaires.csv           # Fichier de données (créé automatiquement)
```

## 📊 Format des Données

Les données sont stockées dans un fichier CSV (`calcule_Heure/horaires.csv`) avec les colonnes suivantes :
- Date de saisie
- Heure début
- Heure début pause
- Heure fin pause
- Heure départ calculée

## ⚙️ Paramètres

- **Durée de travail effectif** : 7h10 (modifiable dans `add_data.py`)
- **Seuil de pause recommandé** : 45 minutes (code couleur dans les graphiques)

## 🎨 Captures d'Écran

### Interface Web
L'application web offre une interface moderne et intuitive avec :
- Formulaires de saisie simplifiés
- Graphiques matplotlib intégrés
- Tableau de données interactif
- Design responsive

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📝 Licence

Ce projet est open source et disponible sous licence MIT.

## 🐛 Dépannage

**L'application ne démarre pas**
- Vérifiez que Python 3.8+ est installé : `python --version`
- Vérifiez que les dépendances sont installées : `pip list`

**Le fichier CSV n'est pas trouvé**
- Le fichier `horaires.csv` est créé automatiquement lors de la première saisie
- Vérifiez que vous avez les droits d'écriture dans le répertoire

**Les graphiques ne s'affichent pas**
- Vérifiez que matplotlib est correctement installé
- Assurez-vous d'avoir au moins une entrée de données

## 📧 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub.

---

Développé avec ❤️ en Python et Streamlit
