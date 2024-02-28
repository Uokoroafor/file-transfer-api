import os

import boto3
from src.database_manager.schemas.database_entry import DatabaseEntry

# Initialise the dynamodb resource
dynamodb = boto3.resource('dynamodb')

# Get the table details from the DatabaseEntry class and create the table
dynamodb.create_table(**DatabaseEntry.get_dynamodb_table_schema())

table_name = DatabaseEntry.get_dynamodb_table_schema()["TableName"]

table = dynamodb.Table(table_name)


# Wait until the table exists







