import json
import os
from typing import Dict, Any, Union
from config.logging_config import Logger

logger = Logger().logger


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        # Avoid re-initialization in the singleton pattern
        if not hasattr(self, "_initialized"):
            self._config_data = {}
            self.script_dir: str = os.path.dirname(os.path.abspath(__file__))
            self.base_dir: str = os.path.abspath(os.path.join(self.script_dir, "../.."))
            self.CONFIG_FILE: str = os.path.join(self.base_dir, "config.json")
            self.LOCAL_CONFIG_FILE: str = os.path.join(self.base_dir, "config.local.json")
            self.local_config_loaded = False
            self.default_config_loaded = False
            self.load_configs()
            self._initialized = True

    def load_configs(self) -> None:
        config: Dict[str, Any] = {}

        # Load the default configuration file
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, "r") as file:
                config = json.load(file)
                self.default_config_loaded = True

        # Load the local configuration file if it exists and merge properties
        if os.path.exists(self.LOCAL_CONFIG_FILE):
            with open(self.LOCAL_CONFIG_FILE, "r") as file:
                local_config: Dict[str, Any] = json.load(file)
                config.update(local_config)
                self.local_config_loaded = True

        self._config_data = config

    def get(self, property_path: str) -> Any:
        keys = property_path.split(".")
        value: Union[Dict[str, Any], Any] = self._config_data

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                error_message = f"Configuration property '{property_path}' not found in any configuration file."
                logger.error(error_message)
                raise KeyError(error_message)

        return value

    @classmethod
    def get_instance(cls) -> "Config":
        return cls()
