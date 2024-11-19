# Utiliser une image de base légère Python
FROM python:3.12-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY app/ ./app
COPY config.json ./config.json
COPY requirements.txt ./requirements.txt

# Installer les dépendances
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Définir le point d'entrée pour exécuter le programme
ENTRYPOINT ["python", "app/cli.py"]
