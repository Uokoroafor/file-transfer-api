from exceptions.custom_exception import BaseCustomException


class FileError(BaseCustomException):
    """Base class for file errors."""

    def __init__(self, description: str, status_code: int = 500):
        """Constructor for FileError.

        Args:
            description : Description of the exception
            status_code : Status code of the exception
        """
        super().__init__(description=description, status_code=status_code)


class FileDownloadError(FileError):
    """Raised when a file download operation fails."""
    def __init__(self, description: str, status_code: int = 500):
        """Constructor for FileDownloadError.

        Args:
            description : Description of the exception
            status_code : Status code of the exception
        """
        super().__init__(description=description, status_code=status_code)


class FileUploadError(FileError):
    """Raised when a file upload operation fails."""
    def __init__(self, description: str, status_code: int = 500):
        """Constructor for FileUploadError.

        Args:
            description : Description of the exception
            status_code : Status code of the exception
        """
        super().__init__(description=description, status_code=status_code)


class FileDeleteError(FileError):
    """Raised when a file delete operation fails."""
    def __init__(self, description: str, status_code: int = 500):
        """Constructor for FileDeleteError.

        Args:
            description : Description of the exception
            status_code : Status code of the exception
        """
        super().__init__(description=description, status_code=status_code)


class FileUpdateError(FileError):
    """Raised when a file update operation fails."""
    def __init__(self, description: str, status_code: int = 500):
        """Constructor for FileUpdateError.

        Args:
            description : Description of the exception
            status_code : Status code of the exception
        """
        super().__init__(description=description, status_code=status_code)


class FileDoesNotExistError(FileError):
    """Raised when a file does not exist."""
    def __init__(self, description: str, status_code: int = 404):
        """Constructor for FileDoesNotExistError.

        Args:
            description : Description of the exception
            status_code : Status code of the exception
        """
        super().__init__(description=description, status_code=status_code)
