from abstracts.response_abstract import CustomResponse
from dataclasses import dataclass


@dataclass
class FileUploadResponse:
    """Response model for file upload"""
    file_id: str
    content_type: str
    message: str

    class Config:
        schema_extra = {
            "example": {
                "file_id": "12345678-1234-5678-1234-567812345678",
                "content_type": "image/jpeg",
                "status_code": 200,
                "message": "File uploaded"
            }
        }


@dataclass
class FileDownloadResponse:
    """Response model for file download"""
    file_id: str
    message: str

    class Config:
        schema_extra = {
            "example": {
                "file_id": "12345678-1234-5678-1234-567812345678",
                "status_code": 200,
                "message": "File downloaded"
            }
        }


@dataclass
class FileReplaceResponse:
    """Response model for file replace"""
    file_id: str
    content_type: str
    message: str

    class Config:
        schema_extra = {
            "example": {
                "file_id": "12345678-1234-5678-1234-567812345678",
                "content_type": "image/jpeg",
                "status_code": 200,
                "message": "File updated"
            }
        }


@dataclass
class FileDeleteResponse:
    """Response model for file delete"""
    file_id: str
    message: str

    class Config:
        schema_extra = {
            "example": {
                "file_id": "12345678-1234-5678-1234-567812345678",
                "status_code": 200,
                "message": "File deleted"
            }
        }


@dataclass
class FileRenameResponse:
    """Response model for file rename"""
    old_file_id: str
    new_file_id: str
    message: str

    class Config:
        schema_extra = {
            "example": {
                "old_file_id": "12345678-1234-5678-1234-567812345678",
                "new_file_id": "28cf0697-1632-4fa5-b0a1-3b58bf57ebe7",
                "status_code": 200,
                "message": "File renamed"
            }
        }


@dataclass
class StandardResponse:
    """Response model for standard responses"""
    message: str

    class Config:
        schema_extra = {
            "example": {
                "message": "Welcome to the API",
                "status_code": 200
            }
        }


@dataclass
class ErrorResponse:
    """Response model for errors"""
    message: str

    class Config:
        schema_extra = {
            "example": {
                "message": "File not found",
                "status_code": 404
            }
        }


@dataclass
class DatabaseSelectResponse:
    """Response model for database select"""
    file_id: str
    name: str
    content_type: str
    size: int
    created_timestamp: str
    last_modified_timestamp: str

    class Config:
        schema_extra = {
            "example": {
                "file_id": "12345678-1234-5678-1234-567812345678",
                "name": "image.jpg",
                "content_type": "image/jpeg",
                "size": 123456,
                "created_timestamp": "2021-01-01T00:00:00",
                "last_modified_timestamp": "2021-01-01T00:00:00",
                "status_code": 200,
                "message": "File selected"
            }
        }


@dataclass
class DatabaseUpdateResponse:
    """Response model for database update"""
    file_id: str
    name: str
    content_type: str
    size: int
    created_timestamp: str
    last_modified_timestamp: str

    class Config:
        schema_extra = {
            "example": {
                "file_id": "12345678-1234-5678-1234-567812345678",
                "name": "image.jpg",
                "content_type": "image/jpeg",
                "size": 123456,
                "created_timestamp": "2021-01-01T00:00:00",
                "last_modified_timestamp": "2021-01-01T00:00:00",
                "status_code": 200,
                "message": "File updated"
            }
        }


@dataclass
class DatabaseDeleteResponse:
    """Response model for database delete"""
    file_id: str

    class Config:
        schema_extra = {
            "example": {
                "file_id": "12345678-1234-5678-1234-567812345678",
                "status_code": 200,
                "message": "File deleted"
            }
        }


# For each class save the config example as a json in the ../tests/test_fixtures folder
if __name__ == '__main__':
    import json
    from pathlib import Path
    import os

    # Create the test_fixtures folder if it doesn't exist
    test_fixtures_folder = Path(__file__).parent.parent / "tests" / "test_fixtures/responses"
    if not test_fixtures_folder.exists():
        os.mkdir(test_fixtures_folder)

    # Save the config example as a json in the ../tests/test_fixtures folder
    for cls in [FileUploadResponse, FileDownloadResponse, FileReplaceResponse, FileDeleteResponse, FileRenameResponse,
                StandardResponse, ErrorResponse, DatabaseSelectResponse, DatabaseUpdateResponse,
                DatabaseDeleteResponse]:
        with open(test_fixtures_folder / f"{cls.__name__}.json", "w") as f:
            json.dump(cls.Config.schema_extra["example"], f, indent=4)
