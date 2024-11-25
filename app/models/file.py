from pathlib import Path
from datetime import datetime
from PIL import Image, ExifTags
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class File:
    """Represents a file and its metadata."""

    def __init__(self, path: Path):
        self.path = path
        self.name = path.name
        self.creation_date = self.get_creation_date()
        self.capture_date = self.get_capture_date()
        self.size = self.get_size()
        self.extension = path.suffix.lower()

    def get_creation_date(self) -> Optional[datetime]:
        """Fetches the file's creation date from the filesystem."""
        try:
            return datetime.fromtimestamp(self.path.stat().st_ctime)
        except Exception as e:
            logger.error(f"Could not retrieve creation date for {self.path}: {e}")
            return None

    def get_capture_date(self) -> Optional[datetime]:
        """Fetches the photo's capture date from its EXIF metadata."""
        if self.extension not in [".heic", ".jpg", ".png"]:
            return None

        try:
            with Image.open(self.path) as img:
                exif_data = img._getexif()
                if exif_data:
                    for tag, value in exif_data.items():
                        tag_name = ExifTags.TAGS.get(tag)
                        if tag_name == "DateTimeOriginal":
                            return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
        except Exception as e:
            logger.warning(f"No capture date found for {self.path}: {e}")
        return None

    def get_size(self) -> Optional[int]:
        """Gets the file size in bytes."""
        try:
            return self.path.stat().st_size
        except Exception as e:
            logger.error(f"Could not retrieve size for {self.path}: {e}")
            return None

    def convert_heic_to_jpg(self) -> None:
        """Converts a .heic file to .jpg and updates the file's path."""
        if self.extension != ".heic":
            logger.info(f"File {self.path} is not a .heic file. Skipping conversion.")
            return

        try:
            # new jpg name
            new_path = self.path.with_suffix(".jpg")
            logger.info(f"Converting {self.path} to {new_path}")

            # conversion
            with Image.open(self.path) as img:
                img.convert("RGB").save(new_path, "JPEG")

            # update object
            self.path = new_path
            self.name = new_path.name
            self.extension = ".jpg"

            logger.info(f"File converted and path updated to {self.path}")

        except Exception as e:
            logger.error(f"Failed to convert {self.path}: {e}")

    def __repr__(self) -> str:
        return (
            f"File(name={self.name}, path={self.path}, creation_date={self.creation_date}, "
            f"capture_date={self.capture_date}, size={self.size}, extension={self.extension})"
        )
