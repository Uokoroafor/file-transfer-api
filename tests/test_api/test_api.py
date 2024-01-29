import pytest
from fastapi.testclient import TestClient
from api.api import app


class TestAPI:

    @pytest.fixture(autouse=True, scope="function")
    def setup_file_system(self, monkeypatch, file_system):
        data_dir, upload_dir, download_dir = file_system
        monkeypatch.setattr("file_manager.local_file_manager.upload_path", upload_dir)
        monkeypatch.setattr("file_manager.local_file_manager.download_path", download_dir)

        yield

        # Unpatch all
        monkeypatch.undo()

    @pytest.fixture(autouse=True, scope="function")
    def setup_database_manager(self, monkeypatch, test_db_session):
        # monkeypatch.setattr("api.routers.fastapi_router.database_manager", test_db_manager)
        monkeypatch.setattr("api.routers.fastapi_router.database_manager.db", test_db_session)

        yield

        # Unpatch all
        monkeypatch.undo()

    @pytest.fixture(scope="function")
    def client(self):
        with TestClient(app) as client:
            yield client

    @pytest.fixture(scope="function")
    def uploaded_file(self, client, file_system, test_database_entry):
        # Put a file in upload directory and write it to database and yield the file_id
        data_dir, upload_dir, download_dir = file_system
        with open(upload_dir / "test_id_1", "wb") as f:
            f.write(b"test data")
        yield "test_id_1"

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
