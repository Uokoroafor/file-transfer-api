import datetime
from typing import List
from src.database_manager.abstract_database_manager import AbstractDatabaseManager
from src.database_manager.schemas.content_enum import ContentEnum
from src.database_manager.schemas.dynamodb_entry import File
from src.database_manager.database_connection.aws_database import table_name, dynamodb_client
from botocore.exceptions import ClientError
from src.exceptions.database_exceptions import DatabaseWriteError, DatabaseReadError, DatabaseConnectionError
from src.database_manager.utils.aws_database_utils import get_database_entry_from_record_query


class AWSDatabaseManager(AbstractDatabaseManager):
    """Class that manages the AWS database in DynamoDB. """

    def __init__(self):
        """Initialises the AWS database manager"""
        self.client = dynamodb_client
        self.table_name = table_name

    def check_database_connection(self) -> None:
        """Check if the database is connected.

        Raises:
            DatabaseConnectionError: If the database is not connected.
        """
        try:
            self.client.describe_table(TableName=self.table_name)
        except ClientError as e:
            raise DatabaseConnectionError(f'Error occurred while checking database connection: {e}')

    def create_file_record(self, name: str, file_id: str, content_type: ContentEnum, size: int):
        """Create a file record in the database.

        Args:
            name: Name of the file
            file_id: Id of the file
            content_type: Content type of the file
            size: Size of the file

        Returns:
            None

        Raises:
            DatabaseWriteError: If the file record creation fails.
        """
        created_timestamp = str(datetime.datetime.utcnow())
        last_modified_timestamp = created_timestamp
        entry = File(file_id, name, content_type, size, created_timestamp, last_modified_timestamp)

        try:
            self.client.put_item(
                TableName=self.table_name,
                Item=entry.to_dynamodb_item()
            )

        except ClientError as e:
            raise DatabaseWriteError(f'Error occurred while writing file record: {e}')

    def get_file_record(self, file_id: str) -> File:
        """Get a file record from the database.

        Args:
            file_id: Id of the file record to get

        Returns:
            File record which contains the file metadata.

        Raises:
            DatabaseReadError: If the file does not exist.
        """
        try:
            record_query = self.client.get_item(
                TableName=self.table_name,
                Key={'file_id': {'S': file_id}}
            )
            if 'Item' not in record_query:
                raise DatabaseReadError(f'File with id {file_id} does not exist')
        except ClientError as e:
            raise DatabaseReadError(f'Error occurred while reading file record: {e}')
        # Convert the record to a DatabaseEntry object
        return get_database_entry_from_record_query(record_query)

    def rename_file_record(self, file_id: str, new_name: str) -> str:
        """Update the 'name' attribute of a file record in the database.

        Args:
            file_id: Id of the file record to update
            new_name: New name of the file record

        Returns:
            A message confirming the file record update.

        Raises:
            DatabaseWriteError: If the file record update fails.
            DatabaseReadError: If the file record does not exist.
        """

        file_record = self.get_file_record(file_id)

        file_record.name = new_name

        # Update the last modified timestamp
        last_modified_timestamp = str(datetime.datetime.utcnow())
        file_record.last_modified_timestamp = last_modified_timestamp
        new_entry = file_record.to_dynamodb_item()

        try:
            self.client.put_item(
                TableName=self.table_name,
                Item=new_entry

            )
        except ClientError as e:
            raise DatabaseWriteError(f'Error occurred while updating file record: {e}')
        return "File record updated successfully"

    def delete_file_record(self, file_id: str) -> str:
        """Delete a file record from the database.

        Args:
            file_id: Id of the file record to delete

        Returns:
            A message confirming the file record deletion.

        Raises:
            DatabaseWriteError: If the file record deletion fails.
        """

        try:
            self.client.delete_item(
                TableName=self.table_name,
                Key={'file_id': {'S': file_id}}
            )
        except ClientError as e:
            raise DatabaseWriteError(f'Error occurred while deleting file record: {e}')
        return "File record deleted successfully"

    def get_all_file_records(self) -> List[File]:
        """Get all file records from the database.

        Returns:
            A list of all file records in the database.

        Raises:
            DatabaseReadError: If an error occurs while reading the file records.
        """
        try:
            records_query = self.client.scan(
                TableName=self.table_name
            )
        except ClientError as e:
            raise DatabaseReadError(f'Error occurred while reading file records: {e}')

        # Return an empty list if there are no records
        if not records_query['Items']:
            return []
        return [get_database_entry_from_record_query(record) for record in records_query['Items']]
