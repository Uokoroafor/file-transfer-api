from abstracts.exceptions_abstract import BaseCustomException


class FileUploadError(BaseCustomException):
    """Raised when file upload fails"""

    def __init__(self, description: str = "Error occurred during file upload"):
        """Constructor for FileUploadError.

        Args:
            Error description that defaults to "Error occurred during file upload".
        """
        self.name = "FileUploadError"
        self.status_code = 500
        self.description = description
        super().__init__(self.name, self.description, self.status_code)


class FileDownloadError(BaseCustomException):
    """Raised when file download fails"""

    def __init__(self, description: str = "Error occurred during file download"):
        """Constructor for FileDownloadError.

        Args:
            Error description that defaults to "Error occurred during file download".
        """
        self.name = "FileDownloadError"
        self.status_code = 500
        self.description = description
        super().__init__(self.name, self.description, self.status_code)


class FileReplaceError(BaseCustomException):
    """Raised when file replace fails"""

    def __init__(self, description: str = "Error occurred during file replace"):
        """Constructor for FileReplaceError.

        Args:
            Error description that defaults to "Error occurred during file replace".
        """
        self.name = "FileReplaceError"
        self.status_code = 500
        self.description = description
        super().__init__(self.name, self.description, self.status_code)


class FileDeleteError(BaseCustomException):
    """Raised when file delete fails"""

    def __init__(self, description: str = "Error occurred during file delete"):
        """Constructor for FileDeleteError.

        Args:
            Error description that defaults to "Error occurred during file delete".
        """
        self.name = "FileDeleteError"
        self.status_code = 500
        self.description = description
        super().__init__(self.name, self.description, self.status_code)


class FileRenameError(BaseCustomException):
    """Raised when file rename fails"""

    def __init__(self, description: str = "Error occurred during file rename"):
        """Constructor for FileRenameError.

        Args:
            Error description that defaults to "Error occurred during file rename".
        """
        self.name = "FileRenameError"
        self.status_code = 500
        self.description = description
        super().__init__(self.name, self.description, self.status_code)


class FileDoesNotExistError(BaseCustomException):
    """Raised when file does not exist"""

    def __init__(self, description: str = "File does not exist"):
        """Constructor for FileDoesNotExistError.

        Args:
            Error description that defaults to "File does not exist".
        """
        self.name = "FileDoesNotExistError"
        self.status_code = 404
        self.description = description
        super().__init__(self.name, self.description, self.status_code)
