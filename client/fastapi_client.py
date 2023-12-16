from typing import Optional, Dict
import requests
from requests.exceptions import HTTPError
from app.utils.logging_utils import ErrorLogger
import mimetypes


class FastAPIClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000", error_logger_path: Optional[str] = None):
        """Constructor for FastAPIClient.

        Args:
            base_url: Base URL for the API. Defaults to "http://127.0.0.1:8000"
        """
        self.base_url = base_url
        self.logger = ErrorLogger(log_file_path=error_logger_path, name="FastAPIClient")

    def _handle_http_error(self, e: HTTPError) -> None:
        """Handle HTTP errors.

        Args:
            e: HTTPError to handle.
        """
        self.logger.log_error(f"HTTP error occurred: {e}")
        raise e

    def _handle_connection_error(self, e: requests.exceptions.ConnectionError) -> None:
        """Handle connection errors.

        Args:
            e: ConnectionError to handle.
        """
        self.logger.log_error(f"Connection error occurred: {e}")
        raise ConnectionError(f"Connection error occurred. Please check the API is running at {self.base_url}."
                              f" \n Error Details: {e}")

    def _get(self, endpoint: str) -> requests.Response:
        """GET request to the API.

        Args:
            endpoint: Endpoint to send the request to.

        Returns:
            Response from the API.

        Raises:
            HTTPError: If the request fails
            ConnectionError: If the connection fails
        """
        try:
            return requests.get(self.base_url + endpoint)
        except HTTPError as e:
            self._handle_http_error(e)
        except requests.exceptions.ConnectionError as e:
            self._handle_connection_error(e)

    def _post(self, endpoint: str, body: Optional[Dict] = None) -> requests.Response:
        """POST request to the API.

        Args:
            endpoint: Endpoint to send the request to.
            body: Body of the request.

        Returns:
            Response from the API.

        Raises:
            HTTPError: If the request fails
            ConnectionError: If the connection fails
        """
        try:
            return requests.post(self.base_url + endpoint, files=body)
        except HTTPError as e:
            self._handle_http_error(e)
        except requests.exceptions.ConnectionError as e:
            self._handle_connection_error(e)

    def _put(self, endpoint: str, body: Optional[Dict] = None) -> requests.Response:
        """PUT request to the API.

        Args:
            endpoint: Endpoint to send the request to.
            body: Body of the request.

        Returns:
            Response from the API.
        """
        try:
            return requests.put(self.base_url + endpoint, params=body)
        except HTTPError as e:
            self._handle_http_error(e)
        except requests.exceptions.ConnectionError as e:
            self._handle_connection_error(e)

    def _put_with_file(self, endpoint: str, body: Optional[Dict] = None) -> requests.Response:
        """PUT request to the API.

        Args:
            endpoint: Endpoint to send the request to.
            body: Body of the request.

        Returns:
            Response from the API.

        Raises:
            HTTPError: If the request fails
            ConnectionError: If the connection fails
        """
        try:
            return requests.put(self.base_url + endpoint, files=body)
        except HTTPError as e:
            self._handle_http_error(e)
        except requests.exceptions.ConnectionError as e:
            self._handle_connection_error(e)

    def _delete(self, endpoint: str) -> requests.Response:
        """DELETE request to the API.

        Args:
            endpoint: Endpoint to send the request to.

        Returns:
            Response from the API.

        Raises:
            HTTPError: If the request fails
            ConnectionError: If the connection fails
        """
        try:
            return requests.delete(self.base_url + endpoint)
        except HTTPError as e:
            self._handle_http_error(e)
        except requests.exceptions.ConnectionError as e:
            self._handle_connection_error(e)

    def upload_file(self, file_path: str) -> requests.Response:
        """Upload a file to the API.

        Args:
            file_path: Path to the file to upload.

        Returns:
            Response from the API.
        """
        content_type, _ = mimetypes.guess_type(file_path) or ("multipart/form-data", None)
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f, content_type)}
            return self._post("/full/upload", body=files)

    def download_file(self, file_id: str) -> requests.Response:
        """Download a file from the API.

        Args:
            file_id: ID of the file to download.

        Returns:
            Response from the API.
        """
        return self._get(f"/full/download/{file_id}")

    def replace_file(self, file_id: str, file_path: str) -> requests.Response:
        """Replace a file in the API.

        Args:
            file_id: ID of the file to replace.
            file_path: Path to the file to replace with.

        Returns:
            Response from the API.
        """
        content_type, _ = mimetypes.guess_type(file_path) or ("multipart/form-data", None)
        with open(file_path, "rb") as f:
            return self._put_with_file(f"/full/replace/{file_id}", body={"file": (file_path, f, content_type)})

    def rename_file(self, file_id: str, new_file_id: str) -> requests.Response:
        """Rename a file in the API.

        Args:
            file_id: ID of the file to rename.
            new_file_id: New ID of the file.

        Returns:
            Response from the API.
        """
        return self._put(f"/full/rename/{file_id}", body={"new_file_id": new_file_id})

    def delete_file(self, file_id: str) -> requests.Response:
        """Delete a file from the API.

        Args:
            file_id: ID of the file to delete.

        Returns:
            Response from the API.
        """
        return self._delete(f"/full/delete/{file_id}")

    def get_file_metadata(self, file_id: str) -> requests.Response:
        """ Get file metadata from the API. This is a database operation.

        Args:
            file_id: ID of the file to get metadata for.

        Returns:
            Response from the API.
        """
        return self._get(f"/database/select/{file_id}")

    def get_all_file_metadata(self) -> requests.Response:
        """ Get all file metadata from the API. This is a database operation.

        Returns:
            Response from the API.
        """
        return self._get("/database/select_all")

    def get_database_count(self) -> requests.Response:
        """ Get the number of files in the database from the API. This is a database operation.

        Returns:
            Response from the API.
        """
        return self._get("/database/count")
