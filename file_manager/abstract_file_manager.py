from abc import ABC, abstractmethod
from typing import IO, Tuple


class AbstractFileManager(ABC):

    @abstractmethod
    def upload_file(self, file:IO) -> Tuple[str, str]:
        pass

    @abstractmethod
    def download_file(self, file_id):
        pass

    @abstractmethod
    def rename_file(self, file_id, new_file_id):
        pass

    @abstractmethod
    def delete_file(self, file_id):
        pass


