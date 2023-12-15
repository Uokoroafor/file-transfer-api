from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class CustomResponse:
    """Abstract class for the response model.

    It contains methods that will be defined elsewhere in concrete classes.
    """

    def __init__(self, **kwargs):
        """Constructor for CustomResponse. It will set the attributes of the class based on the keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments.
        """
        data ={}
        for key, value in kwargs.items():
            setattr(self, key, value)
            if key not in ['message', 'status_code']:
                data[key] = value
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        """Converts the class to a dictionary.

        Returns:
            Dict: Dictionary representation of the class - to make it compatible with FastAPI, we will return
            status_code and message, then the rest of the attributes as a dictionary called data.
        """
        return self.__dict__


if __name__ == '__main__':
    test_response = CustomResponse(message="Welcome to the API", status_code=200, file_id="12345678-1234-5678-1234-567812345678")
    print(test_response)
    print(test_response.to_dict())
