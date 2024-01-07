from exceptions.custom_exception import BaseCustomException


class DatabaseError(BaseCustomException):
    """Base class for Database exceptions related exceptions"""

    def __init__(self, description: str, status_code: int = 500):
        """Constructor for DatabaseError.

        Args:
            description : Description of the exception
            status_code : Status code of the exception
        """
        super().__init__(description=description, status_code=status_code)


class DatabaseReadError(DatabaseError):
    """Raised when a database read operation fails"""
    pass


class DatabaseWriteError(DatabaseError):
    """Raised when a database write operation fails"""
    pass


class DatabaseConnectionError(DatabaseError):
    """Raised when a database connection fails"""
    pass
