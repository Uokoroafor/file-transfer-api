import logging
import logging.handlers
import os
from typing import Optional


class ErrorLogger:
    def __init__(
            self,
            log_file_path: Optional[str] = "logs/errors.log",
            name: Optional[str] = None,
            log_level: int = logging.ERROR
    ):
        """Initialise the logger object

        Args:
            log_file_path: Path to the log file, defaults to "logs/errors.log"
            name: Name of the logger, defaults to None
            log_level: Logging level, defaults to logging.INFO
        """
        if log_file_path is None:
            log_file_path = "logs/errors.log"

        # Create the logs folder if it doesn't exist
        log_folder = "/".join(log_file_path.split("/")[:-1])
        if not os.path.exists(log_folder):
            os.mkdir(log_folder)
        self.log_file_path = log_file_path

        if name is None:
            name = "ErrorLogger"
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        self._setup_file_handler()

    def _setup_file_handler(self):
        """Set up the file handler for logging"""
        try:
            file_handler = logging.handlers.RotatingFileHandler(
                self.log_file_path, maxBytes=1024 * 1024, backupCount=5)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        except Exception as e:
            print(f"Error setting up log file handler: {str(e)}")

    def log(self, message: str, log_level: int = logging.ERROR):
        """Log a message"""
        if log_level == logging.INFO:
            self.logger.info(message)
        elif log_level == logging.WARNING:
            self.logger.warning(message)
        elif log_level == logging.ERROR:
            self.logger.error(message)
        else:
            self.logger.critical(message)
