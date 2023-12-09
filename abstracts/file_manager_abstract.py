# This contains the abstract class for the file manager. It contains methods that will be defined elsewhere
# in concrete classes

from abc import ABC, abstractmethod
from typing import Any, Tuple
from io import BytesIO


class FileManagerAbstract(ABC):
    """Abstract class for the file manager. It contains methods that will be defined elsewhere in concrete classes"""

    @abstractmethod
    def upload_file(self, file: BytesIO) -> Tuple[str, Any]:
        """Abstract method to upload a file.

        Args:
            file : File to upload

        Returns:
            A tuple containing the generated file id and the result of the file upload as defined by the concrete class.
        """
        pass

    @abstractmethod
    def download_file(self, file_id: str) -> Any:
        """Abstract method to download a file.

        Args:
            file_id : Id of the file to download

        Returns:
            The result of the file download as defined by the concrete class.
        """
        pass

    @abstractmethod
    def replace_file(self, file_id: str, file: BytesIO) -> Any:
        """Abstract method to replace a file.

        Args:
            file_id : Id of the file to replace
            file : File to update

        Returns:
            The result of the file update as defined by the concrete class.
        """
        pass

    @abstractmethod
    def delete_file(self, file_id: str) -> Any:
        """Abstract method to delete a file.

        Args:
            file_id : Id of the file to delete

        Returns:
            The result of the file deletion as defined by the concrete class.
        """
        pass

    @abstractmethod
    def rename_file(self, old_file_id: str, new_file_id: str) -> Any:
        """Abstract method to change the id of a file (rename).

        Args:
            old_file_id : Old Id of the file
            new_file_id : New Id of the file

        Returns:
            The result of the file rename as defined by the concrete class.
        """
        pass
