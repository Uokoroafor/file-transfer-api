import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import database_exists, create_database


def create_database_if_not_exists(database_url: str) -> str:
    """Creates database if it does not exist

    Args:
        database_url: URL of the database to be created

    Returns:
        A message indicating whether the database was created or not.
    """
    if not database_exists(database_url):
        create_database(database_url)
        return "Database created"
    else:
        return "Database already exists"


def create_tables(database_url: str, base: declarative_base) -> str:
    """Creates tables in the database.

    Args:
        database_url: URL of the database to create tables in
        base: Base class for the models

    Returns:
        A message indicating whether the tables were created or not.

    Raises:
        psycopg2.OperationalError: If the tables already exist
        Exception: If any other error occurs
    """
    try:
        engine = create_engine(database_url)
        base.metadata.create_all(bind=engine)
        return "Tables created"
    except psycopg2.OperationalError:
        return "Tables already exist"
    except Exception as e:
        return f"Error creating tables: {e}"