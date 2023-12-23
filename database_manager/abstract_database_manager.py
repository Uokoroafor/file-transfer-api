from abc import ABC, abstractmethod
from database_manager.schemas.database_entry import DatabaseEntry


class AbstractDatabaseManager(ABC):
    """Abstract class for the database manager.

    It contains methods that will be defined elsewhere in concrete classes
    """

    @abstractmethod
    def create_file_record(self, name: str, file_id: str, content_type: str, size: int) -> str:
        """Abstract method to create a file record.

        Args:
            name: Name of the file
            file_id: Id of the file
            content_type: Content type of the file
            size: Size of the file

        Returns:
            A message confirming the file record creation.
        """
        pass

    @abstractmethod
    def get_file_record(self, file_id: str) -> DatabaseEntry:
        """Abstract method to get a file record.

        Args:
            file_id : Id of the file record to get

        Returns:
            The result of the file record retrieval as defined by the concrete class.
        """
        pass

    @abstractmethod
    def rename_file_record(self, file_id: str, new_file_id: str) -> str:
        """Abstract method to change a file record's file id.

        Args:
            file_id: Id of the file record to change
            new_file_id: New file id

        Returns:
            File record which contains the file metadata.
        """
        pass

    @abstractmethod
    def delete_file_record(self, file_id: str) -> str:
        """Abstract method to delete a file record.

        Args:
            file_id: Id of the file record to delete

        Returns:
            A message confirming the file record deletion.
        """
        pass
