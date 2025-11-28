"""
Schémas Pydantic pour la validation des données.
"""

from .schedule import (
    ScheduleBase,
    ScheduleCreate,
    ScheduleUpdate,
    ScheduleResponse,
)
from .config import ConfigBase, ConfigUpdate, ConfigResponse

__all__ = [
    "ScheduleBase",
    "ScheduleCreate",
    "ScheduleUpdate",
    "ScheduleResponse",
    "ConfigBase",
    "ConfigUpdate",
    "ConfigResponse",
]
