from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class FileMetadata:
    """ A data structure to store file metadata and transferring it between the API and the database
    
    """
    name: str
    content_type: str
    size: int
    file_id: str = ''

    def __repr__(self):
        return (f"<FileMetadata(name={self.name}, content_type={self.content_type}, "
                f"size={self.size}, file_id={self.file_id})>")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the file metadata to a dictionary.
        """
        return {
            'name': self.name,
            'content_type': self.content_type,
            'size': self.size,
            'file_id': self.file_id
        }

    class Config:
        schema_extra = {
            "example": {
                "name": "test.txt",
                "content_type": "text/plain",
                "size": 100,
                "file_id": "123"
            }
        }


if __name__ == '__main__':
    import json
    from pathlib import Path
    import os

    # Create the test_fixtures folder if it doesn't exist
    test_fixtures_folder = Path(__file__).parent.parent / "tests" / "test_fixtures/file_metadata"
    if not test_fixtures_folder.exists():
        os.mkdir(test_fixtures_folder)

    for cls in [FileMetadata]:
        with open(test_fixtures_folder / f"{cls.__name__}.json", "w") as f:
            json.dump(cls.Config.schema_extra["example"], f, indent=4)
