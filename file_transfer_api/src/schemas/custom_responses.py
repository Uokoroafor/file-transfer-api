from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class FileIdAndPath:
    """Response model for standard responses"""
    file_id: str
    file_path: Optional[Path] = None


@dataclass
class CustomMessage:
    """Response model for standard responses"""
    message: str


@dataclass
class ErrorResponse:
    """Response model for standard responses"""
    status_code: int
    message: str
