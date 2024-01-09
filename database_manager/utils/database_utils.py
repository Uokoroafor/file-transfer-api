from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.exc import SQLAlchemyError


def create_database_if_not_exists(database_url: str) -> bool:
    """Creates database if it does not exist

    Args:
        database_url: URL of the database to be created

    Returns:
        True if the database was created, False if it already exists
    """
    if not database_exists(database_url):
        create_database(database_url)
        return True
    else:
        return False


def create_tables(database_url: str, base: declarative_base) -> bool:
    """Creates tables in the database.

    Args:
        database_url: URL of the database to create tables in
        base: Base class for the models

    Returns:
        True if the tables were created or already exist, False if an error occurred

    Raises:
        psycopg2.OperationalError: If the tables already exist
        Exception: If any other error occurs
    """
    try:
        engine = create_engine(database_url)
        base.metadata.create_all(bind=engine, checkfirst=True)
        return True
    except SQLAlchemyError:
        return False
    except Exception as e:
        raise e
