"""
Module pour l'ajout de données d'horaires.
Gère la saisie et le calcul des horaires de travail.
"""
import logging
from datetime import datetime, timedelta
from typing import Optional

from calcule_Heure.config import ConfigurationManager
from calcule_Heure.csv_handler import CSVHandler
from calcule_Heure.constants import CSV_FILE, TIME_FORMAT, MSG_INVALID_TIME_FORMAT
from calcule_Heure.exceptions import ValidationError, TimeFormatError

logger = logging.getLogger(__name__)


class ScheduleManager:
    """Gestionnaire de saisie et calcul des horaires."""

    def __init__(self):
        """Initialise le gestionnaire d'horaires."""
        self.csv_handler = CSVHandler(CSV_FILE)
        self.config = ConfigurationManager()

    @staticmethod
    def _validate_time(time_str: str) -> bool:
        """
        Valide le format d'une heure.

        Args:
            time_str: Heure au format HH:MM

        Returns:
            True si le format est valide

        Raises:
            TimeFormatError: Si le format est invalide
        """
        try:
            datetime.strptime(time_str, TIME_FORMAT)
            return True
        except ValueError:
            raise TimeFormatError(MSG_INVALID_TIME_FORMAT)

    def _prompt_time(self, prompt_text: str) -> str:
        """
        Demande une heure à l'utilisateur avec validation.

        Args:
            prompt_text: Texte du prompt

        Returns:
            Heure saisie au format HH:MM
        """
        while True:
            time_input = input(f"Entrez l'heure {prompt_text} (HH:MM) : ")
            try:
                self._validate_time(time_input)
                return time_input
            except TimeFormatError:
                print(MSG_INVALID_TIME_FORMAT)

    def calculate_end_time(
        self,
        start_time: str,
        break_start: str,
        break_end: str
    ) -> str:
        """
        Calcule l'heure de départ en fonction des heures saisies.

        Args:
            start_time: Heure de début (HH:MM)
            break_start: Heure de début de pause (HH:MM)
            break_end: Heure de fin de pause (HH:MM)

        Returns:
            Heure de départ calculée (HH:MM)

        Raises:
            ValidationError: Si les heures sont invalides
        """
        try:
            # Valider les formats
            self._validate_time(start_time)
            self._validate_time(break_start)
            self._validate_time(break_end)

            # Parser les heures
            start_dt = datetime.strptime(start_time, TIME_FORMAT)
            break_start_dt = datetime.strptime(break_start, TIME_FORMAT)
            break_end_dt = datetime.strptime(break_end, TIME_FORMAT)

            # Calculer la durée de pause
            break_duration = break_end_dt - break_start_dt

            if break_duration.total_seconds() < 0:
                raise ValidationError("L'heure de fin de pause doit être après l'heure de début")

            # Obtenir la durée de travail configurée
            work_duration = self.config.get_work_duration()

            # Calculer l'heure de départ
            end_dt = start_dt + work_duration + break_duration

            result = end_dt.strftime(TIME_FORMAT)
            logger.info(
                f"Calcul: {start_time} + {work_duration} + {break_duration} = {result}"
            )

            return result

        except TimeFormatError as e:
            logger.error(f"Erreur de format: {e}")
            raise
        except Exception as e:
            logger.error(f"Erreur de calcul: {e}")
            raise ValidationError(f"Erreur lors du calcul: {e}")

    def add_schedule(
        self,
        start_time: Optional[str] = None,
        break_start: Optional[str] = None,
        break_end: Optional[str] = None
    ) -> str:
        """
        Ajoute un nouvel horaire.

        Args:
            start_time: Heure de début (None pour saisie interactive)
            break_start: Heure de début de pause (None pour saisie interactive)
            break_end: Heure de fin de pause (None pour saisie interactive)

        Returns:
            Heure de départ calculée (HH:MM)

        Raises:
            ValidationError: Si les données sont invalides
        """
        # Mode interactif si les heures ne sont pas fournies
        if not (start_time and break_start and break_end):
            logger.info("Mode saisie interactive")
            start_time = self._prompt_time("début travail")
            break_start = self._prompt_time("début pause")
            break_end = self._prompt_time("fin pause")

        # Calculer l'heure de départ
        end_time = self.calculate_end_time(start_time, break_start, break_end)

        # Sauvegarder dans le CSV
        try:
            self.csv_handler.write(start_time, break_start, break_end, end_time)
            logger.info(f"Horaire enregistré: {start_time} -> {end_time}")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde: {e}")
            raise

        return end_time


# Fonction de compatibilité pour l'ancien code
def ajouter_donnees(
    heure_debut: Optional[str] = None,
    heure_pause_debut: Optional[str] = None,
    heure_pause_fin: Optional[str] = None
) -> str:
    """
    Fonction de compatibilité - utilise ScheduleManager.add_schedule()

    Args:
        heure_debut: Heure de début (HH:MM)
        heure_pause_debut: Heure de début de pause (HH:MM)
        heure_pause_fin: Heure de fin de pause (HH:MM)

    Returns:
        Heure de départ calculée (HH:MM)
    """
    manager = ScheduleManager()
    return manager.add_schedule(heure_debut, heure_pause_debut, heure_pause_fin)
