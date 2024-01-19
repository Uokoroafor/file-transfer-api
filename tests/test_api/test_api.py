import pytest
from fastapi.testclient import TestClient

from api.api import app


class TestAPI:
    @pytest.fixture(scope="function")
    def client(self):
        with TestClient(app) as client:
            yield client

    @pytest.fixture(scope="function")
    def uploaded_file(self, client, temp_file, file_system):
        # Upload a file and yield the file_id
        with open(temp_file, "rb") as f:
            response = client.post(f"/files/", files={"file": f})
        file_id = response.json().get("file_id")
        yield file_id

        # Teardown: delete the file
        client.delete(f"/files/{file_id}")

    # Get root endpoint
    def test_root_endpoint_returns_200_and_welcome_message(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()

    # Post file endpoint
    def test_post_file_endpoint_returns_200_and_file_id_and_path(self, client, temp_file, file_system):
        response = client.post(f"/files/", files={"file": open(temp_file, "rb")})
        assert response.status_code == 200
        assert "file_id" in response.json()
        assert "file_path" in response.json()

    # Get files/{file_id} endpoint
    def test_get_file_endpoint_returns_200_and_file(self, client, uploaded_file):
        response = client.get(f"/files/{uploaded_file}")
        assert response.status_code == 200
        assert response.content == b"test data"

    def test_get_file_endpoint_returns_404_when_file_does_not_exist(self, client):
        response = client.get(f"/files/nonexistent_file")
        assert response.status_code == 404
        assert "detail" in response.json()

    # Put files/{file_id} endpoint
    def test_put_file_endpoint_returns_200(self, client, uploaded_file):
        response = client.put(f"/files/{uploaded_file}", params={"new_file_name": "new_file_name"})
        assert response.status_code == 200

    def test_put_file_endpoint_returns_404_when_file_does_not_exist(self, client):
        response = client.put(f"/files/nonexistent_file", params={"new_file_name": "new_file_name"})
        assert response.status_code == 404
        assert "detail" in response.json()

    # Delete files/{file_id} endpoint
    def test_delete_file_endpoint_returns_200(self, client, uploaded_file):
        response = client.delete(f"/files/{uploaded_file}")
        assert response.status_code == 200

    def test_delete_file_endpoint_returns_404_when_file_does_not_exist(self, client):
        response = client.delete(f"/files/nonexistent_file")
        assert response.status_code == 404
        assert "detail" in response.json()
