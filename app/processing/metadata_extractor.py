from PIL import Image
from PIL.ExifTags import TAGS


def extract_metadata(image_path):
    image = Image.open(image_path)
    metadata = {}
    for tag, value in image.getexif().items():
        if tag in TAGS:
            metadata[TAGS[tag]] = value
    return metadata
