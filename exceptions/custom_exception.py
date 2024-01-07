from fastapi import HTTPException


class BaseCustomException(Exception):
    """Base class for custom exceptions"""

    def __init__(self, description: str, status_code: int = 500):
        """Constructor for BaseCustomException.

        Args:
            description : Description of the exception
            status_code : Status code of the exception
        """
        self.name = self.__class__.__name__
        self.description = description
        self.status_code = status_code
        super().__init__(self.description)

    def raise_as_http(self):
        """
        Raise the exception as an HTTP exception.
        """
        raise HTTPException(status_code=self.status_code, detail=str(f'{self.name}: {self.description}'))