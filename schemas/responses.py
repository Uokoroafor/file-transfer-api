from abstracts.response_abstract import AbstractResponse


class FileUploadResponse(AbstractResponse):
    """Response model for file upload"""
    file_id: str
    content_type: str

    class Config:
        schema_extra = {
            "example": {
                "file_id": "12345678-1234-5678-1234-567812345678",
                "content_type": "image/jpeg",
                "status_code": 200,
                "message": "File uploaded"
            }
        }


class FileDownloadResponse(AbstractResponse):
    """Response model for file download"""
    file_id: str
    content_type: str

    class Config:
        schema_extra = {
            "example": {
                "file_id": "12345678-1234-5678-1234-567812345678",
                "content_type": "image/jpeg",
                "status_code": 200,
                "message": "File downloaded"
            }
        }


class FileReplaceResponse(AbstractResponse):
    """Response model for file replace"""
    file_id: str
    content_type: str

    class Config:
        schema_extra = {
            "example": {
                "file_id": "12345678-1234-5678-1234-567812345678",
                "content_type": "image/jpeg",
                "status_code": 200,
                "message": "File updated"
            }
        }


class FileDeleteResponse(AbstractResponse):
    """Response model for file delete"""
    file_id: str

    class Config:
        schema_extra = {
            "example": {
                "file_id": "12345678-1234-5678-1234-567812345678",
                "status_code": 200,
                "message": "File deleted"
            }
        }


class FileRenameResponse(AbstractResponse):
    """Response model for file rename"""
    old_file_id: str
    new_file_id: str

    class Config:
        schema_extra = {
            "example": {
                "old_file_id": "12345678-1234-5678-1234-567812345678",
                "new_file_id": "28cf0697-1632-4fa5-b0a1-3b58bf57ebe7",
                "status_code": 200,
                "message": "File renamed"
            }
        }
