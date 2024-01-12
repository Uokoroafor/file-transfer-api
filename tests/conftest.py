import tempfile
import warnings
from datetime import datetime
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import SAWarning
from sqlalchemy.orm import sessionmaker

from database_manager.database_connection.local_database import Base
from database_manager.local_database_manager import LocalDatabaseManager
from database_manager.schemas.content_enum import ContentEnum
from database_manager.schemas.database_entry import DatabaseEntry
from file_manager.local_file_manager import LocalFileManager


def pytest_configure(config):
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=SAWarning)


DATA_DIR = Path("tests/test_fixtures/data")
UPLOAD_DIR = DATA_DIR / "uploads"
DOWNLOAD_DIR = DATA_DIR / "downloads"


@pytest.fixture(scope="session")
def file_system():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    yield

    # Teardown: remove files and directories
    for directory in [UPLOAD_DIR, DOWNLOAD_DIR, DATA_DIR]:
        for file in directory.iterdir():
            file.unlink()
        directory.rmdir()


@pytest.fixture(scope="session")
def file_manager():
    yield LocalFileManager()


@pytest.fixture
def temp_file(file_system):
    with tempfile.NamedTemporaryFile(dir=DATA_DIR, delete=False) as f:
        f.write(b"test data")
        f.flush()
    yield f.name


@pytest.fixture
def temp_upload_file(file_system):
    # Write a temporary file to the upload directory and yield the file location
    with tempfile.NamedTemporaryFile(dir=UPLOAD_DIR, delete=False) as f:
        f.write(b"test data")
        f.flush()
    yield f.name


@pytest.fixture
def temp_rename_file(file_system):
    # Write a temporary file to the data directory and yield the file location
    with tempfile.NamedTemporaryFile(dir=UPLOAD_DIR, delete=False) as f:
        f.write(b"test data")
        f.flush()
    yield f.name


FIXED_TIMESTAMP = datetime(2021, 1, 1, 0, 0, 0, 0)
TEST_RECORD_1 = {"name": "test_name_1", "file_id": "test_id_1", "content_type": ContentEnum.TEXT, "size": 1}
RENAMED_TEST_RECORD_1 = TEST_RECORD_1.copy()
TEST_RECORD_2 = {"name": "test_name_2", "file_id": "test_id_2", "content_type": ContentEnum.TEXT, "size": 2}
NON_EXISTENT_TEST_RECORD = TEST_RECORD_1.copy()
RENAMED_TEST_RECORD_1["name"] = "test_name_2"
NON_EXISTENT_TEST_RECORD["file_id"] = "non_existent_id"


@pytest.fixture(scope="session")
def test_engine():
    return create_engine('sqlite:///:memory:')


@pytest.fixture(scope="session")
def test_db_session(test_engine):
    Base.metadata.create_all(test_engine)  # Create tables
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def test_db_manager(test_db_session):
    local_database_manager = LocalDatabaseManager()
    local_database_manager.db = test_db_session

    yield local_database_manager

    # Tear down
    test_db_session.query(DatabaseEntry).delete()
    test_db_session.commit()


def create_database_entry(session, value_dict) -> DatabaseEntry:
    """Create a database entry from a dictionary of values"""
    file_record = DatabaseEntry(**value_dict, created_timestamp=FIXED_TIMESTAMP,
                                last_modified_timestamp=FIXED_TIMESTAMP)
    session.add(file_record)
    session.commit()
    return file_record


@pytest.fixture(scope="function")
def test_database_entry(test_db_session):
    file_record = create_database_entry(test_db_session, TEST_RECORD_1)
    yield file_record

    # Tear down
    test_db_session.query(DatabaseEntry).delete()
    test_db_session.commit()


@pytest.fixture(scope="function")
def test_database_entry_2(test_db_session):
    file_record = create_database_entry(test_db_session, TEST_RECORD_2)
    yield file_record

    # Tear down
    test_db_session.query(DatabaseEntry).delete()
    test_db_session.commit()
