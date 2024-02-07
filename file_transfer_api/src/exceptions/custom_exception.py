from fastapi import HTTPException
from dataclasses import dataclass


@dataclass
class BaseCustomException(Exception):
    """Base class for custom exceptions"""
    description: str
    status_code: int = 500

    def raise_as_http(self):
        """
        Raise the exception as an HTTP exception.

        Raises:
            HTTPException: The BaseCustomException raised as an HTTP exception.
        """
        raise HTTPException(status_code=self.status_code, detail=str(f'{self.__class__.__name__}: {self.description}'))
