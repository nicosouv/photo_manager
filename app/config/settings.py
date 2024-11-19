import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(script_dir, "../.."))

CONFIG_FILE = os.path.join(base_dir, "config.json")
LOCAL_CONFIG_FILE = os.path.join(base_dir, "config.local.json")

def load_config():
    # Charger le fichier de configuration local s'il existe
    if os.path.exists(LOCAL_CONFIG_FILE):
        with open(LOCAL_CONFIG_FILE, "r") as file:
            return json.load(file)
    # Sinon, charger le fichier de configuration par défaut
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

CONFIG = load_config()

# Exemple d'utilisation
INPUT_DIRECTORY = CONFIG.get("directories", {}).get("input", "./input")
OUTPUT_DIRECTORY = CONFIG.get("directories", {}).get("output", "./output")
TEMP_FOLDER = CONFIG.get("directories", {}).get("temp", "./tmp")
