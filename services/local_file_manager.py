from abstracts.file_manager_abstract import FileManagerAbstract
from exceptions.custom_exceptions import FileUploadError, FileDownloadError, FileReplaceError, FileDeleteError, \
    FileRenameError, FileDoesNotExistError
from typing import Tuple
from io import BytesIO
import uuid
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()  # Load the variables from .env

upload_directory = Path(os.getenv("UPLOAD_DIRECTORY", "data/uploads"))
upload_directory.mkdir(parents=True, exist_ok=True)  # Create the upload directory if it doesn't exist

download_directory = Path(os.getenv("DOWNLOAD_DIRECTORY", "data/downloads"))
download_directory.mkdir(parents=True, exist_ok=True)  # Create the download directory if it doesn't exist


class LocalFileManager(FileManagerAbstract):
    """Concrete class for the file manager.

    It contains the methods previously defined in the abstract class to upload, download, replace, rename and delete files.
    """

    def upload_file(self, file: BytesIO) -> Tuple[str, str]:
        """Uploads a file to the server.

        Args:
            file : File to upload

        Returns:
            A tuple containing the generated file id and the result of the file upload.

        Raises:
            FileUploadError: If the file upload fails
        """
        # generate a unique id for the file
        try:
            file_id = str(uuid.uuid4())
            file_location = upload_directory / file_id
            # Save the file to the upload directory
            with open(file_location, "wb") as f:
                f.write(file.read())
            return file_id, "File uploaded"
        except Exception as e:
            raise FileUploadError(f"Error occurred during file upload: {e}")

    def download_file(self, file_id: str) -> str:
        """Downloads a file from the upload directory to the download directory.

        Args:
            file_id : Id of the file to download

        Returns:
            The result of the file download.

        Raises:
            FileDoesNotExistError: If the file does not exist
            FileDownloadError: If the file download fails

        """
        file_location = upload_directory / file_id
        if not file_location.is_file():
            raise FileDoesNotExistError(f"File does not exist at {file_location}")

        try:
            with open(download_directory / file_id, "wb") as f:
                f.write(file_location.read_bytes())
            return "File downloaded"
        except Exception as e:
            raise FileDownloadError(f"Error occurred during file download: {e}")

    def replace_file(self, file_id: str, file: BytesIO) -> str:
        """Replaces a file on the server.

        Args:
            file_id : Id of the file to replace
            file : File to update

        Returns:
            The result of the file update.

        Raises:
            FileReplaceError: If the file update fails
        """
        file_location = upload_directory / file_id
        # Check if the file exists
        if not file_location.is_file():
            raise FileDoesNotExistError(f"File does not exist at {file_location}")

        try:

            with open(file_location, "wb") as f:
                f.write(file.read())
            return "File replaced"
        except Exception as e:
            raise FileReplaceError(f"Error occurred during file replace: {e}")

    def delete_file(self, file_id: str) -> str:
        """Deletes a file from the server.

        Args:
            file_id : Id of the file to delete

        Returns:
            The result of the file deletion.

        Raises:
            FileDoesNotExistError: If the file does not exist
            FileDeleteError: If the file deletion fails
        """
        file_location = upload_directory / file_id
        if not file_location.is_file():
            raise FileDoesNotExistError(f"File does not exist at {file_location}")

        try:
            file_location.unlink()
            return "File deleted"

        except Exception as e:
            raise FileDeleteError(f"Error occurred during file delete: {e}")

    def rename_file(self, old_file_id: str, new_file_id: str) -> str:
        """Renames a file on the server.

        Args:
            old_file_id : Old Id of the file
            new_file_id : New Id of the file

        Returns:
            The result of the file rename.

        Raises:
            FileRenameError: If the file rename fails
        """
        old_file_location = upload_directory / old_file_id
        new_file_location = upload_directory / new_file_id

        if not old_file_location.is_file():
            raise FileDoesNotExistError(f"File does not exist at {old_file_location}")
        try:
            old_file_location.rename(new_file_location)
            return "File renamed"
        except Exception as e:
            raise FileRenameError(f"Error occurred during file rename: {e}")
