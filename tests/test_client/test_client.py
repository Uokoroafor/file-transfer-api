import os
import tempfile

import pytest
import requests_mock

from client.client import APIClient
from schemas.custom_responses import FileIdAndPath, ErrorResponse

base_url = "http://127.0.0.1:8000"
error_logger_path = "tests/test_fixtures/error.log"


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
    def api_client(self):
        # return APIClient(base_url=base_url, error_logger_path=error_logger_path)
        temp_log_file = tempfile.NamedTemporaryFile(delete=False)
        self.error_logger_path = temp_log_file.name
        temp_log_file.close()

        client = APIClient(base_url=base_url, error_logger_path=self.error_logger_path)
        yield client

        os.remove(self.error_logger_path)

    @pytest.fixture
    def mock_response(self):
        with requests_mock.Mocker() as m:
            yield m

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

    def test_upload_file_returns_file_id_and_path_when_successful(self, api_client, mock_response, monkeypatch):
        mock_response.post(f"{base_url}/files", json={"file_id": "test_file_id", "file_path": "test_file_path"})
        self.mock_open_path(monkeypatch, "builtins.open", b"test_data")
        response = api_client.upload_file("test_file_path")

        assert response == FileIdAndPath(file_id="test_file_id", file_path="test_file_path")

    def test_upload_file_returns_error_response_when_file_upload_fails(self, api_client, mock_response,
                                                                       monkeypatch):
        try:
            mock_response.post(f"{base_url}/files", status_code=404, json={"detail": "File Upload Failed"})
            self.mock_open_path(monkeypatch, "builtins.open", b"test_data")
            response = api_client.upload_file("test_file_path")

            assert response == ErrorResponse(status_code=404, message="File Upload Failed")

        finally:
            # Reset the open function
            monkeypatch.undo()
        assert self.is_content_in_log_file("Error")

    def test_upload_file_returns_error_response_when_file_path_does_not_exist(self, api_client, mock_response):
        response = api_client.upload_file("nonexistent_file_path")
        assert response == ErrorResponse(status_code=404, message="No such file or directory at: nonexistent_file_path")

        # Check that the error log is not empty
        assert self.is_content_in_log_file("Error")

    def test_download_file_returns_file_content_when_successful(self, api_client, mock_response):
        mock_response.get(f"{base_url}/files/test_file_id", text="test data")
        response = api_client.download_file("test_file_id")
        assert response == b"test data"

    def test_download_file_returns_error_response_when_file_download_fails(self, api_client, mock_response):
        mock_response.get(f"{base_url}/files/test_file_id", status_code=404, json={"detail": "File Download Failed"})
        response = api_client.download_file("test_file_id")

        assert response == ErrorResponse(status_code=404, message="File Download Failed")

        # Check that the error log is not empty
        assert self.is_content_in_log_file("Error")

    def test_rename_file_returns_file_id_and_path_when_successful(self, api_client, mock_response):
        mock_response.put(f"{base_url}/files/test_file_id",
                          json={"file_id": "test_file_id", "file_path": "test_file_path"})
        response = api_client.rename_file("test_file_id", "new_file_id")

        assert response == FileIdAndPath(file_id="test_file_id", file_path="test_file_path")

    def test_rename_file_returns_error_response_when_file_rename_fails(self, api_client, mock_response):
        mock_response.put(f"{base_url}/files/test_file_id", status_code=404, json={"detail": "File Rename Failed"})
        response = api_client.rename_file("test_file_id", "new_file_id")

        assert response == ErrorResponse(status_code=404, message="File Rename Failed")
        # Check that the error log is not empty
        assert self.is_content_in_log_file("Error")

    def test_delete_file_returns_file_id_and_path_when_successful(self, api_client, mock_response):
        mock_response.delete(f"{base_url}/files/test_file_id",
                             json={"file_id": "test_file_id", "file_path": "test_file_path"})
        response = api_client.delete_file("test_file_id")

        assert response == FileIdAndPath(file_id="test_file_id", file_path="test_file_path")

    def test_delete_file_returns_error_response_when_file_delete_fails(self, api_client, mock_response):
        mock_response.delete(f"{base_url}/files/test_file_id", status_code=404, json={"detail": "File Delete Failed"})
        response = api_client.delete_file("test_file_id")

        assert response == ErrorResponse(status_code=404, message="File Delete Failed")
        # Check that the error log is not empty
        assert self.is_content_in_log_file("Error")
