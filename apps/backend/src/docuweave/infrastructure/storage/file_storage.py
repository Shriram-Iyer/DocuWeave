"""
Temporary file storage for generated documents.
Files are stored in a temp directory and served for download.
"""
import tempfile
from pathlib import Path


_STORAGE_DIR = Path(tempfile.gettempdir()) / "docuweave_generated"
_STORAGE_DIR.mkdir(exist_ok=True)


def get_storage_path(filename: str) -> Path:
    return _STORAGE_DIR / filename


def cleanup_file(filename: str) -> None:
    path = _STORAGE_DIR / filename
    if path.exists():
        path.unlink()
