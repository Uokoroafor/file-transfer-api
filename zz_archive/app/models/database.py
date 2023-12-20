from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()  # Load the variables from .env

# Database URL, e.g., "postgresql://user:password@localhost/dbname"
DATABASE_URL = os.getenv("LOCAL_DATABASE_URL")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# SessionLocal class is a factory for new Session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for your models
Base = declarative_base()

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
# Base.metadata.create_all(bind=engine)


# Test connection

if __name__ == '__main__':
    conn = engine.connect()
    print(conn)
    conn.close()
