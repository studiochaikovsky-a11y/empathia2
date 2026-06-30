#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from pathlib import Path
from PIL import Image

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Allow very large images (phone photos can be 100MP+)
Image.MAX_IMAGE_PIXELS = None

BASE = Path(r"C:\Users\Настя\Desktop\клод\assets\images")
MAX_WIDTH = 1920
JPEG_Q = 75
WEBP_Q = 82

saved_total = 0
count = 0
errors = []

def compress_jpeg(path):
    global saved_total, count
    orig = path.stat().st_size
    try:
        with Image.open(path) as img:
            img = img.convert("RGB")
            w, h = img.size
            if w > MAX_WIDTH:
                new_w = MAX_WIDTH
                new_h = int(h * MAX_WIDTH / w)
                img = img.resize((new_w, new_h), Image.LANCZOS)
                new_dims = f" ({w}x{h} -> {new_w}x{new_h})"
            else:
                new_dims = ""
            img.save(path, "JPEG", quality=JPEG_Q, optimize=True, progressive=True)
        new = path.stat().st_size
        saved = orig - new
        saved_total += saved
        count += 1
        print(f"  JPEG {orig//1024}KB -> {new//1024}KB (-{saved//1024}KB){new_dims}  {path.name}")
    except Exception as e:
        errors.append(f"{path.name}: {e}")
        print(f"  SKIP {path.name}: {e}")

def compress_png(path):
    global saved_total, count
    orig = path.stat().st_size
    webp_path = path.with_suffix(".webp")
    try:
        with Image.open(path) as img:
            w, h = img.size
            if w > MAX_WIDTH:
                new_w = MAX_WIDTH
                new_h = int(h * MAX_WIDTH / w)
                img = img.resize((new_w, new_h), Image.LANCZOS)
            # Check alpha
            has_alpha = img.mode in ("RGBA", "LA")
            if not has_alpha:
                img = img.convert("RGB")
            img.save(webp_path, "WEBP", quality=WEBP_Q, method=6)
        webp_size = webp_path.stat().st_size
        saved = orig - webp_size
        saved_total += saved
        count += 1
        print(f"  PNG  {orig//1024}KB  +WebP->{webp_size//1024}KB (-{saved//1024}KB)  {path.name}")
    except Exception as e:
        errors.append(f"{path.name}: {e}")
        print(f"  SKIP {path.name}: {e}")

print("=== Empathia Village - Image Compression ===")
print()

for f in sorted(BASE.rglob("*")):
    if not f.is_file():
        continue
    ext = f.suffix.lower()
    if ext in (".jpg", ".jpeg"):
        compress_jpeg(f)
    elif ext == ".png":
        compress_png(f)

print()
print(f"Done: {count} files processed")
print(f"Space saved: ~{saved_total//1024//1024} MB")
if errors:
    print(f"Errors: {len(errors)}")
    for e in errors:
        print(f"  {e}")
