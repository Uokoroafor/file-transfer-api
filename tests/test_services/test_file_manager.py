import pytest
from services.file_manager import FileManager
from exceptions.custom_exceptions import FileUploadError, FileDoesNotExistError, FileDownloadError, FileReplaceError, FileDeleteError, FileRenameError
from io import BytesIO
from unittest.mock import mock_open, patch, MagicMock
from pathlib import Path


# Test for successful file upload
def test_upload_file_success():
    file_manager = FileManager()
    mock_file_data = BytesIO(b"test data")
    test_uuid = "test_file_id"

    with patch("builtins.open", mock_open()) as mock_file:
        with patch("uuid.uuid4", return_value="test_file_id"):
            file_id, message = file_manager.upload_file(mock_file_data)

    assert file_id == test_uuid
    assert message == "File uploaded"
    mock_file.assert_called_once()  # Ensure file was attempted to be opened


# Test for file upload failure
def test_upload_file_failure():
    file_manager = FileManager()
    mock_file_data = BytesIO(b"test data")

    with patch("builtins.open", side_effect=IOError("Failed to open")):
        with pytest.raises(FileUploadError) as excinfo:
            file_manager.upload_file(mock_file_data)

    assert "Error occurred during file upload" in str(excinfo.value)


# Test for successful file download
def test_download_file_success():
    file_manager = FileManager()
    test_file_id = "existing_file"
    file_content = b"test data"
    download_location = Path("/mock/download")

    # Mocking Path.is_file to simulate the file's existence in the upload directory
    with patch.object(Path, "is_file", return_value=True):
        # Mocking open for reading from the upload directory and writing to the download directory
        mock_file = MagicMock()
        mock_file.read_bytes.return_value = file_content
        with patch("builtins.open", mock_open(), create=True):
            with patch("pathlib.Path.read_bytes", mock_file.read_bytes):
                with patch("services.file_manager.download_directory", download_location):
                    message = file_manager.download_file(test_file_id)

    assert message == "File downloaded"
    mock_file.read_bytes.assert_called_once()


# Test for failure when trying to download file that doesn't exist - filedoesnotexisterror
def test_download_non_existing_file_failure():
    file_manager = FileManager()
    test_file_id = "nonexistent_file"
    upload_directory = Path("test_file_location")

    with patch("services.file_manager.upload_directory", upload_directory):
        with patch.object(Path, "is_file", return_value=False):
            with pytest.raises(FileDoesNotExistError) as excinfo:
                file_manager.download_file(test_file_id)

    assert f"File does not exist at {upload_directory / test_file_id}" in str(excinfo.value)


# Test for failure when trying to download file that exists but fails to open - filedownloaderror
def test_download_file_failure():
    file_manager = FileManager()
    test_file_id = "test_file"

    with patch.object(Path, "is_file", return_value=True):
        with patch("builtins.open", side_effect=Exception("Unexpected error")):
            with pytest.raises(FileDownloadError) as excinfo:
                file_manager.download_file(test_file_id)

    assert "Error occurred during file download" in str(excinfo.value)


# Test for successful file replace
def test_replace_file_success():
    file_manager = FileManager()
    test_file_id = "existing_file"
    file_content = b"test data"

    # Mocking Path.is_file to simulate the file's existence in the upload directory
    with patch.object(Path, "is_file", return_value=True):
        # Mocking open for reading from the upload directory and writing to the upload directory
        mock_file = MagicMock()
        mock_file.read.return_value = file_content
        with patch("builtins.open", mock_open(), create=True):
            with patch("pathlib.Path.read_bytes", mock_file.read):
                message = file_manager.replace_file(test_file_id, mock_file)

    assert message == "File replaced"
    mock_file.read.assert_called_once()


# Test for failure when trying to replace file that doesn't exist - filedoesnotexisterror
def test_replace_non_existing_file_failure():
    file_manager = FileManager()
    test_file_id = "nonexistent_file"
    upload_directory = Path("test_file_location")
    file_content = b"test data"

    with patch("services.file_manager.upload_directory", upload_directory):
        with patch.object(Path, "is_file", return_value=False):
            with pytest.raises(FileDoesNotExistError) as excinfo:
                mock_file = MagicMock()
                mock_file.read.return_value = file_content
                file_manager.replace_file(test_file_id, mock_file)

    assert f"File does not exist at {upload_directory / test_file_id}" in str(excinfo.value)


