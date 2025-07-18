import os

import click
from PIL import Image, ExifTags

from settings import LOGO_PATH, ROOT, HANDLED, ORIENTATION_ANGLE, QUALITY, EXTENSIONS
from utils import ProgressBar

BASE_LOGO = Image.open(LOGO_PATH)
EXT_LIST_FOR_SKIP = ('docx', 'doc', 'txt', 'pdf')


@click.command()
@click.option('--keep_name', is_flag=True, help='Keep image name')
@click.option('--quality', default=QUALITY, help='Image quality')
@click.option('--exif', is_flag=True, help='Exif tags normalize')
@click.option('--resize', type=int, default=800, help='Resize img')
@click.option('--crop', type=int, default=[330, 220], help='Crop img', multiple=True)
@click.option('--watermark', is_flag=True, help='Add watermark to image')
@click.option('--ext', type=click.Choice(EXTENSIONS.keys(), case_sensitive=True), help='Image extensions')
def handle_image(ext, watermark, crop, resize, exif, quality, keep_name):
    for folder in os.listdir(ROOT):
        image_folder = f'{ROOT}{folder}/'
        handled_folder = f'{image_folder}{HANDLED}/'
        os.path.exists(handled_folder) or os.makedirs(handled_folder)
        address, _, file_list = next(os.walk(image_folder))
        with ProgressBar(folder, max=len(file_list)) as bar:
            for i, file in enumerate(file_list):
                if not any([file.endswith(ext) for ext in EXT_LIST_FOR_SKIP]):
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

                        if crop:
                            img = crop_to_fit(img, crop)

                        if watermark:
                            img = img_add_watermark(img)
                        file_name = file.split('.')[0] if keep_name else i
                        img_convert(img, handled_folder, file_name, ext, quality)
                    except OSError as e:
                        print(e)
                        return
                bar.next()

def crop_to_fit(img, target_size):
    target_w, target_h = target_size
    img_ratio = img.width / img.height
    target_ratio = target_w / target_h

    # Масштабируем изображение
    if img_ratio > target_ratio:
        scale = target_h / img.height
    else:
        scale = target_w / img.width

    new_size = (int(img.width * scale), int(img.height * scale))
    img = img.resize(new_size, Image.ANTIALIAS)

    # Центрируем и обрезаем
    left = (img.width - target_w) // 2
    top = (img.height - target_h) // 2
    right = left + target_w
    bottom = top + target_h
    img = img.crop((left, top, right, bottom))
    return img

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
