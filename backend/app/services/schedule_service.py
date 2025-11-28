"""
Service métier pour la gestion des horaires.
"""

from datetime import datetime, time, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session

from ..models.schedule import Schedule
from ..models.config import Config
from ..schemas.schedule import ScheduleCreate, ScheduleUpdate


def calculer_heure_depart(
    heure_debut: time,
    heure_debut_pause: time,
    heure_fin_pause: time,
    duree_travail_heures: int,
    duree_travail_minutes: int
) -> time:
    """
    Calcule l'heure de départ en fonction des horaires de travail et de pause.

    Args:
        heure_debut: Heure de début de travail
        heure_debut_pause: Heure de début de pause
        heure_fin_pause: Heure de fin de pause
        duree_travail_heures: Durée de travail en heures
        duree_travail_minutes: Durée de travail en minutes

    Returns:
        Heure de départ calculée
    """
    # Convertir les time en datetime pour faciliter les calculs
    today = datetime.today()
    dt_debut = datetime.combine(today, heure_debut)
    dt_pause_debut = datetime.combine(today, heure_debut_pause)
    dt_pause_fin = datetime.combine(today, heure_fin_pause)

    # Calculer la durée de pause
    duree_pause = dt_pause_fin - dt_pause_debut

    # Calculer la durée de travail totale
    duree_travail = timedelta(hours=duree_travail_heures, minutes=duree_travail_minutes)

    # Calculer l'heure de départ
    dt_depart = dt_debut + duree_travail + duree_pause

    return dt_depart.time()


def get_schedules(db: Session, skip: int = 0, limit: int = 100) -> List[Schedule]:
    """
    Récupère la liste des horaires.

    Args:
        db: Session de base de données
        skip: Nombre d'éléments à ignorer
        limit: Nombre maximum d'éléments à retourner

    Returns:
        Liste des horaires
    """
    return db.query(Schedule).order_by(Schedule.date_saisie.desc()).offset(skip).limit(limit).all()


def get_schedule(db: Session, schedule_id: int) -> Optional[Schedule]:
    """
    Récupère un horaire par son ID.

    Args:
        db: Session de base de données
        schedule_id: ID de l'horaire

    Returns:
        Horaire trouvé ou None
    """
    return db.query(Schedule).filter(Schedule.id == schedule_id).first()


def create_schedule(db: Session, schedule: ScheduleCreate) -> Schedule:
    """
    Crée un nouveau horaire.

    Args:
        db: Session de base de données
        schedule: Données de l'horaire à créer

    Returns:
        Horaire créé
    """
    # Récupérer la configuration pour calculer l'heure de départ
    config = db.query(Config).filter(Config.id == 1).first()

    # Calculer l'heure de départ
    heure_depart = calculer_heure_depart(
        schedule.heure_debut,
        schedule.heure_debut_pause,
        schedule.heure_fin_pause,
        config.duree_travail_heures,
        config.duree_travail_minutes
    )

    # Créer l'horaire
    db_schedule = Schedule(
        heure_debut=schedule.heure_debut,
        heure_debut_pause=schedule.heure_debut_pause,
        heure_fin_pause=schedule.heure_fin_pause,
        heure_depart_calculee=heure_depart
    )

    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)

    return db_schedule


def update_schedule(db: Session, schedule_id: int, schedule: ScheduleUpdate) -> Optional[Schedule]:
    """
    Met à jour un horaire.

    Args:
        db: Session de base de données
        schedule_id: ID de l'horaire
        schedule: Données de l'horaire à mettre à jour

    Returns:
        Horaire mis à jour ou None
    """
    db_schedule = get_schedule(db, schedule_id)

    if not db_schedule:
        return None

    # Mettre à jour les champs fournis
    update_data = schedule.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_schedule, field, value)

    # Recalculer l'heure de départ si nécessaire
    if any(field in update_data for field in ["heure_debut", "heure_debut_pause", "heure_fin_pause"]):
        config = db.query(Config).filter(Config.id == 1).first()
        heure_depart = calculer_heure_depart(
            db_schedule.heure_debut,
            db_schedule.heure_debut_pause,
            db_schedule.heure_fin_pause,
            config.duree_travail_heures,
            config.duree_travail_minutes
        )
        db_schedule.heure_depart_calculee = heure_depart

    db.commit()
    db.refresh(db_schedule)

    return db_schedule


def delete_schedule(db: Session, schedule_id: int) -> bool:
    """
    Supprime un horaire.

    Args:
        db: Session de base de données
        schedule_id: ID de l'horaire

    Returns:
        True si supprimé, False sinon
    """
    db_schedule = get_schedule(db, schedule_id)

    if not db_schedule:
        return False

    db.delete(db_schedule)
    db.commit()

    return True
