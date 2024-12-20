import argparse
from config.settings import Config
from data.drive_client import list_files_in_drive, download_file
from data.file_parser import is_google_drive_path, parse_local_files
from config.secrets_manager import get_credentials
from googleapiclient.discovery import build
import os
from pathlib import Path
from config.logging_config import Logger

logger = Logger().logger


def process_photos(input_path: str) -> None:
    """Process photos from a given directory path, supporting both Google Drive and local paths."""

    TEMP_FOLDER = "/tmp"  # This should be defined or configured properly

    if is_google_drive_path(input_path):
        logger.info("Detected Google Drive path.")

        try:
            credentials = get_credentials()
            service = build("drive", "v3", credentials=credentials)
            drive_files = list_files_in_drive(service, input_path)

            if not os.path.exists(TEMP_FOLDER):
                os.makedirs(TEMP_FOLDER)

            for drive_file in drive_files:
                destination = os.path.join(TEMP_FOLDER, drive_file["name"])
                download_file(service, drive_file["id"], destination)
                logger.info(f"Downloaded {drive_file['name']} to {TEMP_FOLDER}")

        except Exception as e:
            logger.error(f"An error occurred while processing Google Drive files: {e}")

    else:
        logger.info(f"Detected local path")
        try:
            local_files = parse_local_files(Path(input_path), extensions=[".heic", ".jpg", ".png"])
            for file in local_files:
                logger.info(f"Processing local file: {file}")

        except Exception as e:
            logger.error(f"An error occurred while processing local files: {e}")


def main():
    parser = argparse.ArgumentParser(description="Photo Manager CLI")
    config = Config.get_instance()

    parser.add_argument(
        "--input",
        required=False,
        default=config.get("directories.input"),
        help="Path to the input directory (Google Drive folder ID or local directory)",
    )
    args = parser.parse_args()
    process_photos(args.input)


if __name__ == "__main__":
    main()
