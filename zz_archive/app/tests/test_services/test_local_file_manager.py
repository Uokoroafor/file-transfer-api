import tempfile
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

import pytest

from app.exceptions.custom_exceptions import FileUploadError, FileDoesNotExistError, FileDownloadError, FileReplaceError, \
    FileDeleteError, FileRenameError
from app.services.local_file_manager import LocalFileManager

DATA_DIR = Path("../test_fixtures/data")
UPLOAD_DIR = DATA_DIR / "uploads"
DOWNLOAD_DIR = DATA_DIR / "downloads"


@pytest.fixture(scope="function")
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


@pytest.fixture
def file_manager():
    return LocalFileManager()


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
def temp_replace_file(file_system):
    # Write a temporary file to the data directory and yield the file location
    with tempfile.NamedTemporaryFile(dir=DATA_DIR, delete=False) as f:
        f.write(b"replace data")
        f.flush()
    yield f.name


@pytest.fixture
def temp_rename_file(file_system):
    # Write a temporary file to the data directory and yield the file location
    with tempfile.NamedTemporaryFile(dir=UPLOAD_DIR, delete=False) as f:
        f.write(b"test data")
        f.flush()
    yield f.name


@patch("app.services.local_file_manager.upload_directory", UPLOAD_DIR)
@patch("app.services.local_file_manager.download_directory", DOWNLOAD_DIR)
class TestLocalFileManager:
    def test_upload_file_moves_file_to_upload_directory(self, file_manager, temp_file, file_system):
        with open(temp_file, "rb") as f:
            file_id, message = file_manager.upload_file(f)

        assert file_id in [file.name for file in UPLOAD_DIR.iterdir()]
        assert message == f"File with id {file_id} uploaded to {UPLOAD_DIR}"

    def test_upload_file_raises_error_when_file_upload_fails(self, file_manager, file_system):
        with patch("builtins.open", side_effect=IOError("Failed to open")):
            with pytest.raises(FileUploadError) as excinfo:
                file_manager.upload_file(BytesIO(b"test data"))

        assert "Error occurred during file upload" in str(excinfo.value)

    def test_download_file_moves_file_to_download_directory(self, file_manager, temp_upload_file):
        file_id = Path(temp_upload_file).name
        message = file_manager.download_file(file_id)

        assert file_id in [file.name for file in DOWNLOAD_DIR.iterdir()]
        assert message == f"File downloaded as {file_id} to {DOWNLOAD_DIR}"

    def test_download_file_raises_error_when_file_does_not_exist(self, file_manager, file_system):
        # Try to download a file that doesn't exist
        with pytest.raises(FileDoesNotExistError) as excinfo:
            file_manager.download_file("nonexistent_file")

        assert "File does not exist at" in str(excinfo.value)

    def test_download_file_raises_error_when_file_download_fails(self, file_manager, temp_upload_file):
        file_id = Path(temp_upload_file).name

        with patch("builtins.open", side_effect=Exception("Unexpected error")):
            with pytest.raises(FileDownloadError) as excinfo:
                file_manager.download_file(file_id)

        assert "Error occurred during file download" in str(excinfo.value)

    def test_replace_file_replaces_file_in_upload_directory(self, file_manager, temp_upload_file, temp_replace_file):
        file_id = Path(temp_upload_file).name
        with open(temp_replace_file, "rb") as f:
            message = file_manager.replace_file(file_id, f)
            f.flush()

        with open(temp_upload_file, "rb") as f:
            file_content = f.read()
            assert file_content == b"replace data", f"Unexpected file content: {file_content}"
        assert message == f"File with id {file_id} replaced"

    def test_replace_file_raises_error_when_file_does_not_exist(self, file_manager, temp_replace_file):
        with open(temp_replace_file, "rb") as f:
            with pytest.raises(FileDoesNotExistError) as excinfo:
                file_manager.replace_file("nonexistent_file", f)

        assert "File does not exist at" in str(excinfo.value)

    def test_replace_file_raises_error_when_file_replace_fails(self, file_manager, temp_upload_file, temp_replace_file):
        file_id = Path(temp_upload_file).name
        with open(temp_replace_file, "rb") as f:
            with patch("builtins.open", side_effect=Exception("Unexpected error")):
                with pytest.raises(FileReplaceError) as excinfo:
                    file_manager.replace_file(file_id, f)

        assert "Error occurred during file replace" in str(excinfo.value)

    def test_rename_file_renames_file_in_upload_directory(self, file_manager, temp_rename_file):
        file_id = Path(temp_rename_file).name
        new_file_id = "new_file_id"
        message = file_manager.rename_file(file_id, new_file_id)
        print(message)
        assert message == f"File with id {file_id} renamed to {new_file_id}"
        assert new_file_id in [file.name for file in UPLOAD_DIR.iterdir()]

    def test_rename_file_raises_error_when_file_does_not_exist(self, file_manager):
        with pytest.raises(FileDoesNotExistError) as excinfo:
            file_manager.rename_file("nonexistent_file", "new_file_id")

        assert "File does not exist at" in str(excinfo.value)

    def test_rename_file_raises_error_when_file_rename_fails(self, file_manager, temp_rename_file):
        file_id = Path(temp_rename_file).name
        with patch("pathlib.Path.rename", side_effect=Exception("Unexpected error")):
            with pytest.raises(FileRenameError) as excinfo:
                file_manager.rename_file(file_id, "new_file_id")

        assert "Error occurred during file rename" in str(excinfo.value)

    def test_delete_file_deletes_file_from_upload_directory(self, file_manager, temp_upload_file):
        file_id = Path(temp_upload_file).name
        message = file_manager.delete_file(file_id)

        assert message == f"File with id {file_id} deleted"
        assert file_id not in [file.name for file in UPLOAD_DIR.iterdir()]

    def test_delete_file_raises_error_when_file_does_not_exist(self, file_manager):
        with pytest.raises(FileDoesNotExistError) as excinfo:
            file_manager.delete_file("nonexistent_file")

        assert "File does not exist at" in str(excinfo.value)

    def test_delete_file_raises_error_when_file_delete_fails(self, file_manager, temp_upload_file):
        file_id = Path(temp_upload_file).name
        with patch("pathlib.Path.unlink", side_effect=Exception("Unexpected error")):
            with pytest.raises(FileDeleteError) as excinfo:
                file_manager.delete_file(file_id)

        assert "Error occurred during file delete" in str(excinfo.value)
