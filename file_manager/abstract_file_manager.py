from abc import ABC, abstractmethod
from pathlib import Path
from typing import Tuple, IO


class AbstractFileManager(ABC):

    @abstractmethod
    def upload_file(self, file: IO) -> Path:
        pass

    @abstractmethod
    def download_file(self, file_id: str) -> Path:
        pass

    @abstractmethod
    def rename_file(self, file_id, new_file_id):
        pass

    @abstractmethod
    def delete_file(self, file_id):
        pass
