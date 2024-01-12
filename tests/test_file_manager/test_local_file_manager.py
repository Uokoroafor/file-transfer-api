import tempfile
from io import BytesIO
from pathlib import Path
from unittest.mock import patch
import pytest
from exceptions.file_exceptions import FileUploadError, FileDoesNotExistError, FileDownloadError, FileUpdateError, \
    FileDeleteError
from file_manager.local_file_manager import LocalFileManager

DATA_DIR = Path("tests/test_fixtures/data")
UPLOAD_DIR = DATA_DIR / "uploads"
DOWNLOAD_DIR = DATA_DIR / "downloads"


@pytest.fixture(scope="session")
def file_system():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    yield

    # Teardown: remove files and directories
    for directory in [UPLOAD_DIR, DOWNLOAD_DIR, DATA_DIR]:
        for file in directory.iterdir():
            file.unlink()
        directory.rmdir()


@pytest.fixture(scope="session")
def file_manager():
    yield LocalFileManager()


@pytest.fixture
def temp_file(file_system):
    with tempfile.NamedTemporaryFile(dir=DATA_DIR, delete=False) as f:
        f.write(b"test data")
        f.flush()
    yield f.name


@pytest.fixture
def temp_upload_file(file_system):
    # Write a temporary file to the upload directory and yield the file location
    with tempfile.NamedTemporaryFile(dir=UPLOAD_DIR, delete=False) as f:
        f.write(b"test data")
        f.flush()
    yield f.name


@pytest.fixture
def temp_rename_file(file_system):
    # Write a temporary file to the data directory and yield the file location
    with tempfile.NamedTemporaryFile(dir=UPLOAD_DIR, delete=False) as f:
        f.write(b"test data")
        f.flush()
    yield f.name


@patch("file_manager.local_file_manager.upload_path", UPLOAD_DIR)
@patch("file_manager.local_file_manager.download_path", DOWNLOAD_DIR)
class TestLocalFileManager:
    def test_upload_file_moves_file_to_upload_directory(self, file_manager, temp_file, file_system):
        with open(temp_file, "rb") as f:
            temp_path = file_manager.upload_file(f)

        # Check that the file has been moved to the upload directory
        assert temp_path.name in [file.name for file in UPLOAD_DIR.iterdir()]

    def test_upload_file_raises_error_when_file_upload_fails(self, file_manager, file_system):
        with patch("builtins.open", side_effect=IOError("Failed to open")) as mock_open:
            with pytest.raises(FileUploadError):
                file_manager.upload_file(BytesIO(b"test data"))

        mock_open.assert_called_once()

    def test_download_file_moves_file_to_download_directory(self, file_manager, temp_upload_file):
        file_id = Path(temp_upload_file).name
        file_manager.download_file(file_id)

        assert file_id in [file.name for file in DOWNLOAD_DIR.iterdir()]

    def test_download_file_raises_error_when_file_does_not_exist(self, file_manager, file_system):
        with pytest.raises(FileDoesNotExistError):
            # Check that it raises a FileDoesNotExistError when the file does not exist
            file_manager.download_file("nonexistent_file")

    def test_download_file_raises_error_when_file_download_fails(self, file_manager, temp_upload_file):
        file_id = Path(temp_upload_file).name

        with patch("builtins.open", side_effect=IOError("Failed to open")):
            with pytest.raises(FileDownloadError):
                # Check that it raises a FileDownloadError when the file download fails
                file_manager.download_file(file_id)

    def test_rename_file_renames_file_in_upload_directory(self, file_manager, temp_rename_file):
        file_id = Path(temp_rename_file).name
        new_file_id = "new_file_id"
        file_manager.rename_file(file_id, new_file_id)
        # Check that the file has been renamed
        assert new_file_id in [file.name for file in UPLOAD_DIR.iterdir()]

    def test_rename_file_raises_error_when_file_does_not_exist(self, file_manager):
        with pytest.raises(FileDoesNotExistError):
            # Check that it raises a FileDoesNotExistError when the file does not exist
            file_manager.rename_file("nonexistent_file", "new_file_id")

    def test_rename_file_raises_error_when_file_rename_fails(self, file_manager, temp_rename_file):
        file_id = Path(temp_rename_file).name
        with patch("pathlib.Path.rename", side_effect=IOError("Failed to rename")):
            with pytest.raises(FileUpdateError):
                file_manager.rename_file(file_id, "new_file_id")

    def test_delete_file_deletes_file_from_upload_directory(self, file_manager, temp_upload_file):
        file_id = Path(temp_upload_file).name
        file_manager.delete_file(file_id)
        # Check that the file has been deleted
        assert file_id not in [file.name for file in UPLOAD_DIR.iterdir()]

    def test_delete_file_raises_error_when_file_does_not_exist(self, file_manager):
        with pytest.raises(FileDoesNotExistError):
            # Check that it raises a FileDoesNotExistError when the file does not exist
            file_manager.delete_file("nonexistent_file")

    def test_delete_file_raises_error_when_file_delete_fails(self, file_manager, temp_upload_file):
        file_id = Path(temp_upload_file).name
        with patch("pathlib.Path.unlink", side_effect=IOError("Failed to delete")):
            with pytest.raises(FileDeleteError):
                # Check that it raises a FileDeleteError when the file delete fails
                file_manager.delete_file(file_id)
