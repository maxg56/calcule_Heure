"""
Constantes de l'application de gestion des horaires.
Centralise toutes les valeurs constantes pour faciliter la maintenance.
"""
from pathlib import Path

# Chemins de fichiers
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT
CONFIG_FILE = DATA_DIR / "config.json"
CSV_FILE = DATA_DIR / "horaires.csv"

# Formats de date et heure
TIME_FORMAT = "%H:%M"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"

# Valeurs par défaut de configuration
DEFAULT_WORK_HOURS = 7
DEFAULT_WORK_MINUTES = 10
DEFAULT_BREAK_THRESHOLD_MINUTES = 45

# Headers CSV
CSV_HEADERS = [
    "Date de saisie",
    "Heure début",
    "Heure début pause",
    "Heure fin pause",
    "Heure départ calculée"
]

# Messages utilisateur
MSG_INVALID_TIME_FORMAT = "Format incorrect, veuillez entrer au format HH:MM."
MSG_CONFIG_SAVED = "Configuration sauvegardée avec succès."
MSG_CONFIG_RESET = "Configuration réinitialisée aux valeurs par défaut."
MSG_DATA_SAVED = "Données enregistrées avec succès."

# Validation
MIN_WORK_HOURS = 1
MAX_WORK_HOURS = 12
MIN_WORK_MINUTES = 0
MAX_WORK_MINUTES = 59
MIN_BREAK_MINUTES = 0
MAX_BREAK_MINUTES = 120
