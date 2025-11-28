"""
Module de calcul des moyennes pour l'application de gestion des horaires.
Calcule les statistiques sur les horaires de travail.
"""
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional

from calcule_Heure.constants import TIME_FORMAT
from calcule_Heure.exceptions import ValidationError

logger = logging.getLogger(__name__)


class StatisticsCalculator:
    """Calculateur de statistiques sur les horaires."""

    @staticmethod
    def _parse_time(time_str: str) -> datetime:
        """
        Parse une chaîne de temps.

        Args:
            time_str: Temps au format HH:MM

        Returns:
            Objet datetime

        Raises:
            ValidationError: Si le format est invalide
        """
        try:
            return datetime.strptime(time_str, TIME_FORMAT)
        except ValueError as e:
            raise ValidationError(f"Format de temps invalide '{time_str}': {e}")

    @staticmethod
    def _timedelta_to_str(td: timedelta) -> str:
        """
        Convertit un timedelta en chaîne HH:MM.

        Args:
            td: timedelta à convertir

        Returns:
            Chaîne au format HH:MM
        """
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours:02d}:{minutes:02d}"

    @classmethod
    def calculate_averages(
        cls,
        schedules: List[Dict[str, str]]
    ) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Calcule les moyennes des heures d'arrivée, de départ et de pause.

        Args:
            schedules: Liste de dictionnaires contenant les horaires

        Returns:
            Tuple (heure_depart_moy, duree_pause_moy, heure_arrivee_moy)
            ou (None, None, None) si aucune donnée valide

        """
        if not schedules:
            logger.warning("Aucun horaire à analyser")
            return None, None, None

        total_start = timedelta()
        total_end = timedelta()
        total_break = timedelta()
        valid_count = 0

        for schedule in schedules:
            try:
                # Parser les heures
                start_time = cls._parse_time(schedule["Heure début"])
                end_time = cls._parse_time(schedule["Heure départ calculée"])
                break_start = cls._parse_time(schedule["Heure début pause"])
                break_end = cls._parse_time(schedule["Heure fin pause"])

                # Accumuler les durées
                total_start += timedelta(hours=start_time.hour, minutes=start_time.minute)
                total_end += timedelta(hours=end_time.hour, minutes=end_time.minute)
                total_break += (break_end - break_start)

                valid_count += 1

            except (KeyError, ValidationError) as e:
                logger.warning(f"Entrée invalide ignorée: {e}")
                continue

        if valid_count == 0:
            logger.warning("Aucune entrée valide trouvée")
            return None, None, None

        # Calculer les moyennes
        avg_start = total_start / valid_count
        avg_end = total_end / valid_count
        avg_break = total_break / valid_count

        # Convertir en chaînes
        avg_start_str = cls._timedelta_to_str(avg_start)
        avg_end_str = cls._timedelta_to_str(avg_end)
        avg_break_str = cls._timedelta_to_str(avg_break)

        logger.info(
            f"Moyennes calculées sur {valid_count} entrées: "
            f"arrivée={avg_start_str}, départ={avg_end_str}, pause={avg_break_str}"
        )

        return avg_end_str, avg_break_str, avg_start_str


# Fonction de compatibilité pour l'ancien code
def calculer_moyennes(
    horaires: List[Dict[str, str]]
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Fonction de compatibilité - utilise StatisticsCalculator.calculate_averages()

    Args:
        horaires: Liste de dictionnaires contenant les horaires

    Returns:
        Tuple (heure_depart_moy, duree_pause_moy, heure_arrivee_moy)
    """
    return StatisticsCalculator.calculate_averages(horaires)
