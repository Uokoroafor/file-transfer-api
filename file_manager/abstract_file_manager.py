from abc import ABC, abstractmethod
from pathlib import Path
from typing import Tuple, IO


class AbstractFileManager(ABC):

    @abstractmethod
    def upload_file(self, file: IO) -> Tuple[str, Path]:
        pass

    @abstractmethod
    def download_file(self, file_id: str) -> Path:
        pass

    @abstractmethod
    def rename_file(self, file_id, new_file_id) -> Path:
        pass

    @abstractmethod
    def delete_file(self, file_id) -> str:
        pass

# TODO: Rationalise the return types of the methods in the AbstractFileManager class and its concrete implementations.
