from typing import List

from fastapi import APIRouter
from app.schemas.responses import FileDeleteResponse, \
    StandardResponse, DatabaseSelectResponse
from app.services.local_database_manager import LocalDatabaseManager
from app.services.aws_database_manager import AWSDatabaseManager
import os


router = APIRouter()
DATABASE_LOCATION = os.getenv("DATABASE_LOCATION", "local")

if DATABASE_LOCATION == "local":
    database_manager = LocalDatabaseManager()
elif DATABASE_LOCATION == "aws":
    database_manager = AWSDatabaseManager()
else:
    raise NotImplementedError(f"Database location {DATABASE_LOCATION} not implemented")


@router.get("/")
async def database_root() -> StandardResponse:
    """This is the root endpoint of the database API. It will return a simple message

    Returns:
        A message welcoming the user to the database API
    """
    return StandardResponse(message="Welcome to the database section of the API")


@router.get("/select/{file_id}")
async def select_file(file_id: str) -> DatabaseSelectResponse:
    """Select a file from the database.

    Args:
        file_id: Id of the file to select

    Returns:
        File metadata and status.

    Raises:
        FileDoesNotExistError: If the file does not exist
        FileDownloadError: If the file download fails
    """
    file_record = database_manager.get_file_record(file_id)
    return DatabaseSelectResponse(file_id=file_record.file_id, name=file_record.name,
                                    content_type=file_record.content_type, size=file_record.size,
                                    created_timestamp=file_record.created_timestamp,
                                    last_modified_timestamp=file_record.last_modified_timestamp)


@router.get("/select_all")
async def select_all_files() -> List[DatabaseSelectResponse]:
    """Select all files from the database.

    Returns:
        List of file metadata and status.

    Raises:
        FileDoesNotExistError: If the file does not exist
        FileDownloadError: If the file download fails
    """
    file_records = database_manager.get_all_file_records()
    file_download_responses = []
    for file_record in file_records:
        file_download_responses.append(DatabaseSelectResponse(file_id=file_record.file_id, name=file_record.name,
                                                            content_type=file_record.content_type,
                                                            size=file_record.size,
                                                            created_timestamp=file_record.created_timestamp,
                                                            last_modified_timestamp=file_record.last_modified_timestamp))

    return file_download_responses


@router.get("/count")
async def count_files() -> int:
    """Count the number of files in the database.

    Returns:
        Number of files in the database.

    Raises:
        FileDoesNotExistError: If the file does not exist
        FileDownloadError: If the file download fails
    """
    return database_manager.get_count()


@router.delete("/delete/{file_id}")
async def delete_file(file_id: str) -> FileDeleteResponse:
    """Delete a file from the database.

    Args:
        file_id: Id of the file to delete

    Returns:
        File metadata and status.

    Raises:
        FileDoesNotExistError: If the file does not exist
        FileDownloadError: If the file download fails
    """
    file_record = database_manager.delete_file_record(file_id)
    return FileDeleteResponse(file_id=file_record.file_id)


# @router.put("/rename/{file_id}")
# async def rename_file(file_id: str, new_file_id: str) -> FileRenameResponse:
#     """Rename a file in the database.
#
#     Args:
#         file_id: Id of the file to rename
#         new_file_id: New id of the file
#
#     Returns:
#         File metadata and status.
#
#     Raises:
#         FileDoesNotExistError: If the file does not exist
#         FileRenameError: If the file rename fails
#     """
#     file_record = database_manager.rename_file_record(file_id, new_file_id)
#     return FileRenameResponse(old_file_id=file_id, new_file_id=file_record.file_id)


