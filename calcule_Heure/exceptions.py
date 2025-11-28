"""
Exceptions personnalisées pour l'application de gestion des horaires.
"""


class HorairesException(Exception):
    """Exception de base pour l'application de gestion des horaires."""
    pass


class ConfigurationError(HorairesException):
    """Exception levée lors d'erreurs de configuration."""
    pass


class ValidationError(HorairesException):
    """Exception levée lors d'erreurs de validation des données."""
    pass


class CSVError(HorairesException):
    """Exception levée lors d'erreurs de lecture/écriture CSV."""
    pass


class TimeFormatError(ValidationError):
    """Exception levée lors d'erreurs de format de temps."""
    pass
