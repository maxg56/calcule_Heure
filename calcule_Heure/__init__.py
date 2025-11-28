"""
Package calcule_Heure - Gestion des horaires de travail.

Ce package fournit des outils pour gérer et analyser les horaires de travail,
calculer automatiquement les heures de départ, et visualiser les statistiques.

Modules principaux:
- config: Gestion de la configuration
- csv_handler: Lecture/écriture CSV
- add_data: Ajout de nouvelles données
- colcul: Calculs statistiques
- graphique: Génération de graphiques
- constants: Constantes de l'application
- exceptions: Exceptions personnalisées

Utilisation:
    from calcule_Heure import config, add_data, colcul

    # Charger la configuration
    duree_travail = config.get_duree_travail()

    # Ajouter des données
    heure_depart = add_data.ajouter_donnees("08:00", "12:00", "12:45")

    # Calculer les moyennes
    horaires = csv_handler.CSVHandler().read()
    moyennes = colcul.calculer_moyennes(horaires)
"""

__version__ = "2.0.0"
__author__ = "maxg56"

from calcule_Heure import (
    config,
    csv_handler,
    add_data,
    colcul,
    constants,
    exceptions
)

__all__ = [
    "config",
    "csv_handler",
    "add_data",
    "colcul",
    "constants",
    "exceptions"
]
