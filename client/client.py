from pathlib import Path
from typing import Optional, Union, ByteString
import requests

from schemas.custom_responses import FileIdAndPath, ErrorResponse
from utils.logging_utils import ErrorLogger


class APIClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000", error_logger_path: Optional[str] = None):
        """Constructor for FastAPIClient.

        Args:
            base_url: Base URL for the API. Defaults to "http://127.0.0.1:8000"
        """
        self.base_url = base_url
        self.logger = ErrorLogger(log_file_path=error_logger_path, name="APIClient")

    def request_handler(self, response: requests.Response, raw: bool = False) -> Union[FileIdAndPath, ByteString, ErrorResponse]:
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
            self.logger.log_error(f"Error uploading file: {response.status_code} - {response.json()['detail']}")
            return ErrorResponse(status_code=response.status_code,
                                 message=response.json()['detail'])

    def upload_file(self, file_path: Union[str, Path]) -> Union[FileIdAndPath, ErrorResponse]:
        """Upload a file to the API.

        Args:
            file_path: Path to the file to upload.

        Returns:
            Response from the API.
        """
        with open(file_path, "rb") as f:
            response = requests.post(self.base_url + "/files", files={"file": f})
            return self.request_handler(response)

    def download_file(self, file_id: str) -> Union[ByteString, ErrorResponse]:
        """Download a file from the API.

        Args:
            file_id: ID of the file to download.

        Returns:
            Response from the API.
        """
        response = requests.get(self.base_url + f"/files/{file_id}")
        return self.request_handler(response, raw=True)

    def rename_file(self, file_id: str, new_file_id: str) -> Union[FileIdAndPath, ErrorResponse]:
        """Rename a file in the API.

        Args:
            file_id: ID of the file to rename.
            new_file_id: New ID of the file.

        Returns:
            Response from the API.
        """
        response = requests.put(self.base_url + f"/files/{file_id}", params={"new_file_id": new_file_id})
        return self.request_handler(response)

    def delete_file(self, file_id: str) -> Union[FileIdAndPath, ErrorResponse]:
        """Delete a file from the API.

        Args:
            file_id: ID of the file to delete.

        Returns:
            Response from the API.
        """
        response = requests.delete(self.base_url + f"/files/{file_id}")
        return self.request_handler(response)


if __name__ == '__main__':
    client = APIClient(error_logger_path="../logs/errors.log")
    response1 = client.upload_file("../data/test.png")
    response2 = client.download_file(response1.file_id+"1")
    response3 = client.rename_file(response1.file_id, "test2.png")
    response4 = client.delete_file("test2.png")
    pass
