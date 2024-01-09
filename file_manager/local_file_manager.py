from typing import Tuple, IO

from file_manager.abstract_file_manager import AbstractFileManager
from uuid import uuid4
from pathlib import Path
from dotenv import load_dotenv
import os
from exceptions.file_exceptions import FileDownloadError, FileUploadError, FileDeleteError, FileDoesNotExistError, FileUpdateError

load_dotenv()

upload_path = Path(os.getenv("UPLOAD_DIRECTORY"))
download_path = Path(os.getenv("DOWNLOAD_DIRECTORY"))


class LocalFileManager(AbstractFileManager):
    def upload_file(self, file: IO) -> Tuple[str, Path]:
        # generate a file id
        file_id = str(uuid4())
        file_location = upload_path / file_id

        try:
            # save the file
            with open(file_location, "wb") as f:
                f.write(file.read())

            # return the file id and the file path
        except IOError as e:
            raise FileUploadError(f'Error occurred while uploading file: {e}')
        return file_id, file_location

    def download_file(self, file_id: str) -> Path:
        # Copy the file to the download path and return the path
        download_file_path = download_path / file_id

        try:
            with open(f'{upload_path}/{file_id}', 'rb') as f:
                with open(download_file_path, 'wb') as g:
                    g.write(f.read())
        except FileNotFoundError:
            raise FileDoesNotExistError(f'File with id {file_id} does not exist')
        except IOError as e:
            raise FileDownloadError(f'Error occurred while downloading file: {e}')
        return download_file_path

    def rename_file(self, file_id: str, new_file_id: str) -> str:
        old_file_location = upload_path / file_id
        new_file_location = upload_path / new_file_id

        try:
            old_file_location.rename(new_file_location)
        except FileNotFoundError:
            raise FileDoesNotExistError(f'File with id {file_id} does not exist')
        except IOError as e:
            raise FileUpdateError(f'Error occurred while renaming file: {e}')

        return new_file_id

    def delete_file(self, file_id: str) -> str:
        file_location = upload_path / file_id
        try:
            file_location.unlink()
        except FileNotFoundError:
            raise FileDoesNotExistError(f'File with id {file_id} does not exist')
        except IOError as e:
            raise FileDeleteError(f'Error occurred while deleting file: {e}')
        return file_id

# if __name__ == "__main__":
#     if not os.path.exists(upload_path):
#         os.makedirs(upload_path)
#     # create a local file manager
#     local_file_manager = LocalFileManager()
#
#     # upload a file
#     with open('../data/test.png', 'rb') as f:
#         file_id, file_path = local_file_manager.upload_file(f)
#     print(f'Uploaded file with id {file_id} to path {file_path}')
#
#     # download a file
#     file = local_file_manager.download_file(file_id)
#     print(file)
#     print(f'Downloaded file with id {file_id}')
#
#     # rename a file
#     new_file_id = local_file_manager.rename_file(file_id, 'new_file_id')
#
#     # delete a file
#     local_file_manager.delete_file(new_file_id)
#     print(f'Deleted file with id {new_file_id}')
