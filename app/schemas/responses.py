from dataclasses import dataclass
from app.abstracts.response_abstract import CustomResponse


@dataclass
class FileUploadResponse(CustomResponse):
    """Response model for file upload"""
    file_id: str
    content_type: str
    message: str

    class Config:
        schema_extra = {
            "example": {
                "file_id": "123",
                "content_type": "image/jpeg",
                "message": "File uploaded"
            }
        }


@dataclass
class FileDownloadResponse(CustomResponse):
    """Response model for file download"""
    file_id: str
    message: str

    class Config:
        schema_extra = {
            "example": {
                "file_id": "123",
                "message": "File downloaded"
            }
        }


@dataclass
class FileReplaceResponse(CustomResponse):
    """Response model for file replace"""
    file_id: str
    content_type: str
    message: str

    class Config:
        schema_extra = {
            "example": {
                "file_id": "123",
                "content_type": "image/jpeg",
                "message": "File replaced"
            }
        }


@dataclass
class FileDeleteResponse(CustomResponse):
    """Response model for file delete"""
    file_id: str
    message: str

    class Config:
        schema_extra = {
            "example": {
                "file_id": "123",
                "message": "File deleted"
            }
        }


@dataclass
class FileRenameResponse(CustomResponse):
    """Response model for file rename"""
    old_file_id: str
    new_file_id: str
    message: str

    class Config:
        schema_extra = {
            "example": {
                "old_file_id": "123",
                "new_file_id": "456",
                "message": "File renamed"
            }
        }


@dataclass
class StandardResponse(CustomResponse):
    """Response model for standard responses"""
    message: str

    class Config:
        schema_extra = {
            "example": {
                "message": "Welcome to the API",
            }
        }


@dataclass
class ErrorResponse(CustomResponse):
    """Response model for errors"""
    message: str

    class Config:
        schema_extra = {
            "example": {
                "message": "File not found"
            }
        }


@dataclass
class DatabaseSelectResponse(CustomResponse):
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
                "file_id": "123",
                "name": "image.jpg",
                "content_type": "image/jpeg",
                "size": 100,
                "created_timestamp": "2021-01-01T00:00:00",
                "last_modified_timestamp": "2021-01-01T00:00:00"
            }
        }


@dataclass
class DatabaseUpdateResponse(CustomResponse):
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
                "file_id": "123",
                "name": "image.jpg",
                "content_type": "image/jpeg",
                "size": 100,
                "created_timestamp": "2021-01-01T00:00:00",
                "last_modified_timestamp": "2021-01-01T00:00:00"
            }
        }


@dataclass
class DatabaseDeleteResponse(CustomResponse):
    """Response model for database delete"""
    file_id: str

    class Config:
        schema_extra = {
            "example": {
                "file_id": "123",
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
