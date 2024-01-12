from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from database_manager.schemas.database_entry import DatabaseEntry
from exceptions.database_exceptions import DatabaseReadError, DatabaseWriteError

from tests.conftest import TEST_RECORD_1, RENAMED_TEST_RECORD_1, NON_EXISTENT_TEST_RECORD, test_db_session, \
    test_db_manager, test_database_entry, test_database_entry_2


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
        returned_file_record = self.db_session.query(DatabaseEntry).filter(
            DatabaseEntry.file_id == TEST_RECORD_1["file_id"]).first()

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
        assert self.db_session.query(DatabaseEntry).filter(
            DatabaseEntry.file_id == TEST_RECORD_1["file_id"]).first() is None

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
        returned_file_record = self.db_session.query(DatabaseEntry).filter(
            DatabaseEntry.file_id == RENAMED_TEST_RECORD_1["file_id"]).first()

        assert returned_file_record.file_id == RENAMED_TEST_RECORD_1["file_id"]
        assert returned_file_record.last_modified_timestamp > returned_file_record.created_timestamp

    def test_update_file_record_with_non_existent_file_id_raises_database_write_error(self, test_database_entry):
        # Act and assert
        with pytest.raises(DatabaseReadError):
            # Update test_file_metadata with a non-existent file id
            self.db_manager.update_file_record(**NON_EXISTENT_TEST_RECORD)
