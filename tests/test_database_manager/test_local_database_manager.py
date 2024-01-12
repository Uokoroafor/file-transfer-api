from datetime import datetime
from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from database_manager.schemas.database_entry import DatabaseEntry
from exceptions.database_exceptions import DatabaseReadError, DatabaseWriteError
from database_manager.local_database_manager import LocalDatabaseManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_manager.database_connection.local_database import Base
from database_manager.schemas.content_enum import ContentEnum

FIXED_TIMESTAMP = datetime(2021, 1, 1, 0, 0, 0, 0)
TEST_RECORD_1 = {"name": "test_name_1", "file_id": "test_id_1", "content_type": ContentEnum.TEXT, "size": 1}
RENAMED_TEST_RECORD_1 = TEST_RECORD_1.copy()
RENAMED_TEST_RECORD_1["name"] = "test_name_2"
TEST_RECORD_2 = {"name": "test_name_2", "file_id": "test_id_2", "content_type": ContentEnum.TEXT, "size": 2}
NON_EXISTENT_TEST_RECORD = TEST_RECORD_1.copy()
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


class TestLocalDatabaseManager:
    @pytest.fixture(autouse=True)
    def setup(self, test_db_manager, test_db_session):
        self.db_manager = test_db_manager
        self.db_session = test_db_session

    def test_get_file_record_returns_file_record(self, test_database_entry):
        # Return the file record
        returned_file_record = self.db_manager.get_file_record(TEST_RECORD_1["file_id"])

        # Assert
        assert returned_file_record == test_database_entry

    def test_get_file_record_for_non_existent_file_id_raises_database_read_error(self, test_database_entry):
        # Return a file record that does not exist
        with pytest.raises(DatabaseReadError):
            self.db_manager.get_file_record(NON_EXISTENT_TEST_RECORD["file_id"])

    def test_get_all_file_records_returns_all_file_records(self, test_database_entry, test_database_entry_2):
        # Act
        returned_file_records = self.db_manager.get_all_file_records()

        # Assert
        assert returned_file_records == [test_database_entry, test_database_entry_2]

    def test_create_file_record_returns_created_file_record(self):
        # Act
        self.db_manager.create_file_record(**TEST_RECORD_1)

        # get the file record from the database
        returned_file_record = self.db_session.query(DatabaseEntry).filter(DatabaseEntry.file_id == TEST_RECORD_1["file_id"]).first()

        # Assert
        assert returned_file_record.equal_to_dict(TEST_RECORD_1)

    def test_create_file_record_with_existing_file_id_raises_database_write_error(self, test_database_entry):
        with pytest.raises(DatabaseWriteError):
            self.db_manager.create_file_record(**TEST_RECORD_1)

    def test_rename_file_record_returns_renamed_file_record(self, test_database_entry):
        # Act
        self.db_manager.rename_file_record(TEST_RECORD_1["file_id"], RENAMED_TEST_RECORD_1["name"])

        # get the file record from the database
        returned_file_record = self.db_session.query(DatabaseEntry).filter(DatabaseEntry.file_id == "test_id_1").first()

        # Assert
        assert returned_file_record.name == RENAMED_TEST_RECORD_1["name"]
        assert returned_file_record.last_modified_timestamp > returned_file_record.created_timestamp

    def test_rename_file_record_with_non_existent_file_id_raises_database_write_error(self, test_database_entry):
        # Act and assert
        with pytest.raises(DatabaseReadError):
            self.db_manager.rename_file_record(NON_EXISTENT_TEST_RECORD["file_id"], RENAMED_TEST_RECORD_1["name"])

    def test_delete_file_record_deletes_file_record(self, test_database_entry):
        self.db_manager.delete_file_record(TEST_RECORD_1["file_id"])
        assert self.db_session.query(DatabaseEntry).filter(DatabaseEntry.file_id == TEST_RECORD_1["file_id"]).first() is None

    def test_delete_file_record_with_non_existent_file_id_raises_database_read_error(self, test_database_entry):
        with pytest.raises(DatabaseReadError):
            self.db_manager.delete_file_record(NON_EXISTENT_TEST_RECORD["file_id"])

    def test_error_while_deleting_file_record_raises_database_write_error(self, test_database_entry):
        with patch("sqlalchemy.orm.session.Session.delete", side_effect=SQLAlchemyError):
            with pytest.raises(DatabaseWriteError):
                self.db_manager.delete_file_record(TEST_RECORD_1["file_id"])

    def test_get_count_returns_count_of_file_records(self, test_database_entry, test_database_entry_2):
        count = self.db_manager.get_count()
        assert count == 2

    def test_update_file_record_updates_file_record(self, test_database_entry):
        self.db_manager.update_file_record(**RENAMED_TEST_RECORD_1)

        # get the file record from the database
        returned_file_record = self.db_session.query(DatabaseEntry).filter(DatabaseEntry.file_id == RENAMED_TEST_RECORD_1["file_id"]).first()

        assert returned_file_record.file_id == RENAMED_TEST_RECORD_1["file_id"]
        assert returned_file_record.last_modified_timestamp > returned_file_record.created_timestamp

    def test_update_file_record_with_non_existent_file_id_raises_database_write_error(self, test_database_entry):
        # Act and assert
        with pytest.raises(DatabaseReadError):
            # Update test_file_metadata with a non-existent file id
            self.db_manager.update_file_record(**NON_EXISTENT_TEST_RECORD)
