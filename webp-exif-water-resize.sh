#!/usr/bin/env bash
poetry run python gallery_handler.py --ext webp --quality 80 --keep_name --resize 800 --exif --watermark
#python gallery_handler.py --ext webp --quality 40 --keep_name --watermark --resize 800 600 --exif

$SHELL
