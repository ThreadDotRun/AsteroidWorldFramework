from PIL import Image
import os

class WebpToJpgConverter:
    def __init__(self, input_dir, output_dir, quality=95):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.quality = quality
        os.makedirs(self.output_dir, exist_ok=True)

    def convert_all(self):
        for filename in os.listdir(self.input_dir):
            if filename.endswith('.webp'):
                self.convert_to_jpg(filename)

    def convert_to_jpg(self, filename):
        webp_path = os.path.join(self.input_dir, filename)
        jpg_filename = filename.replace('.webp', '.jpg')
        jpg_path = os.path.join(self.output_dir, jpg_filename)

        with Image.open(webp_path) as img:
            img.convert('RGB').save(jpg_path, 'JPEG', quality=self.quality)
        print(f'Converted: {webp_path} -> {jpg_path}')

# Example usage:
converter = WebpToJpgConverter('./textures/', './textures/')
converter.convert_all()
