from typing import Dict, Optional
from fastapi import File, UploadFile
from schemas.file_metadata import FileMetadata
import logging
import logging.handlers
import os


def create_file_metadata(file: UploadFile = File(...)) -> FileMetadata:
    """Create a dictionary of file metadata.

    Args:
        file: File to get metadata from. Defaults to File(...) but will largely be images.

    Returns:
        Dict[str, Any]: Dictionary of file metadata.
    """
    return FileMetadata(name=file.filename, content_type=file.content_type, size=get_file_size(file))


def get_file_size(file: UploadFile = File(...)) -> int:
    """Get the size of a file.

    Args:
        file: File to get size from. Defaults to File(...) but will largely be images.

    Returns:
        int: Size of file in bytes.
    """
    file.file.seek(0, 2)  # Seek to the end of the file
    file_size = file.file.tell()  # Get the position of EOF
    file.file.seek(0)  # Reset the file position to the beginning

    return file_size


class ErrorLogger:
    def __init__(
            self,
            log_file_path: Optional[str] = "logs/errors.log",
            name: Optional[str] = None,
            log_level: int = logging.INFO,
            verbose: bool = False,
    ):
        """Initialise the logger object

        Args:
            log_file_path: Path to the log file, defaults to "logs/errors.log"
            name: Name of the logger, defaults to None
            log_level: Logging level, defaults to logging.INFO
            verbose: Whether to print the last message, defaults to False
        """
        if log_file_path is None:
            log_file_path = "logs/errors.log"

        # Create the logs folder if it doesn't exist
        log_folder = "/".join(log_file_path.split("/")[:-1])
        if not os.path.exists(log_folder):
            os.mkdir(log_folder)
        self.log_file_path = log_file_path
        if name is None:
            name = __name__
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self.messages = []
        self.verbose = verbose

        self._setup_file_handler()

    def _setup_file_handler(self):
        """Set up the file handler for logging"""
        try:
            file_handler = logging.handlers.RotatingFileHandler(
                self.log_file_path, maxBytes=1024 * 1024, backupCount=5
            )
            # maxBytes = 1024 * 1024 = 1 MB and backupCount = 5 means that at most 5 files will be created
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        except Exception as e:
            print(f"Error setting up log file handler: {str(e)}")

    def log_error(self, message: str):
        """Log an error message"""
        self.logger.error(message)
        self.messages.append(message)
        self.print_last_message() if self.verbose else None

    def print_last_message(self):
        """Print the last message in the log file"""
        if self.messages:
            print(self.messages[-1])
        else:
            print("No messages logged.")
