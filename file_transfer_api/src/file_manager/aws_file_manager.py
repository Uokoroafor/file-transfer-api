from pathlib import Path
from uuid import uuid4

from src.file_manager.abstract_file_manager import AbstractFileManager
import boto3
import os
from botocore.exceptions import NoCredentialsError
from src.exceptions.file_exceptions import (FileDownloadError, FileUploadError, FileDeleteError, FileDoesNotExistError,
                                            FileUpdateError)
from src.file_manager.utils.url_utils import URLPath
from typing import IO, Optional

# Get download location from the environment
download_path = os.getenv("DOWNLOAD_DIRECTORY", default="data/downloads")


class AWSFileManager(AbstractFileManager):
    def __init__(self, target_bucket: str, s3_client: Optional[boto3.client] = boto3.client("s3")):
        """Initialises the AWS file manager.

        Args:
            target_bucket: Name of the target bucket in AWS S3.
            s3_client: AWS S3 client.
        """
        self.client = s3_client
        self.target_bucket = target_bucket

    def upload_file(self, file: IO) -> URLPath:
        """Uploads a file to a target bucket in AWS S3.

        Args:
            file: File to upload.

        Returns:
            The path of the file uploaded.

        Raises:
            FileUploadError: If an error occurs while uploading the file.
        """
        # Generate a file id
        file_id = str(uuid4())

        try:
            # Save the file
            self.client.upload_fileobj(file, self.target_bucket, file_id)
        except NoCredentialsError:
            raise FileUploadError
        # Return the file id and the file path of where it was saved in the s3 bucket
        full_path = "s3://" + self.target_bucket + "/" + file_id

        # Return url as path object

        return URLPath(full_path)

    def download_file(self, file_id: str) -> Path:
        """Downloads a file from a target bucket in AWS S3.

        Args:
            file_id: Id of the file to download.

        Returns:
            The path of the file downloaded.

        Raises:
            FileDownloadError: If an error occurs while downloading the file.
            FileDoesNotExistError: If the file does not exist.
        """
        try:
            self.client.download_file(self.target_bucket, file_id, f"{download_path}/{file_id}")
        except NoCredentialsError:
            raise FileDownloadError
        except FileNotFoundError:
            raise FileDoesNotExistError
        full_path = Path(download_path) / file_id
        return full_path

    def delete_file(self, file_name: str):
        """Deletes a file from a target bucket in AWS S3.

        Args:
            file_name: Name of the file to delete.

        Raises:
            FileDeleteError: If an error occurs while deleting the file.
        """

        try:
            self.client.delete_object(Bucket=self.target_bucket, Key=file_name)
        except NoCredentialsError:
            raise FileDeleteError

    def rename_file(self, file_id: str, new_file_id: str):
        """Renames a file in a target bucket in AWS S3.

        Args:
            file_id: Id of the file to rename.
            new_file_id: New id of the file.

        Raises:
            FileUpdateError: If an error occurs while renaming the file.
        """
        try:
            self.client.copy_object(Bucket=self.target_bucket, CopySource=f"{self.target_bucket}/{file_id}",
                                    Key=new_file_id)
            self.client.delete_object(Bucket=self.target_bucket, Key=file_id)
        except NoCredentialsError:
            raise FileUpdateError
