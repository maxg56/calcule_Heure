"""
Service métier pour les statistiques.
"""

from datetime import time
from typing import Dict, Any
from sqlalchemy.orm import Session

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


def calculer_duree_pause(heure_debut_pause: time, heure_fin_pause: time) -> int:
    """
    Calcule la durée de pause en minutes.

    Args:
        heure_debut_pause: Heure de début de pause
        heure_fin_pause: Heure de fin de pause

    Returns:
        Durée de pause en minutes
    """
    debut_minutes = time_to_minutes(heure_debut_pause)
    fin_minutes = time_to_minutes(heure_fin_pause)
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
            "total_entrees": 0,
            "moyenne_arrivee": "00:00",
            "moyenne_depart": "00:00",
            "moyenne_pause_minutes": 0
        }

    # Calculer les moyennes
    total_arrivee = 0
    total_depart = 0
    total_pause = 0

    for schedule in schedules:
        total_arrivee += time_to_minutes(schedule.heure_debut)
        total_depart += time_to_minutes(schedule.heure_depart_calculee)
        total_pause += calculer_duree_pause(schedule.heure_debut_pause, schedule.heure_fin_pause)

    count = len(schedules)

    return {
        "total_entrees": count,
        "moyenne_arrivee": minutes_to_time(total_arrivee // count).strftime("%H:%M"),
        "moyenne_depart": minutes_to_time(total_depart // count).strftime("%H:%M"),
        "moyenne_pause_minutes": total_pause // count
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
            "arrivee": [],
            "depart": [],
            "pause": []
        }

    arrivee_data = []
    depart_data = []
    pause_data = []

    # Calculate averages for reference lines
    total_arrivee = sum(time_to_minutes(s.heure_debut) for s in schedules)
    total_depart = sum(time_to_minutes(s.heure_depart_calculee) for s in schedules)
    count = len(schedules)
    moyenne_arrivee = minutes_to_time(total_arrivee // count).strftime("%H:%M")
    moyenne_depart = minutes_to_time(total_depart // count).strftime("%H:%M")

    for schedule in schedules:
        date_str = schedule.date_saisie.strftime("%Y-%m-%d")

        arrivee_data.append({
            "date": date_str,
            "heure_debut": schedule.heure_debut.strftime("%H:%M"),
            "moyenne": moyenne_arrivee
        })

        depart_data.append({
            "date": date_str,
            "heure_depart": schedule.heure_depart_calculee.strftime("%H:%M"),
            "moyenne": moyenne_depart
        })

        pause_data.append({
            "date": date_str,
            "duree_pause": calculer_duree_pause(schedule.heure_debut_pause, schedule.heure_fin_pause)
        })

    return {
        "arrivee": arrivee_data,
        "depart": depart_data,
        "pause": pause_data
    }
