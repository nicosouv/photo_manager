from typing import List, Union
from data.drive_client import list_files_in_drive, download_file
from config.secrets_manager import get_credentials
from googleapiclient.discovery import build
import os
from pathlib import Path
from config.logging_config import Logger
from models.file import File

logger = Logger().logger


def is_google_drive_path(path: str) -> bool:
    """Detect if path is similar to a gDrive ID"""
    return len(path) == 33 and not Path(path).exists()


def list_files(directory: Path, extensions: List[str]) -> List["File"]:
    """Parse and list local files"""
    paths = [f for f in directory.iterdir() if f.suffix.lower() in extensions]
    files = [File(path) for path in paths]
    return files


def parse_local_files(input_path: str):
    try:
        local_files = list_files(Path(input_path), extensions=[".heic", ".jpg", ".png"])
        logger.info(f"Found {len(local_files)} local files.")
        for file in local_files:
            logger.info(f"Processing local file: {file}")

        return local_files

    except Exception as e:
        logger.error(f"An error occurred while processing local files: {e}")


def process_input_path(input_path: Union[str, Path]) -> None:
    temp_folder: str = "./tmp"  # This should be defined or configured properly

    if is_google_drive_path(input_path):
        logger.info("Detected Google Drive path.")

        try:
            credentials = get_credentials()
            service = build("drive", "v3", credentials=credentials)
            drive_files = list_files_in_drive(service, input_path)
            logger.info(f"Found {len(drive_files)} files in Google Drive.")

            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)

            for drive_file in drive_files:
                destination = os.path.join(temp_folder, drive_file["name"])
                download_file(service, drive_file["id"], destination)
                logger.info(f"Downloaded {drive_file['name']} to {temp_folder}")

            parse_local_files(temp_folder)

        except Exception as e:
            logger.error(f"An error occurred while processing Google Drive files: {e}")

    else:
        logger.info("Detected local path")
        parse_local_files(input_path)
