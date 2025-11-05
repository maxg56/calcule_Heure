"""
Module de configuration pour l'application de gestion des horaires.
Centralise tous les paramètres personnalisables.
"""
import json
import os
from datetime import timedelta

CONFIG_FILE = 'calcule_Heure/config.json'

# Valeurs par défaut
DEFAULT_CONFIG = {
    "duree_travail_heures": 7,
    "duree_travail_minutes": 10,
    "seuil_pause_minutes": 45,
    "format_heure": "%H:%M",
    "format_date": "%Y-%m-%d %H:%M:%S"
}

def charger_config():
    """Charge la configuration depuis le fichier JSON ou retourne les valeurs par défaut."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Fusionner avec les valeurs par défaut pour les clés manquantes
                return {**DEFAULT_CONFIG, **config}
        except (json.JSONDecodeError, IOError):
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()

def sauvegarder_config(config):
    """Sauvegarde la configuration dans le fichier JSON."""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

def get_duree_travail():
    """Retourne la durée de travail configurée sous forme de timedelta."""
    config = charger_config()
    return timedelta(
        hours=config["duree_travail_heures"],
        minutes=config["duree_travail_minutes"]
    )

def get_seuil_pause():
    """Retourne le seuil de pause en minutes."""
    config = charger_config()
    return config["seuil_pause_minutes"]

def get_format_heure():
    """Retourne le format d'heure configuré."""
    config = charger_config()
    return config["format_heure"]

def get_format_date():
    """Retourne le format de date configuré."""
    config = charger_config()
    return config["format_date"]

def mettre_a_jour_config(duree_heures=None, duree_minutes=None, seuil_pause=None):
    """Met à jour les paramètres de configuration."""
    config = charger_config()

    if duree_heures is not None:
        config["duree_travail_heures"] = duree_heures
    if duree_minutes is not None:
        config["duree_travail_minutes"] = duree_minutes
    if seuil_pause is not None:
        config["seuil_pause_minutes"] = seuil_pause

    sauvegarder_config(config)
    return config

def reinitialiser_config():
    """Réinitialise la configuration aux valeurs par défaut."""
    sauvegarder_config(DEFAULT_CONFIG.copy())
    return DEFAULT_CONFIG.copy()
