class DatabaseError(Exception):
    """Base class for Database exceptions related exceptions"""
    pass


class DatabaseReadError(DatabaseError):
    """Raised when a database read operation fails"""
    pass


class DatabaseWriteError(DatabaseError):
    """Raised when a database write operation fails"""
    pass


class DatabaseConnectionError(DatabaseError):
    """Raised when a database connection fails"""
    pass
