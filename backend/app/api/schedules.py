"""
Routes API pour la gestion des horaires.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.schedule import ScheduleCreate, ScheduleUpdate, ScheduleResponse
from ..services import schedule_service

router = APIRouter(prefix="/schedules", tags=["schedules"])


@router.get("/", response_model=List[ScheduleResponse])
def list_schedules(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Récupère la liste de tous les horaires.

    Args:
        skip: Nombre d'éléments à ignorer
        limit: Nombre maximum d'éléments à retourner
        db: Session de base de données

    Returns:
        Liste des horaires
    """
    schedules = schedule_service.get_schedules(db, skip=skip, limit=limit)
    return schedules


@router.get("/{schedule_id}", response_model=ScheduleResponse)
def get_schedule(
    schedule_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupère un horaire par son ID.

    Args:
        schedule_id: ID de l'horaire
        db: Session de base de données

    Returns:
        Horaire trouvé

    Raises:
        HTTPException: Si l'horaire n'existe pas
    """
    schedule = schedule_service.get_schedule(db, schedule_id)

    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Horaire {schedule_id} non trouvé"
        )

    return schedule


@router.post("/", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_schedule(
    schedule: ScheduleCreate,
    db: Session = Depends(get_db)
):
    """
    Crée un nouvel horaire.

    Args:
        schedule: Données de l'horaire à créer
        db: Session de base de données

    Returns:
        Horaire créé
    """
    return schedule_service.create_schedule(db, schedule)


@router.put("/{schedule_id}", response_model=ScheduleResponse)
def update_schedule(
    schedule_id: int,
    schedule: ScheduleUpdate,
    db: Session = Depends(get_db)
):
    """
    Met à jour un horaire.

    Args:
        schedule_id: ID de l'horaire
        schedule: Données de l'horaire à mettre à jour
        db: Session de base de données

    Returns:
        Horaire mis à jour

    Raises:
        HTTPException: Si l'horaire n'existe pas
    """
    updated_schedule = schedule_service.update_schedule(db, schedule_id, schedule)

    if not updated_schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Horaire {schedule_id} non trouvé"
        )

    return updated_schedule


@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db)
):
    """
    Supprime un horaire.

    Args:
        schedule_id: ID de l'horaire
        db: Session de base de données

    Raises:
        HTTPException: Si l'horaire n'existe pas
    """
    deleted = schedule_service.delete_schedule(db, schedule_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Horaire {schedule_id} non trouvé"
        )
