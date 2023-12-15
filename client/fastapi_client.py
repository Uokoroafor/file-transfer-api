import requests
from typing import List, Optional, Dict


class FastAPIClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        """Constructor for FastAPIClient.

        Args:
            base_url: Base URL for the API. Defaults to "http://127.0.0.1:8000"
        """
        self.base_url = base_url

    def get(self, endpoint: str) -> requests.Response:
        """GET request to the API.

        Args:
            endpoint: Endpoint to send the request to.

        Returns:
            Response from the API.
        """
        return requests.get(self.base_url + endpoint)

    def post(self, endpoint: str, body: Optional[Dict] = None) -> requests.Response:
        """POST request to the API.

        Args:
            endpoint: Endpoint to send the request to.
            body: Body of the request.

        Returns:
            Response from the API.
        """
        return requests.post(self.base_url + endpoint, json=body)

    def put(self, endpoint: str, body: Optional[Dict] = None) -> requests.Response:
        """PUT request to the API.

        Args:
            endpoint: Endpoint to send the request to.
            body: Body of the request.

        Returns:
            Response from the API.
        """
        return requests.put(self.base_url + endpoint, json=body)

    def delete(self, endpoint: str) -> requests.Response:
        """DELETE request to the API.

        Args:
            endpoint: Endpoint to send the request to.

        Returns:
            Response from the API.
        """
        return requests.delete(self.base_url + endpoint)

# TODO: Add the rest of the methods
