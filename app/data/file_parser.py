from typing import List, Dict, Union
from pathlib import Path
from googleapiclient.discovery import Resource

def is_google_drive_path(path: str) -> bool:
    """Détecte si un chemin correspond à un ID Google Drive."""
    return len(path) == 33 and not Path(path).exists()

def parse_local_files(directory: Path, extensions: List[str]) -> List[Path]:
    """Parse les fichiers dans un répertoire local."""
    return [f for f in directory.iterdir() if f.suffix in extensions]

def list_files_in_drive(service: Resource, folder_id: str) -> List[Dict[str, str]]:
    """Liste les fichiers dans un dossier Google Drive donné."""
    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query).execute()
    return results.get('files', [])

def process_input_path(service: Resource, input_path: Union[str, Path]) -> None:
    """Traite les fichiers à partir d'un chemin local ou Google Drive."""
    if isinstance(input_path, str) and is_google_drive_path(input_path):
        print("Processing Google Drive folder")
        drive_files = list_files_in_drive(service, input_path)
        print(f"Found {len(drive_files)} files in Google Drive.")
    elif isinstance(input_path, Path):
        print("Processing local folder")
        local_files = parse_local_files(input_path, [".heic", ".png", ".jpg"])
        print(f"Found {len(local_files)} local files.")
