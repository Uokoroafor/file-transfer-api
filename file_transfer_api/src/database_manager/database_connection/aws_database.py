import os

import boto3
from src.database_manager.schemas.database_entry import get_dynamodb_table_schema
from src.database_manager.utils.aws_database_utils import create_dynamodb_table_if_not_exists

# Initialise the dynamodb resource
# Use the default AWS credentials if the local environment is not set up
if "AWS_ACCESS_KEY_ID" not in os.environ:
    dynamodb_resource = boto3.resource('dynamodb')
else:
    dynamodb_resource = boto3.resource('dynamodb',
                                       aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                                       aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                                       region_name=os.getenv("AWS_REGION"))

# Get the table details from the DatabaseEntry class and create the table if it does not exist
create_dynamodb_table_if_not_exists(dynamodb_resource, get_dynamodb_table_schema())

table_name = get_dynamodb_table_schema()["TableName"]

table = dynamodb_resource.Table(table_name)
