from pathlib import Path

from fastapi import APIRouter, File, UploadFile, Response
from fastapi.responses import FileResponse, StreamingResponse

from file_manager.local_file_manager import LocalFileManager
from dataclasses import dataclass

router = APIRouter()
file_manager = LocalFileManager()


@dataclass
class CustomResponseWithFileIdAndPath:
    """Response model for standard responses"""
    file_id: str
    file_path: Path

@dataclass
class CustomResponseWithFileID:
    """Response model for standard responses"""
    file_id: str


@dataclass
class CustomResponseWithMessage:
    """Response model for standard responses"""
    message: str


@router.get("/")
async def root() -> CustomResponseWithMessage:
    return CustomResponseWithMessage(message="Welcome to the API")


@router.post("/")
async def upload_file(file: UploadFile = File(...)) -> CustomResponseWithFileIdAndPath:
    file_id, file_path = file_manager.upload_file(file.file)
    return CustomResponseWithFileIdAndPath(file_id=file_id, file_path=file_path)


@router.get("/{file_id}")
async def download_file(file_id: str) -> FileResponse:
    file_str = file_manager.download_file(file_id)
    return FileResponse(file_str)

@router.put("/{file_id}")
async def rename_file(file_id: str, new_file_id: str) -> CustomResponseWithFileID:
    file_id = file_manager.rename_file(file_id, new_file_id)
    return CustomResponseWithFileID(file_id=file_id)


@router.delete("/{file_id}")
async def delete_file(file_id: str) -> CustomResponseWithFileID:
    file_id = file_manager.delete_file(file_id)
    return CustomResponseWithFileID(file_id=file_id)
