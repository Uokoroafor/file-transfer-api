import datetime
from dataclasses import dataclass
from typing import Dict, Any
from sqlalchemy import Column, Integer, String, DateTime
from database_manager.database_connection.local_database import Base
import os
from dotenv import load_dotenv

load_dotenv()  # Load the variables from .env
TABLE_NAME = os.getenv("LOCAL_DATABASE_TABLE_NAME")


@dataclass
class DatabaseEntry(Base):
    """A dataclass for database entries"""

    __tablename__ = TABLE_NAME
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    file_id = Column(String, unique=True, nullable=False)
    content_type = Column(String)
    size = Column(Integer)
    created_timestamp = Column(DateTime, nullable=False)
    last_modified_timestamp = Column(DateTime, nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "file_id": self.file_id,
            "content_type": self.content_type,
            "size": self.size,
            "created_timestamp": self.created_timestamp,
            "last_modified_timestamp": self.last_modified_timestamp}

    def __repr__(self):
        return (
            f"<FileRecord(id={self.id}, name={self.name}, file_id={self.file_id}, content_type={self.content_type}, "
            f"size={self.size}, created_timestamp={self.created_timestamp}, "
            f"last_modified_timestamp={self.last_modified_timestamp})>")
