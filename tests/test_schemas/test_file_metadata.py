import json
from pathlib import Path
import pytest
from schemas.file_metadata import FileMetadata


@pytest.fixture
def file_metadata_json():
    test_fixtures_folder = Path(__file__).parent.parent / "test_fixtures/file_metadata"
    with open(test_fixtures_folder / "FileMetadata.json", "r") as f:
        return json.load(f)

@pytest.fixture
def file_metadata_dict():
    return {"name": "test.txt", "content_type": "text/plain", "size": 100, "file_id": "123"}

@pytest.fixture
def file_metadata():
    return FileMetadata(name="test.txt", content_type="text/plain", size=100, file_id="123")


def test_file_metadata_to_dict(file_metadata_dict):
    file_metadata = FileMetadata(name="test.txt", content_type="text/plain", size=100, file_id="123")
    assert file_metadata.to_dict() == file_metadata_dict


def test_file_metadata_from_dict(file_metadata_dict, file_metadata):
    assert FileMetadata(**file_metadata_dict) == file_metadata


def test_file_metadata_compared_with_loaded_json(file_metadata_json, file_metadata):
    assert FileMetadata(**file_metadata_json) == file_metadata
