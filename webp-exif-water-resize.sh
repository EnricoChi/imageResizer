#!/usr/bin/env bash
source .venv/bin/activate
#python gallery_handler.py --ext webp --quality 40 --keep_name --watermark --resize --exif
python gallery_handler.py --ext webp --quality 100 --resize 1320 1320 --exif

$SHELL