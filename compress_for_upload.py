#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
Image.MAX_IMAGE_PIXELS = None

SRC = Path(r"C:\Users\Настя\Desktop\клод")
OUT = SRC / "optimized"
OUT.mkdir(exist_ok=True)

MAX_WIDTH = 1920
JPEG_Q = 80

saved_total = 0
count = 0
skipped = []

for f in sorted(SRC.iterdir()):
    if not f.is_file():
        continue
    ext = f.suffix.lower()
    if ext not in ('.jpg', '.jpeg', '.png'):
        continue

    orig_size = f.stat().st_size
    out_path = OUT / f.name

    try:
        with Image.open(f) as img:
            w, h = img.size
            if w > MAX_WIDTH:
                new_h = int(h * MAX_WIDTH / w)
                img = img.resize((MAX_WIDTH, new_h), Image.LANCZOS)

            if ext in ('.jpg', '.jpeg'):
                img = img.convert("RGB")
                img.save(out_path, "JPEG", quality=JPEG_Q, optimize=True, progressive=True)
            else:
                if img.mode not in ('RGBA', 'LA', 'P'):
                    img = img.convert("RGB")
                img.save(out_path, "PNG", optimize=True)

        new_size = out_path.stat().st_size
        saved = orig_size - new_size
        saved_total += saved
        count += 1
        print(f"  {orig_size//1024:>6}KB -> {new_size//1024:>5}KB  {f.name}")

    except Exception as e:
        skipped.append(f.name)
        print(f"  SKIP {f.name}: {e}")

print(f"\nГотово: {count} файлов")
print(f"Сэкономлено: ~{saved_total//1024//1024} МБ")
print(f"Оптимизированные файлы в: {OUT}")
if skipped:
    print(f"Пропущено: {skipped}")
