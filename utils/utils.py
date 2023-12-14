from typing import Dict, Any
from fastapi import File, UploadFile
from schemas.file_metadata import FileMetadata


def create_file_metadata(file: UploadFile = File(...)) -> FileMetadata:
    """Create a dictionary of file metadata.

    Args:
        file: File to get metadata from. Defaults to File(...) but will largely be images.

    Returns:
        Dict[str, Any]: Dictionary of file metadata.
    """
    return FileMetadata(name=file.filename, content_type=file.content_type, size=get_file_size(file))


def get_file_size(file: UploadFile = File(...)) -> int:
    """Get the size of a file.

    Args:
        file: File to get size from. Defaults to File(...) but will largely be images.

    Returns:
        int: Size of file in bytes.
    """
    file.file.seek(0, 2)  # Seek to the end of the file
    file_size = file.file.tell()  # Get the position of EOF
    file.file.seek(0)  # Reset the file position to the beginning

    return file_size