def test_replace_file_failure():
    file_manager = FileManager()
    test_file_id = "test_file"
    file_content = b"test data"

    with patch.object(Path, "is_file", return_value=True):
        with patch("builtins.open", side_effect=Exception("Unexpected error")):
            with pytest.raises(FileReplaceError) as excinfo:
                mock_file = MagicMock()
                mock_file.read.return_value = file_content
                file_manager.replace_file(test_file_id, mock_file)

    assert "Error occurred during file replace" in str(excinfo.value)


# Test for successful file delete
def test_delete_file_success():
    file_manager = FileManager()
    test_file_id = "existing_file"

    # Mocking Path.is_file to simulate the file's existence in the upload directory
    with patch.object(Path, "is_file", return_value=True):
        # Mocking open for reading from the upload directory and writing to the upload directory
        with patch("pathlib.Path.unlink") as mock_unlink:
            message = file_manager.delete_file(test_file_id)

    assert message == "File deleted"
    mock_unlink.assert_called_once()


# Test for failure when trying to delete file that doesn't exist - filedoesnotexisterror
def test_delete_non_existing_file_failure():
    file_manager = FileManager()
    test_file_id = "nonexistent_file"
    upload_directory = Path("test_file_location")

    with patch("services.file_manager.upload_directory", upload_directory):
        with patch.object(Path, "is_file", return_value=False):
            with pytest.raises(FileDoesNotExistError) as excinfo:
                file_manager.delete_file(test_file_id)

    assert f"File does not exist at {upload_directory / test_file_id}" in str(excinfo.value)


# Test for failure when trying to delete file that exists due to unexpected error - filedeleteerror
def test_delete_file_failure():
    file_manager = FileManager()
    test_file_id = "test_file"

    with patch.object(Path, "is_file", return_value=True):
        with patch("pathlib.Path.unlink", side_effect=Exception("Unexpected error")):
            with pytest.raises(FileDeleteError) as excinfo:
                file_manager.delete_file(test_file_id)

    assert "Error occurred during file delete" in str(excinfo.value)


# Test for successful file rename
def test_rename_file_success():
    file_manager = FileManager()
    test_file_id = "existing_file"
    new_file_id = "new_file_id"

    # Mocking Path.is_file to simulate the file's existence in the upload directory
    with patch.object(Path, "is_file", return_value=True):
        # Mocking open for reading from the upload directory and writing to the upload directory
        with patch("pathlib.Path.rename") as mock_rename:
            message = file_manager.rename_file(test_file_id, new_file_id)

    assert message == "File renamed"
    mock_rename.assert_called_once()


# Test for failure when trying to rename file that doesn't exist - filedoesnotexisterror
def test_rename_non_existing_file_failure():
    file_manager = FileManager()
    test_file_id = "nonexistent_file"
    new_file_id = "new_file_id"
    upload_directory = Path("test_file_location")

    with patch("services.file_manager.upload_directory", upload_directory):
        with patch.object(Path, "is_file", return_value=False):
            with pytest.raises(FileDoesNotExistError) as excinfo:
                file_manager.rename_file(test_file_id, new_file_id)

    assert f"File does not exist at {upload_directory / test_file_id}" in str(excinfo.value)


# Test for failure when trying to rename file that exists due to unexpected error - filerenameerror
def test_rename_file_failure():
    file_manager = FileManager()
    test_file_id = "test_file"
    new_file_id = "new_file_id"

    with patch.object(Path, "is_file", return_value=True):
        with patch("pathlib.Path.rename", side_effect=Exception("Unexpected error")):
            with pytest.raises(FileRenameError) as excinfo:
                file_manager.rename_file(test_file_id, new_file_id)

    assert "Error occurred during file rename" in str(excinfo.value)

# TODO: Write the tests in an OOP way