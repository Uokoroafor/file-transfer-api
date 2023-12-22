from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse

from file_manager.local_file_manager import LocalFileManager

from schemas.responses.custom_responses import FileIdAndPath, CustomMessage

router = APIRouter()
file_manager = LocalFileManager()


@router.get("/")
async def root() -> CustomMessage:
    return CustomMessage(message="Welcome to the API")


@router.post("/")
async def upload_file(file: UploadFile = File(...)) -> FileIdAndPath:
    file_id, file_path = file_manager.upload_file(file.file)
    return FileIdAndPath(file_id=file_id, file_path=file_path)


@router.get("/{file_id}")
async def download_file(file_id: str) -> FileResponse:
    file_str = file_manager.download_file(file_id)
    return FileResponse(file_str)


@router.put("/{file_id}")
async def rename_file(file_id: str, new_file_id: str) -> FileIdAndPath:
    file_id = file_manager.rename_file(file_id, new_file_id)
    return FileIdAndPath(file_id=file_id)


@router.delete("/{file_id}")
async def delete_file(file_id: str) -> FileIdAndPath:
    file_id = file_manager.delete_file(file_id)
    return FileIdAndPath(file_id=file_id)
