from exceptions.custom_exception import BaseCustomException
from dataclasses import dataclass


@dataclass
class DatabaseError(BaseCustomException):
    """Base class for Database exceptions related exceptions"""

    pass


@dataclass
class DatabaseReadError(DatabaseError):
    """Raised when a database read operation fails"""
    description = "Database read failed"


@dataclass
class DatabaseWriteError(DatabaseError):
    """Raised when a database write operation fails"""
    description = "Database write failed"


@dataclass
class DatabaseConnectionError(DatabaseError):
    """Raised when a database connection fails"""
    description = "Database connection failed"
