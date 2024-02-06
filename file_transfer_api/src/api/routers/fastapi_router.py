from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse

from file_transfer_api.src.file_manager.local_file_manager import LocalFileManager
from file_transfer_api.src.database_manager.local_database_manager import LocalDatabaseManager

from file_transfer_api.src.schemas.custom_responses import FileIdAndPath, CustomMessage
from file_transfer_api.src.api.utils.api_utils import get_file_details

from file_transfer_api.src.exceptions.custom_exception import BaseCustomException
from file_transfer_api.src.exceptions.database_exceptions import DatabaseConnectionError

router = APIRouter()
file_manager = LocalFileManager()
database_manager = LocalDatabaseManager()


@router.on_event('startup')  # Only runs on startup
async def on_start():
    # Test the database connection
    if not database_manager.check_database_connection():
        print("Database connection failed")
        # Raise an exception if the database connection fails
        DatabaseConnectionError("Database connection failed").raise_as_http()
    else:
        print("Database connection successful")


@router.get("/")
async def root() -> CustomMessage:
    return CustomMessage(message="Welcome to the API")


@router.post("/")
async def upload_file(file: UploadFile = File(...)) -> FileIdAndPath:
    try:
        file_path = file_manager.upload_file(file.file)
        file_details = get_file_details(file)

        file_id = file_path.name

        # Create a database record
        database_manager.create_file_record(file_id=file_id, **file_details)

        return FileIdAndPath(file_id=file_id, file_path=file_path)
    except BaseCustomException as e:
        e.raise_as_http()


@router.get("/{file_id}")
async def download_file(file_id: str) -> FileResponse:
    try:
        file_str = file_manager.download_file(file_id)
        # No database operation required
        return FileResponse(file_str)
    except BaseCustomException as e:
        e.raise_as_http()


@router.put("/{file_id}")
async def rename_file(file_id: str, new_file_name: str) -> FileIdAndPath:
    try:
        # No file manager operation required
        # Update the database record
        database_manager.rename_file_record(file_id, new_file_name)
        return FileIdAndPath(file_id=file_id)
    except BaseCustomException as e:
        e.raise_as_http()


@router.delete("/{file_id}")
async def delete_file(file_id: str) -> FileIdAndPath:
    try:
        file_manager.delete_file(file_id)

        # Delete the database record
        database_manager.delete_file_record(file_id)
        return FileIdAndPath(file_id=file_id)
    except BaseCustomException as e:
        e.raise_as_http()
