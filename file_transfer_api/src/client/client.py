from pathlib import Path
from typing import Optional, Union, ByteString
import requests

from src.schemas.custom_responses import FileIdAndPath, ErrorResponse
from src.utils.logging_utils import ErrorLogger


class APIClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000", error_logger_path: Optional[str] = None):
        """Constructor for FastAPIClient.

        Args:
            base_url: Base URL for the API. Defaults to "http://127.0.0.1:8000"
        """
        self.base_url = base_url
        self.logger = ErrorLogger(log_file_path=error_logger_path, name="APIClient")

    def _request_handler(self, response: requests.Response, raw: bool = False) -> (
            Union)[FileIdAndPath, ByteString, ErrorResponse]:
        """Handle the response from the API.

        Args:
            response: Response from the API.
            raw: Whether to return the raw content of the response. Defaults to False.

        Returns:
            Response from the API.
        """
        if response.ok:
            if raw:
                return response.content
            else:
                response = response.json()
                return FileIdAndPath(file_id=response["file_id"],
                                     file_path=response["file_path"])
        else:
            self.logger.log(f"Error: {response.status_code} - {response.json()['detail']}")
            return ErrorResponse(status_code=response.status_code,
                                 message=response.json()['detail'])

    def upload_file(self, file_path: Union[str, Path]) -> Union[FileIdAndPath, ErrorResponse]:
        """Upload a file to the API.

        Args:
            file_path: Path to the file to upload.

        Returns:
            Response from the API.
        """
        try:
            with open(file_path, "rb") as f:
                response = requests.post(f"{self.base_url}/files", files={"file": f})
                return self._request_handler(response)
        except FileNotFoundError as e:
            self.logger.log(f"Error uploading file: {e}")
            return ErrorResponse(status_code=404, message=f"No such file or directory at: {file_path}")

    def download_file(self, file_id: str) -> Union[ByteString, ErrorResponse]:
        """Download a file from the API.

        Args:
            file_id: ID of the file to download.

        Returns:
            Response from the API.
        """
        response = requests.get(f"{self.base_url}/files/{file_id}")
        return self._request_handler(response, raw=True)

    def rename_file(self, file_id: str, new_file_name: str) -> Union[FileIdAndPath, ErrorResponse]:
        """Rename a file in the API.

        Args:
            file_id: ID of the file to rename.
            new_file_name: New ID of the file.

        Returns:
            Response from the API.
        """
        response = requests.put(f"{self.base_url}/files/{file_id}", params={"new_file_name": new_file_name})
        return self._request_handler(response)

    def delete_file(self, file_id: str) -> Union[FileIdAndPath, ErrorResponse]:
        """Delete a file from the API.

        Args:
            file_id: ID of the file to delete.

        Returns:
            Response from the API.
        """
        response = requests.delete(f"{self.base_url}/files/{file_id}")
        return self._request_handler(response)


# TODO: Use Marshmallow to validate the response from the API
