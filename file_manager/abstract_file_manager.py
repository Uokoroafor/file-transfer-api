from abc import ABC, abstractmethod
from pathlib import Path
from typing import IO


class AbstractFileManager(ABC):
    """Abstract class for the file manager.

    It contains methods that will be defined elsewhere in concrete classes
    """

    @abstractmethod
    def upload_file(self, file: IO) -> Path:
        """Abstract method to upload a file.

        Args:
            file: File to upload

        Returns:
            Path of the file uploaded.
        """
        pass

    @abstractmethod
    def download_file(self, file_id: str) -> Path:
        """Abstract method to download a file.

        Args:
            file_id: Id of the file to download

        Returns:
            Path of the file downloaded.
        """
        pass

    @abstractmethod
    def rename_file(self, file_id, new_file_id):
        """Abstract method to rename a file.

        Args:
            file_id: Id of the file to rename
            new_file_id: New id of the file

        Returns:
            Path of the file renamed.
        """
        pass

    @abstractmethod
    def delete_file(self, file_id):
        """Abstract method to delete a file.

        Args:
            file_id: Id of the file to delete

        Returns:
            Path of the file deleted.
        """
        pass
