from typing import IO
import shutil

from src.file_manager.abstract_file_manager import AbstractFileManager
from uuid import uuid4
from pathlib import Path
from dotenv import load_dotenv
import os
from src.exceptions.file_exceptions import (FileDownloadError, FileUploadError, FileDeleteError, FileDoesNotExistError,
                                        FileUpdateError)

load_dotenv()
upload_path = Path(os.getenv("UPLOAD_DIRECTORY", default="data/uploads"))
download_path = Path(os.getenv("DOWNLOAD_DIRECTORY", default="data/downloads"))


class LocalFileManager(AbstractFileManager):
    """Class for the local file manager."""

    def upload_file(self, file: IO) -> Path:
        """Upload a file to the local file system.

        Args:
            file: File to upload.

        Returns:
            Path to the uploaded file.

        Raises:
            FileUploadError: If an error occurs while uploading the file.
        """

        # generate a file id
        file_id = str(uuid4())
        file_location = upload_path / file_id

        try:
            # save the file
            with open(file_location, "wb") as f:
                f.write(file.read())

            # return the file id and the file path
        except IOError as e:
            raise FileUploadError(f'Error occurred while uploading file: {e}')
        return file_location

    def download_file(self, file_id: str) -> Path:
        """Download a file from the local file system.

        Args:
            file_id: ID of the file to download.

        Returns:
            Path to the downloaded file.

        Raises:
            FileDownloadError: If an error occurs while downloading the file.
            FileDoesNotExistError: If the file does not exist.
        """

        # Copy the file to the download path and return the path
        upload_file_path = upload_path / file_id
        download_file_path = download_path / file_id

        try:
            shutil.copy(upload_file_path, download_file_path)
        except FileNotFoundError:
            raise FileDoesNotExistError(f'File with id {file_id} does not exist')
        except IOError as e:
            raise FileDownloadError(f'Error occurred while downloading file: {e}')
        return download_file_path

    def rename_file(self, file_id: str, new_file_id: str):
        """Rename a file in the local file system.

        Args:

            file_id: ID of the file to rename.
            new_file_id: New id of the file.

        Raises:
            FileDoesNotExistError: If the file does not exist.
            FileUpdateError: If an error occurs while renaming the file.
        """
        old_file_location = upload_path / file_id
        new_file_location = upload_path / new_file_id

        try:
            old_file_location.rename(new_file_location)
        except FileNotFoundError:
            raise FileDoesNotExistError(f'File with id {file_id} does not exist')
        except IOError as e:
            raise FileUpdateError(f'Error occurred while renaming file: {e}')

    def delete_file(self, file_id: str):
        """Delete a file from the local file system.

        Args:
            file_id: ID of the file to delete.

        Raises:
            FileDoesNotExistError: If the file does not exist.
            FileDeleteError: If an error occurs while deleting the file.
        """
        file_location = upload_path / file_id
        try:
            file_location.unlink()
        except FileNotFoundError:
            raise FileDoesNotExistError(f'File with id {file_id} does not exist')
        except OSError as e:
            raise FileDeleteError(f'Error occurred while deleting file: {e}')
