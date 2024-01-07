from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse

from file_manager.local_file_manager import LocalFileManager
from database_manager.local_database_manager import LocalDatabaseManager

from schemas.custom_responses import FileIdAndPath, CustomMessage
from api.utils.api_utils import get_file_details

from exceptions.custom_exception import BaseCustomException

router = APIRouter()
file_manager = LocalFileManager()
database_manager = LocalDatabaseManager()


@router.get("/")
async def root() -> CustomMessage:
    return CustomMessage(message="Welcome to the API")


@router.post("/")
async def upload_file(file: UploadFile = File(...)) -> FileIdAndPath:
    try:
        file_id, file_path = file_manager.upload_file(file.file)
        file_details = get_file_details(file)

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
async def rename_file(file_id: str, new_file_id: str) -> FileIdAndPath:
    try:
        # Rename the file
        _ = file_manager.rename_file(file_id, new_file_id)

        # Update the database record
        database_manager.rename_file_record(file_id, new_file_id)
        return FileIdAndPath(file_id=file_id)
    except BaseCustomException as e:
        e.raise_as_http()


@router.delete("/{file_id}")
async def delete_file(file_id: str) -> FileIdAndPath:
    try:
        file_id = file_manager.delete_file(file_id)

        # Delete the database record
        database_manager.delete_file_record(file_id)
        return FileIdAndPath(file_id=file_id)
    except BaseCustomException as e:
        e.raise_as_http()
