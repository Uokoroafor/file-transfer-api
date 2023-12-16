import json
from pathlib import Path

import pytest

from app.schemas.responses import DatabaseDeleteResponse, DatabaseUpdateResponse, DatabaseSelectResponse, \
    FileUploadResponse, FileDownloadResponse, FileReplaceResponse, FileDeleteResponse, FileRenameResponse, \
    StandardResponse, ErrorResponse

RESPONSE_CLASSES = {"FileUploadResponse": FileUploadResponse,
                    "FileDownloadResponse": FileDownloadResponse,
                    "FileReplaceResponse": FileReplaceResponse,
                    "FileDeleteResponse": FileDeleteResponse,
                    "FileRenameResponse": FileRenameResponse,
                    "StandardResponse": StandardResponse,
                    "ErrorResponse": ErrorResponse,
                    "DatabaseSelectResponse": DatabaseSelectResponse,
                    "DatabaseUpdateResponse": DatabaseUpdateResponse,
                    "DatabaseDeleteResponse": DatabaseDeleteResponse
                    }


def get_response_values(val_list):
    vals_dict = {
        "file_id": "123",
        "old_file_id": "123",
        "new_file_id": "456",
        "name": "image.jpg",
        "content_type": "image/jpeg",
        "size": 100,
        "created_timestamp": "2021-01-01T00:00:00",
        "last_modified_timestamp": "2021-01-01T00:00:00",
        "updated_message": "File updated",
        "deleted_message": "File deleted",
        "downloaded_message": "File downloaded",
        "uploaded_message": "File uploaded",
        "replaced_message": "File replaced",
        "renamed_message": "File renamed",
        "error_message": "File not found",
        "standard_message": "Welcome to the API"}

    # Look up keys in val_list and return the values
    subset_dict = {key: vals_dict[key] for key in val_list}

    # If the key contains message, change it to message
    for key in subset_dict.keys():
        if key.endswith("message"):
            subset_dict["message"] = subset_dict.pop(key)
            break
    return subset_dict


REQUIRED_FIELDS_LOOKUP = {
    "FileUploadResponse": ["file_id", "content_type", "uploaded_message"],
    "FileDownloadResponse": ["file_id", "downloaded_message"],
    "FileReplaceResponse": ["file_id", "content_type", "replaced_message"],
    "FileDeleteResponse": ["file_id", "deleted_message"],
    "FileRenameResponse": ["old_file_id", "new_file_id", "renamed_message"],
    "StandardResponse": ["standard_message"],
    "ErrorResponse": ["error_message"],
    "DatabaseSelectResponse": ["file_id", "name", "content_type", "size", "created_timestamp",
                               "last_modified_timestamp"],
    "DatabaseUpdateResponse": ["file_id", "name", "content_type", "size", "created_timestamp",
                               "last_modified_timestamp"],
    "DatabaseDeleteResponse": ["file_id"]
}


@pytest.mark.parametrize("response_class", REQUIRED_FIELDS_LOOKUP.keys())
def test_response(response_class):
    # load response values
    required_keys = REQUIRED_FIELDS_LOOKUP[response_class]
    response_values = get_response_values(required_keys)

    # create response object
    response = RESPONSE_CLASSES[response_class](**response_values)

    # load expected response from json
    with open(Path(__file__).parent.parent / f"test_fixtures/responses/{response_class}.json") as f:
        expected_response = json.load(f)

    assert response.to_dict() == expected_response
