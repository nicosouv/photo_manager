import pyheif
from PIL import Image

def convert_heic_to_png(input_path, output_path):
    heif_file = pyheif.read(input_path)
    image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data)
    image.save(output_path, format='PNG')
