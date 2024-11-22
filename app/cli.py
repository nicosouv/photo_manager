import argparse
from config.settings import Config
from config.logging_config import Logger
from data.file_parser import process_input_path

logger = Logger().logger


def process_photos(input_path: str) -> None:
    """Process photos from a given directory path, supporting both Google Drive and local paths."""
    process_input_path(input_path)


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
