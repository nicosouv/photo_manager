import os
from google.oauth2 import service_account


def get_credentials():
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "path/to/credentials.json")
    return service_account.Credentials.from_service_account_file(credentials_path)
