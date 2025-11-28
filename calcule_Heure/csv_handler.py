"""
Gestionnaire de fichiers CSV pour l'application de gestion des horaires.
Centralise toutes les opérations de lecture/écriture CSV.
"""
import csv
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from calcule_Heure.constants import CSV_FILE, CSV_HEADERS, DATETIME_FORMAT
from calcule_Heure.exceptions import CSVError

logger = logging.getLogger(__name__)


class CSVHandler:
    """Gestionnaire pour les opérations CSV."""

    def __init__(self, file_path: Path = CSV_FILE):
        """
        Initialise le gestionnaire CSV.

        Args:
            file_path: Chemin vers le fichier CSV
        """
        self.file_path = file_path

    def read(self) -> List[Dict[str, str]]:
        """
        Lit les horaires depuis le fichier CSV.

        Returns:
            Liste de dictionnaires contenant les horaires

        Raises:
            CSVError: Si la lecture échoue
        """
        if not self.file_path.exists():
            logger.warning(f"Fichier CSV non trouvé: {self.file_path}")
            return []

        try:
            with open(self.file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)
                logger.info(f"{len(data)} entrées lues depuis {self.file_path}")
                return data
        except IOError as e:
            logger.error(f"Erreur de lecture CSV: {e}")
            raise CSVError(f"Impossible de lire le fichier CSV: {e}")
        except csv.Error as e:
            logger.error(f"Erreur de format CSV: {e}")
            raise CSVError(f"Format CSV invalide: {e}")

    def write(
        self,
        start_time: str,
        break_start: str,
        break_end: str,
        end_time: str,
        timestamp: Optional[datetime] = None
    ) -> None:
        """
        Écrit une nouvelle entrée dans le fichier CSV.

        Args:
            start_time: Heure de début (HH:MM)
            break_start: Heure de début de pause (HH:MM)
            break_end: Heure de fin de pause (HH:MM)
            end_time: Heure de départ calculée (HH:MM)
            timestamp: Date et heure de saisie (par défaut: maintenant)

        Raises:
            CSVError: Si l'écriture échoue
        """
        if timestamp is None:
            timestamp = datetime.now()

        file_exists = self.file_path.exists()

        try:
            # Créer le répertoire parent si nécessaire
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.file_path, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)

                # Écrire les headers si le fichier est nouveau
                if not file_exists:
                    writer.writerow(CSV_HEADERS)
                    logger.info(f"Fichier CSV créé: {self.file_path}")

                # Écrire la nouvelle entrée
                writer.writerow([
                    timestamp.strftime(DATETIME_FORMAT),
                    start_time,
                    break_start,
                    break_end,
                    end_time
                ])

                logger.info(f"Nouvelle entrée ajoutée: {start_time} -> {end_time}")

        except IOError as e:
            logger.error(f"Erreur d'écriture CSV: {e}")
            raise CSVError(f"Impossible d'écrire dans le fichier CSV: {e}")

    def exists(self) -> bool:
        """
        Vérifie si le fichier CSV existe.

        Returns:
            True si le fichier existe, False sinon
        """
        return self.file_path.exists()

    def get_row_count(self) -> int:
        """
        Retourne le nombre d'entrées dans le CSV.

        Returns:
            Nombre d'entrées
        """
        try:
            data = self.read()
            return len(data)
        except CSVError:
            return 0


# Fonction de compatibilité pour l'ancien code
def lire_horaires(fichier: str) -> List[Dict[str, str]]:
    """
    Fonction de compatibilité - utilise CSVHandler.read()

    Args:
        fichier: Chemin vers le fichier CSV (str ou Path)

    Returns:
        Liste de dictionnaires contenant les horaires
    """
    handler = CSVHandler(Path(fichier))
    return handler.read()
