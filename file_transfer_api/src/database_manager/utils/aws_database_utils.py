from typing import Dict, Any

from src.database_manager.schemas.database_entry import DatabaseEntry
from botocore.exceptions import ClientError
from boto3.resources.base import ServiceResource
from src.database_manager.schemas.content_enum import ContentEnum


def get_database_entry_from_record_query(record_query: Dict[str, Any]) -> DatabaseEntry:
    """Get a DatabaseEntry object from a record query.

    Args:
        record_query: Query result from the database

    Returns:
        DatabaseEntry object containing the file metadata
    """

    # Args for this function will be dicts of two variants:
    # 1. The result of a query from the database which will contain an 'Item' key
    # 2. A dict containing the file metadata which will not contain an 'Item' key
    # (due to multiple records being returned)

    item = record_query.get('Item')

    # If there is no 'Item' key, then the record_query is the item
    if item is None:
        item = record_query

    return DatabaseEntry(
        file_id=item['file_id'],
        name=item['name'],
        content_type=ContentEnum.from_str(item['content_type']),
        size=item['size'],
        created_timestamp=item['created_timestamp'],
        last_modified_timestamp=item['last_modified_timestamp']
    )


def create_dynamodb_table_if_not_exists(dynamodb: ServiceResource, table_schema: Dict[str, Any]) -> None:
    """Create a DynamoDB table if it does not exist.

    Args:
        dynamodb: DynamoDB resource
        table_schema: Schema of the table in DynamoDB format

    Returns:
        None

    Raises:
        ClientError: If the table creation fails for any reason other than the table already existing
    """
    try:
        dynamodb.create_table(**table_schema)
    except ClientError as e:
        if e.response['Error']['Code'] != 'ResourceInUseException':
            raise e
        else:
            pass
