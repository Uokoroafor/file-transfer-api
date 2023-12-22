from pathlib import Path
from typing import Optional, Union, ByteString
import requests
# from requests.exceptions import HTTPError
# from app.utils.logging_utils import ErrorLogger
# import mimetypes

# from starlette.responses import FileResponse

from api.fastapi_router import CustomResponseWithFileIdAndPath, CustomResponseWithFileID


class FastAPIClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000", error_logger_path: Optional[str] = None):
        """Constructor for FastAPIClient.

        Args:
            base_url: Base URL for the API. Defaults to "http://127.0.0.1:8000"
        """
        self.base_url = base_url
        # self.logger = ErrorLogger(log_file_path=error_logger_path, name="FastAPIClient")

    # def _handle_http_error(self, e: HTTPError) -> None:
    #     """Handle HTTP errors.
    #
    #     Args:
    #         e: HTTPError to handle.
    #     """
    #     # self.logger.log_error(f"HTTP error occurred: {e}")
    #     raise e
    #
    # def _handle_connection_error(self, e: requests.exceptions.ConnectionError) -> None:
    #     """Handle connection errors.
    #
    #     Args:
    #         e: ConnectionError to handle.
    #     """
    #     # self.logger.log_error(f"Connection error occurred: {e}")
    #     raise ConnectionError(f"Connection error occurred. Please check the API is running at {self.base_url}."
    #                           f" \n Error Details: {e}")


    def upload_file(self, file_path: Union[str, Path]) -> CustomResponseWithFileIdAndPath:
        """Upload a file to the API.

        Args:
            file_path: Path to the file to upload.

        Returns:
            Response from the API.
        """
        # content_type, _ = mimetypes.guess_type(file_path) or ("multipart/form-data", None)
        with open(file_path, "rb") as f:
            response = requests.post(self.base_url + "/files", files={"file": f})
            if response.ok:
                return CustomResponseWithFileIdAndPath(file_id=response.json()["file_id"],
                                                       file_path=response.json()["file_path"])
            else:
                raise Exception(f"Error uploading file: {response.status_code} - {response.text}")

    def download_file(self, file_id: str) -> ByteString:
        """Download a file from the API.

        Args:
            file_id: ID of the file to download.

        Returns:
            Response from the API.
        """
        response = requests.get(self.base_url + f"/files/{file_id}")
        if response.ok:
            return response.content
        else:
            raise Exception(f"Error downloading file: {response.status_code} - {response.text}")

    def rename_file(self, file_id: str, new_file_id: str) -> CustomResponseWithFileID:
        """Rename a file in the API.

        Args:
            file_id: ID of the file to rename.
            new_file_id: New ID of the file.

        Returns:
            Response from the API.
        """
        response = requests.put(self.base_url + f"/files/{file_id}", params={"new_file_id": new_file_id})
        if response.ok:
            return CustomResponseWithFileID(file_id=response.json()["file_id"])
        else:
            raise Exception(f"Error renaming file: {response.status_code} - {response.text}")

    def delete_file(self, file_id: str) -> CustomResponseWithFileID:
        """Delete a file from the API.

        Args:
            file_id: ID of the file to delete.

        Returns:
            Response from the API.
        """
        response = requests.delete(self.base_url + f"/files/{file_id}")
        if response.ok:
            return CustomResponseWithFileID(file_id=response.json()["file_id"])
        else:
            raise Exception(f"Error deleting file: {response.status_code} - {response.text}")


if __name__ == '__main__':
    client = FastAPIClient()
    response1 = client.upload_file("../data/test.png")
    response2 = client.download_file(response1.file_id)
    response3 = client.rename_file(response1.file_id, "test2.png")
    response4 = client.delete_file("test2.png")
    pass

