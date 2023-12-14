from exceptions.custom_exceptions import DatabaseWriteError, DatabaseReadError
from models.database import SessionLocal
from models.file_model import FileRecord
from typing import List
from abstracts.database_manager_abstract import DatabaseManagerAbstract
from sqlalchemy import text


class LocalDatabaseManager(DatabaseManagerAbstract):
    """Class that manages the local database"""

    def __init__(self):
        """Initialises the local database manager"""
        self.db = SessionLocal()

    def get_file_record(self, file_id: str) -> FileRecord:
        """Get a file from the database.

        Args:
            file_id: Id of the file to get

        Returns:
            File record which contains the file metadata.

        Raises:
            DatabaseReadError: If the file does not exist
        """
        # return self.db.query(FileRecord).filter(FileRecord.file_id == file_id).first()
        record_query = self.db.query(FileRecord).filter(FileRecord.file_id == file_id).first()
        if record_query is None:
            raise DatabaseReadError(f'File record with id {file_id} does not exist on the database.')
        return record_query

    def get_all_file_records(self) -> List[FileRecord]:
        """Get all files from the database.

        Returns:
            List of file records which contain the file metadata.
        """
        return self.db.query(FileRecord).all()

    def create_file_record(self, name: str, file_id: str, content_type: str, size: int) -> FileRecord:
        """Create a file record in the database.

        Args:
            name: Name of the file
            file_id: Id of the file
            content_type: Content type of the file
            size: Size of the file

        Returns:
            File record which contains the file metadata.

        Raises:
            DatabaseWriteError: If the file record creation fails
        """
        result = self.db.execute(text("SELECT CURRENT_TIMESTAMP"))
        created_timestamp = result.scalar()

        # Format the timestamp as a string
        created_timestamp_str = created_timestamp.strftime('%Y-%m-%d %H:%M:%S')

        file_record = FileRecord(
            name=name,
            file_id=file_id,
            content_type=content_type,
            size=size,
            created_timestamp=created_timestamp_str,
            last_modified_timestamp=created_timestamp_str
        )

        try:
            self.db.add(file_record)
            self.db.commit()
            self.db.refresh(file_record)
            return file_record
        except Exception as e:
            self.db.rollback()
            raise DatabaseWriteError(f'Error occurred during file record creation: {e}')

    def update_file_record(self, file_id: str, name: str, content_type: str, size: int) -> FileRecord:
        """Update a file record in the database.

        Args:
            file_id: Id of the file
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
            file_record = self.db.query(FileRecord).filter(FileRecord.file_id == file_id).first()
        except Exception as e:
            raise DatabaseReadError(f'Error occurred during file record read: {e}')

        file_record.name = name
        file_record.content_type = content_type
        file_record.size = size

        result = self.db.execute(text("SELECT CURRENT_TIMESTAMP"))
        last_modified_timestamp = result.scalar()

        # Format the timestamp as a string
        last_modified_timestamp_str = last_modified_timestamp.strftime('%Y-%m-%d %H:%M:%S')
        file_record.last_modified_timestamp = last_modified_timestamp_str

        try:
            self.db.commit()
            self.db.refresh(file_record)
            return file_record
        except Exception as e:
            self.db.rollback()
            raise DatabaseWriteError(f'Error occurred during file record update: {e}')

    def rename_file_record(self, file_id: str, new_file_id: str) -> FileRecord:
        """Rename a file record in the database.

        Args:
            file_id: Id of the file
            new_file_id: New file id

        Returns:
            File record which contains the file metadata.
        """

        try:
            file_record = self.db.query(FileRecord).filter(FileRecord.file_id == file_id).first()
        except DatabaseReadError as e:
            raise e

        if file_record is None:
            raise DatabaseReadError(f'File with id {file_id} does not exist')

        file_record.file_id = new_file_id

        result = self.db.execute(text("SELECT CURRENT_TIMESTAMP"))
        last_modified_timestamp = result.scalar()

        # Format the timestamp as a string
        last_modified_timestamp_str = last_modified_timestamp.strftime('%Y-%m-%d %H:%M:%S')
        file_record.last_modified_timestamp = last_modified_timestamp_str

        try:
            self.db.commit()
            self.db.refresh(file_record)
            return file_record
        except Exception as e:
            self.db.rollback()
            raise DatabaseWriteError(f'Error occurred during file record rename: {e}')

    def delete_file_record(self, file_id: str) -> FileRecord:
        """Delete a file record in the database.

        Args:
            file_id: Id of the file

        Returns:
            File record which contains the file metadata.
        """
        try:
            file_record = self.db.query(FileRecord).filter(FileRecord.file_id == file_id).first()
        except Exception as e:
            raise DatabaseReadError(f'Error occurred during file record read: {e}')

        try:
            self.db.delete(file_record)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise DatabaseWriteError(f'Error occurred during file record delete: {e}')
        return file_record

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

        except Exception as e:
            raise DatabaseReadError(f'Error occurred during file record read: {e}')

        try:
            self.db.query(FileRecord).delete()
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise DatabaseWriteError(f'Error occurred during file record delete: {e}')
        return f"All of the {deleted_count} file records have been deleted."

    def get_count(self) -> int:
        """Get the number of file records in the database.

        Returns:
            The number of file records in the database.
        """
        return self.db.query(FileRecord).count()


if __name__ == "__main__":
    pass
    # # Create a local database manager
    manager = LocalDatabaseManager()
    #
    # # Get all file records
    # file_records = manager.get_all_file_records()
    # print(f'All file records are {file_records}')
    #
    # Create a file record
    file_record = manager.create_file_record(name="test_file", file_id="127", content_type="image/png", size=100)
    print(f'Created file record is {file_record}')
    #
    # # Get a file record
    # file_record = manager.get_file_record("123")
    # print(f'File record is {file_record}')
    #
    # # Update a file record
    # file_record = manager.update_file_record(file_id="123", name="test_file_updated", content_type="image/png",
    #                                          size=100)
    #
    # Get all file records
    file_records = manager.get_all_file_records()
    print(f'All file records are {file_records}')


    # # Delete a file record
    # file_record_deleted = manager.delete_file_record("123")
    # print(f'Deleted file record is {file_record_deleted}')
    #
    # # Print all the attributes of the file record
    # for attr, value in file_record_deleted.__dict__.items():
    #     print(attr, value)
