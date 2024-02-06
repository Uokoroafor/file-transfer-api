import datetime
from typing import List
from file_transfer_api.src.database_manager.abstract_database_manager import AbstractDatabaseManager
from file_transfer_api.src.database_manager.schemas.content_enum import ContentEnum
from file_transfer_api.src.database_manager.schemas.database_entry import DatabaseEntry
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from file_transfer_api.src.database_manager.database_connection.local_database import SessionLocal
from file_transfer_api.src.exceptions.database_exceptions import DatabaseWriteError, DatabaseReadError, DatabaseConnectionError


class LocalDatabaseManager(AbstractDatabaseManager):
    """Class that manages the local database. """

    def __init__(self):
        """Initialises the local database manager"""
        self.db = SessionLocal()

    def check_database_connection(self) -> bool:
        """Check if the database is connected.

        Returns:
            True if the database is connected.

        Raises:
            DatabaseConnectionError: If the database is not connected.
        """
        try:
            self.db.execute(text("SELECT 1"))
        except SQLAlchemyError as e:
            raise DatabaseConnectionError(f'Error occurred while checking database connection: {e}')
        return True

    def get_file_record(self, file_id: str) -> DatabaseEntry:
        """Get a file from the database.

        Args:
            file_id: ID of the file to get

        Returns:
            File record which contains the file metadata.

        Raises:
            DatabaseReadError: If the file does not exist
        """
        # return self.db.query(FileRecord).filter(FileRecord.file_id == file_id).first()
        try:
            record_query = self.db.query(DatabaseEntry).filter(DatabaseEntry.file_id == file_id).first()
            # raise error if the file does not exist (i.e. the query returns None)
            if record_query is None:
                raise DatabaseReadError(f'File with id {file_id} does not exist')
        except SQLAlchemyError as e:
            raise DatabaseReadError(f'Error occurred while reading file record: {e}')
        return record_query

    def get_all_file_records(self) -> List[DatabaseEntry]:
        """Get all files from the database.

        Returns:
            List of file records which contain the file metadata.
        """
        return self.db.query(DatabaseEntry).all()

    def create_file_record(self, name: str, file_id: str, content_type: ContentEnum, size: int) -> DatabaseEntry:
        """Create a file record in the database.

        Args:
            name: Name of the file
            file_id: ID of the file
            content_type: Content type of the file
            size: Size of the file

        Returns:
            File record which contains the file metadata.

        Raises:
            DatabaseWriteError: If the file record creation fails
        """

        created_timestamp_str = datetime.datetime.now()

        file_record = DatabaseEntry(
            name=name,
            file_id=file_id,
            content_type=content_type,
            size=size,
            created_timestamp=created_timestamp_str,
            last_modified_timestamp=created_timestamp_str
        )

        # Check if the file record already exists
        if self.db.query(DatabaseEntry).filter(DatabaseEntry.file_id == file_id).first() is not None:
            raise DatabaseWriteError(f'File with id {file_id} already exists')

        try:
            self.db.add(file_record)
            self.db.commit()
            self.db.refresh(file_record)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseWriteError(f'Error occurred while creating file record: {e}')

        return file_record

    def update_file_record(self, file_id: str, name: str, content_type: ContentEnum, size: int) -> str:
        """Update a file record in the database.

        Args:
            file_id: ID of the file
            name: Name of the file
            content_type: Content type of the file
            size: Size of the file

        Returns:
            File record which contains the file metadata.

        Raises:
            DatabaseWriteError: If the file record update fails
            DatabaseReadError: If the file record does not exist
        """

        try:
            file_record = self.db.query(DatabaseEntry).filter(DatabaseEntry.file_id == file_id).first()
            # raise error if the file does not exist (i.e. the query returns None)
            if file_record is None:
                raise DatabaseReadError(f'File with id {file_id} does not exist')
        except SQLAlchemyError as e:
            raise DatabaseReadError(f'Error occurred while reading file record: {e}')

        file_record.name = name
        file_record.content_type = content_type
        file_record.size = size

        file_record.last_modified_timestamp = datetime.datetime.now()

        try:
            self.db.commit()
            self.db.refresh(file_record)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseWriteError(f'Error occurred while updating file record: {e}')
        return "File record updated successfully"

    def rename_file_record(self, file_id: str, new_file_name: str) -> str:
        """Rename a file record in the database.

        Args:
            file_id: ID of the file
            new_file_name: New name of the file

        Returns:
            File record which contains the file metadata.
        """

        file_record = self.get_file_record(file_id)

        file_record.name = new_file_name

        last_modified_timestamp = datetime.datetime.now()
        file_record.last_modified_timestamp = last_modified_timestamp

        try:
            self.db.commit()
            self.db.refresh(file_record)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseWriteError(f'Error occurred while renaming file record: {e}')
        return "File record renamed successfully"

    def delete_file_record(self, file_id: str) -> str:
        """Delete a file record in the database.

        Args:
            file_id: ID of the file

        Returns:
            File record which contains the file metadata.
        """

        file_record = self.db.query(DatabaseEntry).filter(DatabaseEntry.file_id == file_id).first()
        # raise error if the file does not exist (i.e. the query returns None)
        if file_record is None:
            raise DatabaseReadError(f'File with id {file_id} does not exist')

        try:
            self.db.delete(file_record)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseWriteError(f'Error occurred while deleting file record: {e}')
        return "File record deleted successfully"

    def delete_all_file_records(self) -> str:
        """Delete all file records in the database.

        Returns:
            String confirming how many file records have been deleted.

        Raises:
            DatabaseWriteError: If the file record deletion fails
            DatabaseReadError: If the file record does not exist
        """
        try:
            deleted_count = self.get_count()

            self.db.query(DatabaseEntry).delete()
            self.db.commit()

        except SQLAlchemyError as e:
            # Roll back the transaction in case of an error
            self.db.rollback()
            raise DatabaseWriteError(f'Error occurred while deleting all file records: {e}')

        return f"All of the {deleted_count} file records have been deleted."

    def get_count(self) -> int:
        """Get the number of file records in the database.

        Returns:
            The number of file records in the database.
        """
        return self.db.query(DatabaseEntry).count()


if __name__ == "__main__":
    pass
    # # Create a local database manager
    manager = LocalDatabaseManager()

    # Check that the database is connected
    manager.check_database_connection()

    # Get all file records
    file_records = manager.get_all_file_records()
    print(f'All file records are {file_records}')

    # Get a file record
    file_record_ = manager.get_file_record("120")
    print(f'File record is {file_record_}')
