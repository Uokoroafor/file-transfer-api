from fastapi import HTTPException


class FileError(Exception):
    """Base class for file errors."""

    def raise_as_http(self, status_code: int = 500):
        """Raise the exception as an HTTP exception"""
        raise HTTPException(status_code=status_code, detail=str(f'{self.__class__.__name__}: {self.args[0]}'))


class FileDownloadError(FileError):
    """Raised when a file download operation fails."""
    pass


class FileUploadError(FileError):
    """Raised when a file upload operation fails."""
    pass


class FileDeleteError(FileError):
    """Raised when a file delete operation fails."""
    pass


class FileUpdateError(FileError):
    """Raised when a file update operation fails."""
    pass


class FileDoesNotExistError(FileError):
    """Raised when a file does not exist."""
    pass
