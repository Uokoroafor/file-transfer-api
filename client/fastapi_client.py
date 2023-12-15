from typing import Optional, Dict
import requests


class FastAPIClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        """Constructor for FastAPIClient.

        Args:
            base_url: Base URL for the API. Defaults to "http://127.0.0.1:8000"
        """
        self.base_url = base_url

    def _get(self, endpoint: str) -> requests.Response:
        """GET request to the API.

        Args:
            endpoint: Endpoint to send the request to.

        Returns:
            Response from the API.
        """
        return requests.get(self.base_url + endpoint)

    def _post(self, endpoint: str, body: Optional[Dict] = None) -> requests.Response:
        """POST request to the API.

        Args:
            endpoint: Endpoint to send the request to.
            body: Body of the request.

        Returns:
            Response from the API.
        """
        return requests.post(self.base_url + endpoint, json=body)

    def _put(self, endpoint: str, body: Optional[Dict] = None) -> requests.Response:
        """PUT request to the API.

        Args:
            endpoint: Endpoint to send the request to.
            body: Body of the request.

        Returns:
            Response from the API.
        """
        return requests.put(self.base_url + endpoint, json=body)

    def _delete(self, endpoint: str) -> requests.Response:
        """DELETE request to the API.

        Args:
            endpoint: Endpoint to send the request to.

        Returns:
            Response from the API.
        """
        return requests.delete(self.base_url + endpoint)

    def upload_file(self, file_path: str) -> requests.Response:
        """Upload a file to the API.

        Args:
            file_path: Path to the file to upload.

        Returns:
            Response from the API.
        """
        with open(file_path, "rb") as f:
            return self._post("/full/upload", body={"file": f})

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
        with open(file_path, "rb") as f:
            return self._put(f"/full/replace/{file_id}", body={"file": f})

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
        self._delete(f"/full/delete/{file_id}")

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



