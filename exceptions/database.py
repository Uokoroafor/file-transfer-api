from fastapi import HTTPException


class DatabaseError(Exception):
    """Base class for Database exceptions related exceptions"""
    def raise_as_http(self, status_code: int = 500):
        """Raise the exception as an HTTP exception"""
        raise HTTPException(status_code=status_code, detail=str(f'{self.__class__.__name__}: {self.args[0]}'))


class DatabaseReadError(DatabaseError):
    """Raised when a database read operation fails"""
    pass


class DatabaseWriteError(DatabaseError):
    """Raised when a database write operation fails"""
    pass


class DatabaseConnectionError(DatabaseError):
    """Raised when a database connection fails"""
    pass
