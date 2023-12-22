from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class FileIdAndPath:
    """Response model for standard responses"""
    file_id: Optional[str] = None
    file_path: Optional[Path] = None


@dataclass
class CustomResponseWithFileID:
    """Response model for standard responses"""
    file_id: str


@dataclass
class CustomMessage:
    """Response model for standard responses"""
    message: str
