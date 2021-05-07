import os
from collections import namedtuple
from PIL import Image

ROOT = 'photo/'
HANDLED = 'handled/'
LOGO_PATH = 'logo.png'

Size = namedtuple('Size', ('width', 'height'))
RESIZE = Size(800, 600)
QUALITY = 60


def resize_and_watermark():
    logo = Image.open(LOGO_PATH)

    for folder in os.listdir(ROOT):
        image_folder = f'{ROOT}{folder}/'
        handled_folder = f'{image_folder}{HANDLED}/'
        os.path.exists(handled_folder) or os.makedirs(handled_folder)
        address, _, file_list = next(os.walk(image_folder))
        handled_count = 0
        for i, file in enumerate(file_list):
            if not file.endswith('.docx'):
                try:
                    img = Image.open(f'{address}/{file}')
                    img = img.convert('RGB')
                    img.width <= RESIZE.width or img.thumbnail(RESIZE, Image.ANTIALIAS)
                    img.paste(logo, ((img.width - logo.width) // 2, (img.height - logo.height) // 2), mask=logo)
                    img.save(f'{handled_folder}/{i}.jpg', quality=QUALITY)
                    handled_count += 1
                except OSError as e:
                    print(e)
                    return
        print(f'*** {folder} finished. Handled - {handled_count} photo ***')


if __name__ == '__main__':
    resize_and_watermark()
