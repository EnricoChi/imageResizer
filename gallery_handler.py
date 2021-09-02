import os
from PIL import Image, ExifTags
from settings import LOGO_PATH, ROOT, HANDLED, ORIENTATION_ANGLE, RESIZE, Size, QUALITY
from utils import ProgressBar

BASE_LOGO = Image.open(LOGO_PATH)


def resize_and_watermark():
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
                        if hasattr(img, '_getexif'):
                            exif = img._getexif()
                            if exif:
                                orientation = next(
                                    (tag for tag, label in ExifTags.TAGS.items() if label == 'Orientation'), None)

                                if orientation in exif and exif[orientation] in ORIENTATION_ANGLE:
                                    img = img.rotate(ORIENTATION_ANGLE[exif[orientation]], expand=True)

                        img = img.convert('RGB')
                        img.width <= RESIZE.width or img.thumbnail(RESIZE, Image.ANTIALIAS)

                        # Ресайзим лого по ширине, если оно больше чем само изображение
                        logo = BASE_LOGO.copy()
                        logo.width < img.width or logo.thumbnail(Size(img.width - 50, logo.height), Image.ANTIALIAS)

                        img.paste(logo, ((img.width - logo.width) // 2, (img.height - logo.height) // 2), mask=logo)
                        img.save(f'{handled_folder}/{i}.jpg', quality=QUALITY)
                    except OSError as e:
                        print(e)
                        return
                bar.next()


if __name__ == '__main__':
    resize_and_watermark()
