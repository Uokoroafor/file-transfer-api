import os
from dataclasses import dataclass
from typing import Dict, Any

from src.database_manager.schemas.content_enum import ContentEnum

# Load the environment variables

AWS_TABLE_NAME = os.getenv("AWS_DATABASE_TABLE_NAME")


@dataclass
class File:
    """A dataclass for database entries into DynamoDB"""

    file_id: str
    name: str
    content_type: ContentEnum
    size: int
    created_timestamp: str
    last_modified_timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert the database entry to a dictionary.

        Returns:
            Dictionary representation of the database entry.
        """
        return {
            "file_id": self.file_id,
            "name": self.name,
            "content_type": self.content_type,
            "size": self.size,
            "created_timestamp": self.created_timestamp,
            "last_modified_timestamp": self.last_modified_timestamp}

    def to_dynamodb_item(self) -> Dict[str, Any]:
        """Convert the database entry to a dictionary in DynamoDB format.

        Returns:
            Dictionary representation of the database entry in DynamoDB format.
        """
        return {
            "file_id": {"S": self.file_id},
            "name": {"S": self.name},
            "content_type": {"S": str(self.content_type)},
            "size": {"N": str(self.size)},
            "created_timestamp": {"S": self.created_timestamp},
            "last_modified_timestamp": {"S": self.last_modified_timestamp}
        }

    def equal_to_dict(self, other: Dict[str, Any]) -> bool:
        """Check if the database entry is equal to a dictionary. It does not check the timestamps.

        Args:
            other: Dictionary to compare to.

        Returns:
            True if the database entry is equal to the dictionary.
        """
        return (self.file_id == other.get("file_id")
                and self.name == other.get("name")
                and self.content_type == other.get("content_type")
                and self.size == other.get("size"))

    def __repr__(self):
        return (
            f"<FileRecord(file_id={self.file_id}, name={self.name}, content_type={self.content_type.value}, "
            f"size={self.size}, created_timestamp={self.created_timestamp}, "
            f"last_modified_timestamp={self.last_modified_timestamp})>")

    def __eq__(self, other) -> bool:
        if isinstance(other, File):
            return (self.file_id == other.file_id
                    and self.name == other.name
                    and self.content_type == other.content_type
                    and self.size == other.size)
        return False


def get_dynamodb_table_schema() -> Dict[str, Any]:
    """ Output the schema of the table in DynamoDB format. This will be used to create an equivalent table in DynamoDB.

    Returns:
        Dictionary representation of the database entry in DynamoDB format.
    """

    table_name = AWS_TABLE_NAME
    key_schema = [
        {
            'AttributeName': 'file_id',
            'KeyType': 'HASH'
        },
    ]
    attribute_definitions = [
        {
            'AttributeName': 'file_id',
            'AttributeType': 'S'
        }
    ]

    provisioned_throughput = {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }

    return {
        'TableName': table_name,
        'KeySchema': key_schema,
        'AttributeDefinitions': attribute_definitions,
        'ProvisionedThroughput': provisioned_throughput,
    }
