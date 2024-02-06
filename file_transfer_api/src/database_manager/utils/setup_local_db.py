# Imports
import os
from dotenv import load_dotenv
from file_transfer_api.src.database_manager.utils.database_utils import create_database_if_not_exists, create_tables
from file_transfer_api.src.database_manager.schemas.database_entry import DatabaseEntry

if __name__ == '__main__':
    # Script to create a local database and table if they do not exist

    # Load the variables from .env
    load_dotenv()

    # Create the database if it does not exist
    outcome1 = create_database_if_not_exists(os.getenv("LOCAL_DATABASE_URL"))
    print(f'Database Creation Outcome: {outcome1}')

    # Create the table if it doesn't exist
    outcome2 = create_tables(os.getenv("LOCAL_DATABASE_URL"), DatabaseEntry)
    print(f'Table Creation Outcome: {outcome2}')
