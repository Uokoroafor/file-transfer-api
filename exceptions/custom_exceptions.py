class FileUploadError(Exception):
    """Raised when file upload fails"""

    def __init__(self, message: str = "Error occurred during file upload"):
        """Constructor for FileUploadError.

        Args:
            Error message that defaults to "Error occurred during file upload".
        """
        self.message = message
        super().__init__(self.message)


class FileDownloadError(Exception):
    """Raised when file download fails"""

    def __init__(self, message: str = "Error occurred during file download"):
        """Constructor for FileDownloadError.

        Args:
            Error message that defaults to "Error occurred during file download".
        """
        self.message = message
        super().__init__(self.message)


class FileReplaceError(Exception):
    """Raised when file replace fails"""

    def __init__(self, message: str = "Error occurred during file replace"):
        """Constructor for FileReplaceError.

        Args:
            Error message that defaults to "Error occurred during file replace".
        """
        self.message = message
        super().__init__(self.message)


class FileDeleteError(Exception):
    """Raised when file delete fails"""

    def __init__(self, message: str = "Error occurred during file delete"):
        """Constructor for FileDeleteError.

        Args:
            Error message that defaults to "Error occurred during file delete".
        """
        self.message = message
        super().__init__(self.message)


class FileRenameError(Exception):
    """Raised when file rename fails"""

    def __init__(self, message: str = "Error occurred during file rename"):
        """Constructor for FileRenameError.

        Args:
            Error message that defaults to "Error occurred during file rename".
        """
        self.message = message
        super().__init__(self.message)


class FileDoesNotExistError(Exception):
    """Raised when file does not exist"""

    def __init__(self, message: str = "File does not exist"):
        """Constructor for FileDoesNotExistError.

        Args:
            Error message that defaults to "File does not exist".
        """
        self.message = message
        super().__init__(self.message)
