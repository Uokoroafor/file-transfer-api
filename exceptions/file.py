class FileError(Exception):
    """Base class for file errors."""
    pass


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
