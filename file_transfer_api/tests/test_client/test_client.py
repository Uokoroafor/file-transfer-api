import os
import tempfile

import pytest
import requests_mock

from file_transfer_api.src.client.client import APIClient
from file_transfer_api.src.schemas.custom_responses import FileIdAndPath, ErrorResponse

base_url = "http://test_url"   # "http://127.0.0.1:8000"


class MockOpen:
    """Mock open context manager to mock the open function in pytest."""

    def __init__(self, mock_data):
        self.mock_data = mock_data

    def __enter__(self):
        return self.mock_data

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class TestAPIClient:
    @pytest.fixture(scope="function")
    def api_client(self, request, monkeypatch):
        with requests_mock.Mocker() as m:
            # Mock successful and error responses for all requests
            if request.param == "success":
                m.post(f"{base_url}/files", json={"file_id": "test_file_id", "file_path": "test_file_path"})
                m.get(f"{base_url}/files/test_file_id", text="test data")
                m.put(f"{base_url}/files/test_file_id",
                      json={"file_id": "test_file_id", "file_path": "test_file_path"})
                m.delete(f"{base_url}/files/test_file_id",
                         json={"file_id": "test_file_id", "file_path": "test_file_path"})
            else:
                m.post(f"{base_url}/files", status_code=500, json={"detail": "File Upload Failed"})
                m.get(f"{base_url}/files/test_file_id", status_code=500, json={"detail": "File Download Failed"})
                m.put(f"{base_url}/files/test_file_id", status_code=500, json={"detail": "File Rename Failed"})
                m.delete(f"{base_url}/files/test_file_id", status_code=500, json={"detail": "File Delete Failed"})

            temp_log_file = tempfile.NamedTemporaryFile(delete=False)
            self.error_logger_path = temp_log_file.name
            temp_log_file.close()

            client = APIClient(base_url=base_url, error_logger_path=self.error_logger_path)
            yield client

            os.remove(self.error_logger_path)

    def read_log_file(self):
        with open(self.error_logger_path, "r") as f:
            return f.read()

    def is_content_in_log_file(self, content):
        log_contents = self.read_log_file()
        return content in log_contents

    def mock_open_path(self, monkeypatch, function, mock_data):
        def mock_function(*args, **kwargs):
            return MockOpen(mock_data)

        monkeypatch.setattr(function, mock_function)

    @pytest.mark.parametrize("api_client", ["success"], indirect=True)
    def test_upload_file_returns_file_id_and_path_when_successful(self, api_client, monkeypatch):
        try:
            self.mock_open_path(monkeypatch, "builtins.open", b"test_data")
            response = api_client.upload_file("test_file_path")

            assert response == FileIdAndPath(file_id="test_file_id", file_path="test_file_path")

        finally:
            # Reset the open function
            monkeypatch.undo()

    @pytest.mark.parametrize("api_client", ["error"], indirect=True)
    def test_upload_file_returns_error_response_when_file_upload_fails(self, api_client, monkeypatch):
        try:
            self.mock_open_path(monkeypatch, "builtins.open", b"test_data")
            response = api_client.upload_file("test_file_path")

            assert response == ErrorResponse(status_code=500, message="File Upload Failed")

        finally:
            # Reset the open function
            monkeypatch.undo()

        assert self.is_content_in_log_file("Error")

    @pytest.mark.parametrize("api_client", ["success"], indirect=True)
    def test_upload_file_returns_error_response_when_file_path_does_not_exist(self, api_client):
        response = api_client.upload_file("nonexistent_file_path")

        assert response == ErrorResponse(status_code=404, message="No such file or directory at: nonexistent_file_path")
        assert self.is_content_in_log_file("Error")

    @pytest.mark.parametrize("api_client", ["success"], indirect=True)
    def test_download_file_returns_file_content_when_successful(self, api_client):
        response = api_client.download_file("test_file_id")

        assert response == b"test data"

    @pytest.mark.parametrize("api_client", ["error"], indirect=True)
    def test_download_file_returns_error_response_when_file_download_fails(self, api_client):
        response = api_client.download_file("test_file_id")

        assert response == ErrorResponse(status_code=500, message="File Download Failed")
        assert self.is_content_in_log_file("Error")

    @pytest.mark.parametrize("api_client", ["success"], indirect=True)
    def test_rename_file_returns_file_id_and_path_when_successful(self, api_client):
        response = api_client.rename_file("test_file_id", "new_file_id")

        assert response == FileIdAndPath(file_id="test_file_id", file_path="test_file_path")

    @pytest.mark.parametrize("api_client", ["error"], indirect=True)
    def test_rename_file_returns_error_response_when_file_rename_fails(self, api_client):
        response = api_client.rename_file("test_file_id", "new_file_id")

        assert response == ErrorResponse(status_code=500, message="File Rename Failed")
        assert self.is_content_in_log_file("Error")

    @pytest.mark.parametrize("api_client", ["success"], indirect=True)
    def test_delete_file_returns_file_id_and_path_when_successful(self, api_client):
        response = api_client.delete_file("test_file_id")

        assert response == FileIdAndPath(file_id="test_file_id", file_path="test_file_path")

    #
    @pytest.mark.parametrize("api_client", ["error"], indirect=True)
    def test_delete_file_returns_error_response_when_file_delete_fails(self, api_client):
        response = api_client.delete_file("test_file_id")

        assert response == ErrorResponse(status_code=500, message="File Delete Failed")
        assert self.is_content_in_log_file("Error")
