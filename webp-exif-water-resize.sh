#!/usr/bin/env bash
source .venv/bin/activate
#python gallery_handler.py --ext webp --quality 40 --keep_name --watermark
python gallery_handler.py --ext webp --quality 80 --resize --exif --keep_name

$SHELL