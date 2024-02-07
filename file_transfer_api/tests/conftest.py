import tempfile
from datetime import datetime
from pathlib import Path

import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from src.database_manager.database_connection.local_database import Base
from src.database_manager.local_database_manager import LocalDatabaseManager
from src.database_manager.schemas.content_enum import ContentEnum
from src.database_manager.schemas.database_entry import DatabaseEntry
from src.file_manager.local_file_manager import LocalFileManager


@pytest.fixture(scope="function")
def file_system():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        data_dir = temp_dir_path / "data"
        upload_dir = data_dir / "uploads"
        download_dir = data_dir / "downloads"

        # Create the directories
        data_dir.mkdir(parents=True, exist_ok=True)
        upload_dir.mkdir(parents=True, exist_ok=True)
        download_dir.mkdir(parents=True, exist_ok=True)

        # Yield the directory paths for use in tests
        yield data_dir, upload_dir, download_dir


@pytest.fixture(scope="function")
def file_manager():
    return LocalFileManager()


@pytest.fixture
def temp_file(file_system):
    data_dir, upload_dir, download_dir = file_system
    with tempfile.NamedTemporaryFile(dir=data_dir, delete=False) as f:
        f.write(b"test data")
    yield f.name


@pytest.fixture
def temp_upload_file(file_system):
    # Write a temporary file to the upload directory and yield the file location
    data_dir, upload_dir, download_dir = file_system
    with tempfile.NamedTemporaryFile(dir=upload_dir, delete=False) as f:
        f.write(b"test data")
    yield f.name


@pytest.fixture
def temp_rename_file(file_system):
    # Write a temporary file to the data directory and yield the file location
    data_dir, upload_dir, download_dir = file_system
    with tempfile.NamedTemporaryFile(dir=upload_dir, delete=False) as f:
        f.write(b"test data")
    yield f.name


FIXED_TIMESTAMP = datetime(2021, 1, 1, 0, 0, 0, 0)
TEST_RECORD_1 = {"name": "test_name_1", "file_id": "test_id_1", "content_type": ContentEnum.TEXT, "size": 1}
TEST_RECORD_2 = {"name": "test_name_2", "file_id": "test_id_2", "content_type": ContentEnum.TEXT, "size": 2}

# Create renamed and non-existent records using dictionary comprehension
RENAMED_TEST_RECORD_1 = {**TEST_RECORD_1, "name": "test_name_2"}
NON_EXISTENT_TEST_RECORD = {**TEST_RECORD_1, "file_id": "non_existent_id"}


# Convert the records to pytest fixtures
@pytest.fixture(scope="session")
def test_record_1():
    return TEST_RECORD_1


@pytest.fixture(scope="session")
def test_record_2():
    return TEST_RECORD_2


@pytest.fixture(scope="session")
def renamed_test_record_1():
    return RENAMED_TEST_RECORD_1


@pytest.fixture(scope="session")
def non_existent_test_record():
    return NON_EXISTENT_TEST_RECORD


@pytest.fixture(scope="function")
def test_engine():
    engine = create_engine('sqlite:///:memory:', connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)  # Create tables
    return engine


@pytest.fixture(scope="function")
def test_db_session(test_engine):
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
