from dataclasses import dataclass
from typing import Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, Enum
from src.database_manager.database_connection.local_database import Base
import os
from src.database_manager.schemas.content_enum import ContentEnum

# Load the environment variables
TABLE_NAME = os.getenv("LOCAL_DATABASE_TABLE_NAME",
                       "files")  # The tablename will default to "files" if not specified in .env


@dataclass
class DatabaseEntry(Base):
    """A dataclass for database entries"""

    __tablename__ = TABLE_NAME
    file_id = Column(String, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False)
    content_type = Column(Enum(ContentEnum), nullable=False)
    size = Column(Integer)
    created_timestamp = Column(DateTime, nullable=False)
    last_modified_timestamp = Column(DateTime, nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the database entry to a dictionary.

        Returns:
            Dictionary representation of the database entry.
        """
        return {
            "file_id": self.file_id,
            "name": self.name,
            "content_type": self.content_type,
            "size": self.size,
            "created_timestamp": self.created_timestamp,
            "last_modified_timestamp": self.last_modified_timestamp}

    def equal_to_dict(self, other: Dict[str, Any]) -> bool:
        """Check if the database entry is equal to a dictionary. It does not check the timestamps.

        Args:
            other: Dictionary to compare to.

        Returns:
            True if the database entry is equal to the dictionary.
        """
        return (self.file_id == other.get("file_id")
                and self.name == other.get("name")
                and self.content_type == other.get("content_type")
                and self.size == other.get("size"))

    def __repr__(self):
        return (
            f"<FileRecord(file_id={self.file_id}, name={self.name}, content_type={self.content_type.value}, "
            f"size={self.size}, created_timestamp={self.created_timestamp}, "
            f"last_modified_timestamp={self.last_modified_timestamp})>")

    def __eq__(self, other) -> bool:
        if isinstance(other, DatabaseEntry):
            return (self.file_id == other.file_id
                    and self.name == other.name
                    and self.content_type == other.content_type
                    and self.size == other.size)
        return False
