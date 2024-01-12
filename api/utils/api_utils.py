import mimetypes
from typing import IO, Union, Dict, Any
from fastapi import UploadFile, File

from database_manager.schemas.content_enum import ContentEnum


def get_file_details(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Get metadata from a file.

    Args:
        file: File to get metadata from. Defaults to File(...) but will largely be images.

    Returns:
        Details from the file.
    """
    file_details = {
        "name": file.filename,
        "content_type": ContentEnum.from_str(file.content_type) if file.content_type else None,
        "size": get_file_size(file.file),
    }
    if file_details["content_type"] is None:
        print(f'Guessing content type for {file_details["name"]}')
        file_details["content_type"] = ContentEnum.from_str(mimetypes.guess_type(file_details["name"])[0])

    return file_details


def get_file_size(file: IO) -> Union[int, float]:
    """Get the size of a file.

    Args:
        file: File to get size from. Defaults to File(...) but will largely be images.

    Returns:
        Size of the file in KB.
    """
    file.seek(0, 2)  # Seek to the end of the file
    file_size = round(file.tell() / 1024.0, 2)  # Get the file size in KB
    file.seek(0)  # Seek back to the start of the file

    return file_size


def guess_file_extension(file: UploadFile = File(...)) -> str:
    """Guess the file extension of a file.

    Args:
        file: File to guess extension from. Defaults to File(...) but will largely be images.

    Returns:
        File extension.
    """
    return mimetypes.guess_extension(file.content_type)

