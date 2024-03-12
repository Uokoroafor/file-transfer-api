import os

import boto3
from src.database_manager.schemas.dynamodb_entry import get_dynamodb_table_schema


# Initialise the dynamodb resource
# Use the default AWS credentials if the local environment is not set up
if "AWS_ACCESS_KEY_ID" not in os.environ:
    dynamodb_client = boto3.client('dynamodb')
else:
    dynamodb_client = boto3.client('dynamodb',
                                   aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                                   aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                                   region_name=os.environ['AWS_REGION'])

# # Get the table details from the DatabaseEntry class and create the table if it does not exist
# create_dynamodb_table_if_not_exists(dynamodb_client, get_dynamodb_table_schema())

table_name = get_dynamodb_table_schema()["TableName"]

