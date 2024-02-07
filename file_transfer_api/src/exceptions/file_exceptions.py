from src.exceptions.custom_exception import BaseCustomException
from dataclasses import dataclass


@dataclass
class FileError(BaseCustomException):
    """Base class for file errors."""
    pass


@dataclass
class FileDownloadError(FileError):
    """Raised when a file download operation fails."""
    description = "File download failed"


@dataclass
class FileUploadError(FileError):
    """Raised when a file upload operation fails."""
    description = "File upload failed"


@dataclass
class FileDeleteError(FileError):
    """Raised when a file delete operation fails."""
    description = "File delete failed"


@dataclass
class FileUpdateError(FileError):
    """Raised when a file update operation fails."""
    description = "File update failed"


@dataclass
class FileDoesNotExistError(FileError):
    """Raised when a file does not exist."""
    status_code: int = 404
    description: str = "File does not exist"
