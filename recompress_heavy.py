#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recompress every image referenced by the site that is heavier than
THRESHOLD_KB. Regenerates WebP from the original PNG/JPG source when one
exists next to it. Heroes keep 1920px, the rest are capped at 1600px."""
import re
import sys
from pathlib import Path
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
Image.MAX_IMAGE_PIXELS = None

ROOT = Path(__file__).parent
THRESHOLD_KB = 250
WEBP_Q = 70

refs = set()
for hf in ROOT.glob("*.html"):
    refs.update(re.findall(r'src="([^"]+\.(?:webp|jpe?g|png))"', hf.read_text(encoding="utf-8")))

total_before = total_after = 0
for ref in sorted(refs):
    path = ROOT / ref
    if not path.exists():
        continue
    size_kb = path.stat().st_size // 1024
    if size_kb < THRESHOLD_KB:
        continue
    # prefer the uncompressed source if present
    source = None
    for ext in (".png", ".jpg", ".jpeg"):
        cand = path.with_suffix(ext)
        if cand.exists() and cand != path:
            source = cand
            break
    src_img = source or path
    max_w = 1920 if "hero" in path.name.lower() else 1600
    tmp = path.with_suffix(".tmp.webp")
    with Image.open(src_img) as img:
        img = img.convert("RGB")
        w, h = img.size
        if w > max_w:
            img = img.resize((max_w, int(h * max_w / w)), Image.LANCZOS)
        img.save(tmp, "WEBP", quality=WEBP_Q, method=6)
    new_kb = tmp.stat().st_size // 1024
    if new_kb < size_kb * 0.9:
        out = path.with_suffix(".webp")
        tmp.replace(out)
        total_before += size_kb
        total_after += new_kb
        note = f" (from {src_img.name})" if source else ""
        print(f"  {size_kb}KB -> {new_kb}KB  {ref}{note}")
    else:
        tmp.unlink()
        print(f"  keep ({size_kb}KB, new would be {new_kb}KB): {ref}")

print(f"\nTotal: {total_before}KB -> {total_after}KB "
      f"(saved {(total_before - total_after) // 1024} MB)")
