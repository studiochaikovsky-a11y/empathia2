#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert JPGs referenced by the site to WebP and update HTML refs.
Keeps the WebP only when it is actually smaller than the JPG."""
import re
import sys
from pathlib import Path
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
Image.MAX_IMAGE_PIXELS = None

ROOT = Path(__file__).parent
MAX_WIDTH = 1920
WEBP_Q = 80

html_files = sorted(ROOT.glob("*.html"))

# 1. Collect all .jpg/.jpeg src refs from HTML
jpg_refs = set()
for hf in html_files:
    text = hf.read_text(encoding="utf-8")
    jpg_refs.update(re.findall(r'src="([^"]+\.jpe?g)"', text))

mapping = {}  # old ref -> new ref
for ref in sorted(jpg_refs):
    src = ROOT / ref
    if not src.exists():
        print(f"  MISSING on disk, skip: {ref}")
        continue
    dst = src.with_suffix(".webp")
    orig_kb = src.stat().st_size // 1024
    if not dst.exists():
        with Image.open(src) as img:
            img = img.convert("RGB")
            w, h = img.size
            if w > MAX_WIDTH:
                img = img.resize((MAX_WIDTH, int(h * MAX_WIDTH / w)), Image.LANCZOS)
            img.save(dst, "WEBP", quality=WEBP_Q, method=6)
    new_kb = dst.stat().st_size // 1024
    if new_kb < orig_kb:
        mapping[ref] = ref.rsplit(".", 1)[0] + ".webp"
        print(f"  {orig_kb}KB -> {new_kb}KB  {ref}")
    else:
        print(f"  KEEP JPG ({orig_kb}KB <= webp {new_kb}KB): {ref}")

# 2. Rewrite src refs in HTML
for hf in html_files:
    text = hf.read_text(encoding="utf-8")
    orig = text
    for old, new in mapping.items():
        text = text.replace(f'src="{old}"', f'src="{new}"')
    if text != orig:
        hf.write_text(text, encoding="utf-8")
        print(f"  updated refs: {hf.name}")

print(f"\nConverted {len(mapping)} of {len(jpg_refs)} referenced JPGs")
