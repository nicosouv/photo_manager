from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import os


def list_files_in_drive(service, folder_id):
    """Liste les fichiers dans un dossier Google Drive donné."""
    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query).execute()
    return results.get("files", [])


def download_file(service, file_id, destination_path):
    """Télécharge un fichier depuis Google Drive."""
    request = service.files().get_media(fileId=file_id)
    with open(destination_path, "wb") as file:
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download progress: {int(status.progress() * 100)}%")
