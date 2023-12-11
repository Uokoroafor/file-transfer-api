from pathlib import Path
from typing import List

from fastapi import FastAPI, File, UploadFile, APIRouter
from schemas.responses import FileUploadResponse, FileDownloadResponse, FileReplaceResponse, FileDeleteResponse, \
    FileRenameResponse, StandardResponse
# from exceptions.custom_exceptions import
from services.local_file_manager import LocalFileManager
from services.aws_file_manager import AWSFileManager
import os
from io import BytesIO

router = APIRouter()
FILE_STORAGE_TYPE = os.getenv("FILE_STORAGE_TYPE", "local")

if FILE_STORAGE_TYPE == "local":
    file_manager = LocalFileManager()
elif FILE_STORAGE_TYPE == "aws":
    file_manager = AWSFileManager()
else:
    raise NotImplementedError(f"File storage type {FILE_STORAGE_TYPE} not implemented")


@router.get("/")
async def files_root() -> StandardResponse:
    """This is the root endpoint of the files API. It will return a simple message

    Returns:
        A message welcoming the user to the files API
    """
    return StandardResponse(message="Welcome to the files API")


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> FileUploadResponse:
    """Upload a file to the server.

    Args:
        file: File to upload. Defaults to File(...) but will largely be images.

    Returns:
        File metadata and status.

    Raises:
        FileUploadError: If the file upload fails
    """
    file_content = await file.read()
    file_id, message = file_manager.upload_file(BytesIO(file_content))
    return FileUploadResponse(file_id=file_id, message=message, content_type=file.content_type, status_code=200)


@router.get("/download/{file_id}")
async def download_file(file_id: str) -> FileDownloadResponse:
    """Download a file from the server.

    Args:
        file_id: Id of the file to download

    Returns:
        File metadata and status.

    Raises:
        FileDoesNotExistError: If the file does not exist
        FileDownloadError: If the file download fails
    """
    message = file_manager.download_file(file_id)
    return FileDownloadResponse(file_id=file_id, message=message, status_code=200)
