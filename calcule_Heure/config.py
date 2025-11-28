"""
Module de configuration pour l'application de gestion des horaires.
Centralise tous les paramètres personnalisables avec validation et gestion d'erreurs.
"""
import json
import logging
from datetime import timedelta
from pathlib import Path
from typing import Dict, Any, Optional

from calcule_Heure.constants import (
    CONFIG_FILE,
    DEFAULT_WORK_HOURS,
    DEFAULT_WORK_MINUTES,
    DEFAULT_BREAK_THRESHOLD_MINUTES,
    TIME_FORMAT,
    DATETIME_FORMAT,
    MIN_WORK_HOURS,
    MAX_WORK_HOURS,
    MIN_WORK_MINUTES,
    MAX_WORK_MINUTES,
    MIN_BREAK_MINUTES,
    MAX_BREAK_MINUTES
)
from calcule_Heure.exceptions import ConfigurationError, ValidationError

# Configuration du logger
logger = logging.getLogger(__name__)


class ConfigurationManager:
    """Gestionnaire de configuration centralisé avec validation."""

    DEFAULT_CONFIG = {
        "duree_travail_heures": DEFAULT_WORK_HOURS,
        "duree_travail_minutes": DEFAULT_WORK_MINUTES,
        "seuil_pause_minutes": DEFAULT_BREAK_THRESHOLD_MINUTES,
        "format_heure": TIME_FORMAT,
        "format_date": DATETIME_FORMAT
    }

    @classmethod
    def load(cls) -> Dict[str, Any]:
        """
        Charge la configuration depuis le fichier JSON.

        Returns:
            Dict contenant la configuration

        Raises:
            ConfigurationError: Si la configuration ne peut pas être chargée
        """
        if not CONFIG_FILE.exists():
            logger.info(f"Fichier de configuration non trouvé, utilisation des valeurs par défaut")
            return cls.DEFAULT_CONFIG.copy()

        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Fusionner avec les valeurs par défaut pour les clés manquantes
                merged_config = {**cls.DEFAULT_CONFIG, **config}
                cls._validate_config(merged_config)
                logger.info("Configuration chargée avec succès")
                return merged_config
        except json.JSONDecodeError as e:
            logger.error(f"Erreur de décodage JSON: {e}")
            return cls.DEFAULT_CONFIG.copy()
        except IOError as e:
            logger.error(f"Erreur de lecture du fichier: {e}")
            return cls.DEFAULT_CONFIG.copy()
        except ValidationError as e:
            logger.error(f"Erreur de validation: {e}")
            return cls.DEFAULT_CONFIG.copy()

    @classmethod
    def save(cls, config: Dict[str, Any]) -> None:
        """
        Sauvegarde la configuration dans le fichier JSON.

        Args:
            config: Dictionnaire de configuration à sauvegarder

        Raises:
            ConfigurationError: Si la sauvegarde échoue
        """
        try:
            cls._validate_config(config)
            CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)

            logger.info("Configuration sauvegardée avec succès")
        except IOError as e:
            logger.error(f"Erreur d'écriture du fichier: {e}")
            raise ConfigurationError(f"Impossible de sauvegarder la configuration: {e}")
        except ValidationError as e:
            logger.error(f"Erreur de validation: {e}")
            raise

    @staticmethod
    def _validate_config(config: Dict[str, Any]) -> None:
        """
        Valide les valeurs de configuration.

        Args:
            config: Configuration à valider

        Raises:
            ValidationError: Si la configuration est invalide
        """
        # Validation durée de travail
        hours = config.get("duree_travail_heures", DEFAULT_WORK_HOURS)
        minutes = config.get("duree_travail_minutes", DEFAULT_WORK_MINUTES)

        if not isinstance(hours, int) or not MIN_WORK_HOURS <= hours <= MAX_WORK_HOURS:
            raise ValidationError(
                f"Les heures de travail doivent être entre {MIN_WORK_HOURS} et {MAX_WORK_HOURS}"
            )

        if not isinstance(minutes, int) or not MIN_WORK_MINUTES <= minutes <= MAX_WORK_MINUTES:
            raise ValidationError(
                f"Les minutes de travail doivent être entre {MIN_WORK_MINUTES} et {MAX_WORK_MINUTES}"
            )

        # Validation seuil de pause
        break_threshold = config.get("seuil_pause_minutes", DEFAULT_BREAK_THRESHOLD_MINUTES)
        if not isinstance(break_threshold, int) or not MIN_BREAK_MINUTES <= break_threshold <= MAX_BREAK_MINUTES:
            raise ValidationError(
                f"Le seuil de pause doit être entre {MIN_BREAK_MINUTES} et {MAX_BREAK_MINUTES} minutes"
            )

    @classmethod
    def get_work_duration(cls) -> timedelta:
        """
        Retourne la durée de travail configurée.

        Returns:
            timedelta représentant la durée de travail
        """
        config = cls.load()
        return timedelta(
            hours=config["duree_travail_heures"],
            minutes=config["duree_travail_minutes"]
        )

    @classmethod
    def get_break_threshold(cls) -> int:
        """
        Retourne le seuil de pause en minutes.

        Returns:
            Seuil de pause en minutes
        """
        config = cls.load()
        return config["seuil_pause_minutes"]

    @classmethod
    def get_time_format(cls) -> str:
        """
        Retourne le format d'heure configuré.

        Returns:
            Format d'heure (ex: '%H:%M')
        """
        config = cls.load()
        return config["format_heure"]

    @classmethod
    def get_date_format(cls) -> str:
        """
        Retourne le format de date configuré.

        Returns:
            Format de date (ex: '%Y-%m-%d %H:%M:%S')
        """
        config = cls.load()
        return config["format_date"]

    @classmethod
    def update(
        cls,
        work_hours: Optional[int] = None,
        work_minutes: Optional[int] = None,
        break_threshold: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Met à jour les paramètres de configuration.

        Args:
            work_hours: Heures de travail
            work_minutes: Minutes de travail
            break_threshold: Seuil de pause en minutes

        Returns:
            Configuration mise à jour

        Raises:
            ValidationError: Si les valeurs sont invalides
        """
        config = cls.load()

        if work_hours is not None:
            config["duree_travail_heures"] = work_hours
        if work_minutes is not None:
            config["duree_travail_minutes"] = work_minutes
        if break_threshold is not None:
            config["seuil_pause_minutes"] = break_threshold

        cls.save(config)
        return config

    @classmethod
    def reset(cls) -> Dict[str, Any]:
        """
        Réinitialise la configuration aux valeurs par défaut.

        Returns:
            Configuration par défaut
        """
        default_config = cls.DEFAULT_CONFIG.copy()
        cls.save(default_config)
        logger.info("Configuration réinitialisée")
        return default_config


# Fonctions de compatibilité pour l'ancien code
def charger_config() -> Dict[str, Any]:
    """Fonction de compatibilité - utilise ConfigurationManager.load()"""
    return ConfigurationManager.load()


def sauvegarder_config(config: Dict[str, Any]) -> None:
    """Fonction de compatibilité - utilise ConfigurationManager.save()"""
    ConfigurationManager.save(config)


def get_duree_travail() -> timedelta:
    """Fonction de compatibilité - utilise ConfigurationManager.get_work_duration()"""
    return ConfigurationManager.get_work_duration()


def get_seuil_pause() -> int:
    """Fonction de compatibilité - utilise ConfigurationManager.get_break_threshold()"""
    return ConfigurationManager.get_break_threshold()


def get_format_heure() -> str:
    """Fonction de compatibilité - utilise ConfigurationManager.get_time_format()"""
    return ConfigurationManager.get_time_format()


def get_format_date() -> str:
    """Fonction de compatibilité - utilise ConfigurationManager.get_date_format()"""
    return ConfigurationManager.get_date_format()


def mettre_a_jour_config(
    duree_heures: Optional[int] = None,
    duree_minutes: Optional[int] = None,
    seuil_pause: Optional[int] = None
) -> Dict[str, Any]:
    """Fonction de compatibilité - utilise ConfigurationManager.update()"""
    return ConfigurationManager.update(duree_heures, duree_minutes, seuil_pause)


def reinitialiser_config() -> Dict[str, Any]:
    """Fonction de compatibilité - utilise ConfigurationManager.reset()"""
    return ConfigurationManager.reset()
