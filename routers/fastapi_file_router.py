from fastapi import File, UploadFile, APIRouter
from abstracts.exceptions_abstract import BaseCustomException
from schemas.responses import FileDownloadResponse, StandardResponse, FileReplaceResponse, FileDeleteResponse, \
    FileUploadResponse, FileRenameResponse
from services.local_file_manager import LocalFileManager
from services.aws_file_manager import AWSFileManager
import os
from io import BytesIO

from utils.utils import create_file_metadata

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
    """This is the root endpoint of the files section of the API. It will return a simple message

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
        FileDoesNotExistError: If the file does not exist
        FileUploadError: If the file upload fails
    """
    try:
        file_content = await file.read()
        message = file_manager.replace_file(file_id, BytesIO(file_content))
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
    """
    try:
        message = file_manager.delete_file(file_id)
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
    """
    try:
        message = file_manager.rename_file(file_id, new_file_id)
    except BaseCustomException as exc:
        exc.raise_as_http()
    return FileRenameResponse(old_file_id=file_id, new_file_id=new_file_id, message=message)