from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Load Environment Variables

DATABASE_URL = os.getenv("LOCAL_DATABASE_URL", default="sqlite:///./test.db")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# SessionLocal class is a factory for new Session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for the models
Base = declarative_base()
