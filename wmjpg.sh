#!/usr/bin/env bash
source .venv/bin/activate
python gallery_handler.py --ext jpg --quality 60 --resize --watermark --exif --keep_name

$SHELL