#!/usr/bin/env bash
source .venv/bin/activate
#python gallery_handler.py --ext webp --quality 40 --keep_name --watermark --resize 800 600 --exif
python gallery_handler.py --ext webp --quality 80 --keep_name --resize 600 --exif --watermark
$SHELL
