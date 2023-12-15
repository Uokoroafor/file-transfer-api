import os
from io import BytesIO
from fastapi import APIRouter
from fastapi import File, UploadFile
from abstracts.exceptions_abstract import BaseCustomException
from schemas.responses import FileUploadResponse, FileDownloadResponse, FileReplaceResponse, FileDeleteResponse, \
    FileRenameResponse, StandardResponse, DatabaseSelectResponse
from services.aws_database_manager import AWSDatabaseManager
from services.aws_file_manager import AWSFileManager
from services.local_database_manager import LocalDatabaseManager
from services.local_file_manager import LocalFileManager
from utils.utils import create_file_metadata

router = APIRouter()
FILE_STORAGE_TYPE = os.getenv("FILE_STORAGE_TYPE", "local")

if FILE_STORAGE_TYPE == "local":
    file_manager = LocalFileManager()
elif FILE_STORAGE_TYPE == "aws":
    file_manager = AWSFileManager()
else:
    raise NotImplementedError(f"File storage type {FILE_STORAGE_TYPE} not implemented")

DATABASE_LOCATION = os.getenv("DATABASE_LOCATION", "local")

if DATABASE_LOCATION == "local":
    database_manager = LocalDatabaseManager()
elif DATABASE_LOCATION == "aws":
    database_manager = AWSDatabaseManager()
else:
    raise NotImplementedError(f"Database location {DATABASE_LOCATION} not implemented")


@router.get("/")
async def full_root() -> StandardResponse:
    """This is the root endpoint of the full API. It will return a simple message

    Returns:
        A message welcoming the user to the API
    """
    return StandardResponse(message="Welcome to the full API")


@router.post("/upload/{file_id}")
async def upload_file_and_create_record(file: UploadFile = File(...)) -> FileUploadResponse:
    """Upload a file to the server and create a record in the database.

    Args:
        file: File to upload. Defaults to File(...) but will largely be images.

    Returns:
        File metadata and status.

    Raises:
        FileUploadError: If the file upload fails
        DatabaseWriteError: If the database write fails
    """
    try:
        file_content = await file.read()
        file_metadata = create_file_metadata(file)
        file_id, message = file_manager.upload_file(BytesIO(file_content))

        # Add the file id to the file metadata
        file_metadata.file_id = file_id

        # Create the file record
        database_manager.create_file_record(**file_metadata.to_dict())
    except BaseCustomException as exc:
        exc.raise_as_http()

    return FileUploadResponse(file_id=file_id, message=message, content_type=file.content_type)


@router.get("/download/{file_id}")
async def download_file(file_id: str, download_name: str = None) -> FileDownloadResponse:
    """Download a file from the server.

    Args:
        file_id: Id of the file to download
        download_name: Name to give the downloaded file

    Returns:
        File metadata and status.

    Raises:
        FileDoesNotExistError: If the file does not exist
        FileDownloadError: If the file download fails
    """
    try:
        message = file_manager.download_file(file_id, download_name)
    except BaseCustomException as exc:
        exc.raise_as_http()
    return FileDownloadResponse(file_id=file_id, message=message)


@router.put("/replace/{file_id}")
async def replace_file(file_id: str, file: UploadFile = File(...)) -> FileReplaceResponse:
    """Replace a file on the server with a new file

    Args:
        file_id: Id of the file to replace
        file: File to replace. Defaults to File(...) but will largely be images.

    Returns:
        File metadata and status.

    Raises:
        FileReplaceError: If the file replace fails
        DatabaseReadError: If the database read fails
        DatabaseWriteError: If the database write fails
    """
    try:
        file_content = await file.read()
        message = file_manager.replace_file(file_id, BytesIO(file_content))

        # Create FileMetadata object
        file_metadata = create_file_metadata(file)
        file_metadata.file_id = file_id

        # Update the file record in the database
        database_manager.update_file_record(**file_metadata.to_dict())

    except BaseCustomException as exc:
        exc.raise_as_http()
    return FileReplaceResponse(file_id=file_id, message=message, content_type=file.content_type)


@router.delete("/delete/{file_id}")
async def delete_file(file_id: str) -> FileDeleteResponse:
    """Delete a file from the server.

    Args:
        file_id: Id of the file to delete

    Returns:
        File metadata and status.

    Raises:
        FileDoesNotExistError: If the file does not exist
        FileDeleteError: If the file delete fails
        DatabaseReadError: If the database read fails
        DatabaseWriteError: If the database write fails
    """
    try:
        message = file_manager.delete_file(file_id)

        # Delete the file record from the database
        database_manager.delete_file_record(file_id)

    except BaseCustomException as exc:
        exc.raise_as_http()
    return FileDeleteResponse(file_id=file_id, message=message)


@router.put("/rename/{file_id}")
async def rename_file(file_id: str, new_file_id: str) -> FileRenameResponse:
    """Rename a file on the server.

    Args:
        file_id: Id of the file to rename
        new_file_id: New id of the file

    Returns:
        File metadata and status.

    Raises:
        FileDoesNotExistError: If the file does not exist
        FileRenameError: If the file rename fails
        DatabaseReadError: If the database read fails
        DatabaseWriteError: If the database write fails
    """
    try:
        message = file_manager.rename_file(file_id, new_file_id)

        # Rename the file record in the database
        database_manager.rename_file_record(file_id, new_file_id)

    except BaseCustomException as exc:
        exc.raise_as_http()
    return FileRenameResponse(old_file_id=file_id, new_file_id=new_file_id, message=message)


@router.get("/count")
async def count_files() -> int:
    """Count the number of files in the database.

    Returns:
        Number of files in the database.

    Raises:
        DatabaseReadError: If the manager fails to read the database
    """
    return database_manager.get_count()


@router.get("/detail/{file_id}")
async def get_file_detail(file_id: str) -> DatabaseSelectResponse:
    """Get the detail of a file in the database.

    Args:
        file_id: Id of the file to get detail of

    Returns:
        File metadata and status.

    Raises:
        FileDoesNotExistError: If the file does not exist
    """
    try:
        file_record = database_manager.get_file_record(file_id)
        response = DatabaseSelectResponse(file_id=file_record.file_id,
                                  name=file_record.name,
                                  content_type=file_record.content_type,
                                  size=file_record.size,
                                  created_timestamp=file_record.created_timestamp,
                                  last_modified_timestamp=file_record.last_modified_timestamp)
    except BaseCustomException as exc:
        exc.raise_as_http()
    return response
