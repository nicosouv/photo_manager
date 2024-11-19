import logging
import os


class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._setup_logging()
        return cls._instance

    def _setup_logging(self):
        script_dir: str = os.path.dirname(os.path.abspath(__file__))
        base_dir: str = os.path.abspath(os.path.join(script_dir, "../.."))

        # Define the log format
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M")

        # Create a stream handler for console output
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        print(f"{base_dir}/app.log")
        # Create a file handler for log file output
        file_handler = logging.FileHandler(f"{base_dir}/app.log")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # Configure the logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
