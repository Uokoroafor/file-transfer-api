from abc import ABC
from pydantic import BaseModel


class AbstractResponse(BaseModel, ABC):
    """Abstract class for the response model.

    It contains methods that will be defined elsewhere in concrete classes.
    """
    status_code: int = 200
    message: str



