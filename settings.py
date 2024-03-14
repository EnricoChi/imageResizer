from collections import namedtuple

ROOT = 'photo/'
HANDLED = 'handled/'
LOGO_PATH = 'logo.png'


# Size = namedtuple('Size', ('width', 'height'))
# RESIZE = Size(800, 600)
QUALITY = 60

ORIENTATION_ANGLE = {
    3: 180,
    6: 270,
    8: 90
}

EXTENSIONS = {
    'jpg': {'mode': 'RGB'},
    'webp': {'mode': 'RGBA'},
}
