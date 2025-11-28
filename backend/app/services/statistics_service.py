"""
Service métier pour les statistiques.
"""

from datetime import time
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.schedule import Schedule
from ..models.config import Config


def time_to_minutes(t: time) -> int:
    """
    Convertit un objet time en minutes depuis minuit.

    Args:
        t: Objet time

    Returns:
        Nombre de minutes depuis minuit
    """
    return t.hour * 60 + t.minute


def minutes_to_time(minutes: int) -> time:
    """
    Convertit des minutes en objet time.

    Args:
        minutes: Nombre de minutes depuis minuit

    Returns:
        Objet time
    """
    hours = minutes // 60
    mins = minutes % 60
    return time(hour=hours, minute=mins)


def calculer_duree_pause(heure_pause_debut: time, heure_pause_fin: time) -> int:
    """
    Calcule la durée de pause en minutes.

    Args:
        heure_pause_debut: Heure de début de pause
        heure_pause_fin: Heure de fin de pause

    Returns:
        Durée de pause en minutes
    """
    debut_minutes = time_to_minutes(heure_pause_debut)
    fin_minutes = time_to_minutes(heure_pause_fin)
    return fin_minutes - debut_minutes


def get_statistics(db: Session) -> Dict[str, Any]:
    """
    Calcule les statistiques sur les horaires.

    Args:
        db: Session de base de données

    Returns:
        Dictionnaire contenant les statistiques
    """
    schedules = db.query(Schedule).all()

    if not schedules:
        return {
            "nombre_entrees": 0,
            "heure_arrivee_moyenne": None,
            "heure_depart_moyenne": None,
            "duree_pause_moyenne": None
        }

    # Calculer les moyennes
    total_arrivee = 0
    total_depart = 0
    total_pause = 0

    for schedule in schedules:
        total_arrivee += time_to_minutes(schedule.heure_debut)
        total_depart += time_to_minutes(schedule.heure_depart_calculee)
        total_pause += calculer_duree_pause(schedule.heure_pause_debut, schedule.heure_pause_fin)

    count = len(schedules)

    return {
        "nombre_entrees": count,
        "heure_arrivee_moyenne": minutes_to_time(total_arrivee // count),
        "heure_depart_moyenne": minutes_to_time(total_depart // count),
        "duree_pause_moyenne": total_pause // count
    }


def get_charts_data(db: Session) -> Dict[str, Any]:
    """
    Récupère les données pour les graphiques.

    Args:
        db: Session de base de données

    Returns:
        Dictionnaire contenant les données pour les graphiques
    """
    schedules = db.query(Schedule).order_by(Schedule.date_saisie).all()
    config = db.query(Config).filter(Config.id == 1).first()

    if not schedules:
        return {
            "dates": [],
            "heures_arrivee": [],
            "heures_depart": [],
            "durees_pause": [],
            "seuil_pause": config.seuil_pause_minutes if config else 45
        }

    dates = []
    heures_arrivee = []
    heures_depart = []
    durees_pause = []

    for schedule in schedules:
        dates.append(schedule.date_saisie.strftime("%Y-%m-%d"))
        heures_arrivee.append(schedule.heure_debut.strftime("%H:%M"))
        heures_depart.append(schedule.heure_depart_calculee.strftime("%H:%M"))
        durees_pause.append(calculer_duree_pause(schedule.heure_pause_debut, schedule.heure_pause_fin))

    return {
        "dates": dates,
        "heures_arrivee": heures_arrivee,
        "heures_depart": heures_depart,
        "durees_pause": durees_pause,
        "seuil_pause": config.seuil_pause_minutes if config else 45
    }
