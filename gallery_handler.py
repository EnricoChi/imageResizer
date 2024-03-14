import os

import click
from PIL import Image, ExifTags

from settings import LOGO_PATH, ROOT, HANDLED, ORIENTATION_ANGLE, QUALITY, EXTENSIONS
from utils import ProgressBar

BASE_LOGO = Image.open(LOGO_PATH)


@click.command()
@click.option('--keep_name', is_flag=True, help='Keep image name')
@click.option('--quality', default=QUALITY, help='Image quality')
@click.option('--exif', is_flag=True, help='Exif tags normalize')
@click.option('--resize', type=int, default=800, help='Resize img')
@click.option('--watermark', is_flag=True, help='Add watermark to image')
@click.option('--ext', type=click.Choice(EXTENSIONS.keys(), case_sensitive=True), help='Image extensions')
def handle_image(ext, watermark, resize, exif, quality, keep_name):
    for folder in os.listdir(ROOT):
        image_folder = f'{ROOT}{folder}/'
        handled_folder = f'{image_folder}{HANDLED}/'
        os.path.exists(handled_folder) or os.makedirs(handled_folder)
        address, _, file_list = next(os.walk(image_folder))
        with ProgressBar(folder, max=len(file_list)) as bar:
            for i, file in enumerate(file_list):

                if not file.endswith('.docx'):
                    try:
                        img = Image.open(f'{address}/{file}')

                        # Убираем неправильный поворот изображения
                        if exif:
                            img = exif_fix(img)

                        img = img.convert(EXTENSIONS[ext]['mode'])

                        if resize:
                            # height, width = resize
                            # resize = Size(height, width)
                            max(img.width, img.height) <= resize or img.thumbnail([resize, resize], Image.ANTIALIAS)

                        if watermark:
                            img = img_add_watermark(img)
                        file_name = file.split('.')[0] if keep_name else i
                        img_convert(img, handled_folder, file_name, ext, quality)
                    except OSError as e:
                        print(e)
                        return
                bar.next()


def exif_fix(img):
    if hasattr(img, '_getexif'):
        exif = img._getexif()
        if exif:
            orientation = next(
                (tag for tag, label in ExifTags.TAGS.items() if label == 'Orientation'), None)

            if orientation in exif and exif[orientation] in ORIENTATION_ANGLE:
                img = img.rotate(ORIENTATION_ANGLE[exif[orientation]], expand=True)
    return img


def img_add_watermark(img):
    logo = BASE_LOGO.copy()

    # Ресайзим лого по ширине, если оно больше чем само изображение
    logo.width < img.width or logo.thumbnail([img.width - 50, logo.height], Image.ANTIALIAS)

    img.paste(logo, ((img.width - logo.width) // 2, (img.height - logo.height) // 2), mask=logo)

    return img


def img_convert(img, handled_folder, i, ext, quality):
    img.save(f'{handled_folder}/{i}.{ext}', quality=quality)


if __name__ == '__main__':
    handle_image()
