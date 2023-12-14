from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from models.database import Base
import os
from dotenv import load_dotenv
from dataclasses import dataclass
load_dotenv()  # Load the variables from .env
TABLE_NAME = os.getenv("LOCAL_DATABASE_TABLE_NAME")


# What information do we want to store in the database for each file?
# Name, ID, Type, Size, Date Created, Date Last Modified
class FileRecord(Base):
    """ File model """
    __tablename__ = TABLE_NAME
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    file_id = Column(String, unique=True, nullable=False)
    content_type = Column(String)
    size = Column(Integer)
    created_timestamp = Column(String, nullable=False)
    last_modified_timestamp = Column(String, nullable=False)

    def __repr__(self):
        return (f"<FileRecord(id={self.id}, name={self.name}, file_id={self.file_id}, content_type={self.content_type}, "
                f"size={self.size}, created_timestamp={self.created_timestamp}, "
                f"last_modified_timestamp={self.last_modified_timestamp})>")


