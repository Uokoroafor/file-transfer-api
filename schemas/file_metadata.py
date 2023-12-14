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