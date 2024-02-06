from io import BytesIO
from pathlib import Path

import pytest

from file_transfer_api.src.exceptions.file_exceptions import FileUploadError, FileDoesNotExistError, FileDownloadError, FileUpdateError, \
    FileDeleteError


class TestLocalFileManager:

    @pytest.fixture(autouse=True)
    def setup_method(self, monkeypatch, file_system):
        data_dir, upload_dir, download_dir = file_system
        monkeypatch.setattr("file_transfer_api.src.file_manager.local_file_manager.upload_path", upload_dir)
        monkeypatch.setattr("file_transfer_api.src.file_manager.local_file_manager.download_path", download_dir)

    def mock_function_failure(self, monkeypatch, function, exception):
        def mock_function(*args, **kwargs):
            raise exception

        monkeypatch.setattr(function, mock_function)

    def test_upload_file_moves_file_to_upload_directory(self, file_manager, temp_file, file_system):
        upload_dir = file_system[1]
        with open(temp_file, "rb") as f:
            temp_path = file_manager.upload_file(f)

        # Check that the file has been moved to the upload directory
        assert temp_path.name in [file.name for file in upload_dir.iterdir()]

    def test_upload_file_raises_error_when_file_upload_fails(self, file_manager, file_system, monkeypatch):

        self.mock_function_failure(monkeypatch, "builtins.open", IOError("Failed to open"))
        with pytest.raises(FileUploadError):
            file_manager.upload_file(BytesIO(b"test data"))

    def test_download_file_moves_file_to_download_directory(self, file_manager, temp_upload_file, file_system):
        download_dir = file_system[2]
        file_id = Path(temp_upload_file).name
        file_manager.download_file(file_id)

        assert file_id in [file.name for file in download_dir.iterdir()]

    def test_download_file_raises_error_when_file_does_not_exist(self, file_manager, file_system):
        with pytest.raises(FileDoesNotExistError):
            # Check that it raises a FileDoesNotExistError when the file does not exist
            file_manager.download_file("nonexistent_file")

    def test_download_file_raises_error_when_file_download_fails(self, file_manager, temp_upload_file, monkeypatch):
        file_id = Path(temp_upload_file).name
        self.mock_function_failure(monkeypatch, "builtins.open", IOError("Failed to open"))
        with pytest.raises(FileDownloadError):
            file_manager.download_file(file_id)

    def test_rename_file_renames_file_in_upload_directory(self, file_manager, temp_rename_file, file_system):
        upload_dir = file_system[1]
        file_id = Path(temp_rename_file).name
        new_file_id = "new_file_id"
        file_manager.rename_file(file_id, new_file_id)
        # Check that the file has been renamed
        assert new_file_id in [file.name for file in upload_dir.iterdir()]

    def test_rename_file_raises_error_when_file_does_not_exist(self, file_manager):
        with pytest.raises(FileDoesNotExistError):
            # Check that it raises a FileDoesNotExistError when the file does not exist
            file_manager.rename_file("nonexistent_file", "new_file_id")

    def test_rename_file_raises_error_when_file_rename_fails(self, file_manager, temp_rename_file, monkeypatch):
        file_id = Path(temp_rename_file).name
        self.mock_function_failure(monkeypatch, "pathlib.Path.rename", IOError("Failed to rename"))
        with pytest.raises(FileUpdateError):
            file_manager.rename_file(file_id, "new_file_id")

    def test_delete_file_deletes_file_from_upload_directory(self, file_manager, temp_upload_file, file_system):
        upload_dir = file_system[1]
        file_id = Path(temp_upload_file).name
        file_manager.delete_file(file_id)
        # Check that the file has been deleted
        assert file_id not in [file.name for file in upload_dir.iterdir()]

    def test_delete_file_raises_error_when_file_does_not_exist(self, file_manager):
        with pytest.raises(FileDoesNotExistError):
            # Check that it raises a FileDoesNotExistError when the file does not exist
            file_manager.delete_file("nonexistent_file")

    def test_delete_file_raises_error_when_file_delete_fails(self, file_manager, temp_upload_file, monkeypatch):
        try:
            file_id = Path(temp_upload_file).name
            self.mock_function_failure(monkeypatch, "pathlib.Path.unlink", OSError("Failed to delete"))
            with pytest.raises(FileDeleteError):
                file_manager.delete_file(file_id)

        finally:
            # Undo the patch to prevent the teardown from failing
            monkeypatch.undo()
