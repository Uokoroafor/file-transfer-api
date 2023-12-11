class BaseCustomException(Exception):
    """Base class for custom exceptions"""

    def __init__(self, name: str, description: str, status_code: int):
        """Constructor for BaseCustomException.

        Args:
            name : Name of the exception
            description : Description of the exception
            status_code : Status code of the exception
        """
        self.name = name
        self.description = description
        self.status_code = status_code
        super().__init__(self.description)