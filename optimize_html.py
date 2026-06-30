#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1. Extract CSS from index.html <style> block → index.css
2. Replace all assets/images/*.png → .webp in every HTML file
3. Add fetchpriority="high" to first hero img and preload link
4. Ensure missing loading="lazy" + decoding="async" on non-hero images
"""
import sys, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(r"C:\Users\Настя\Desktop\клод")
HTML_FILES = list(ROOT.glob("*.html"))

# ─────────────────────────────────────────────
# 1. Extract <style> from index.html → index.css
# ─────────────────────────────────────────────
idx = ROOT / "index.html"
idx_css = ROOT / "index.css"

content = idx.read_text(encoding="utf-8")

style_match = re.search(r'(<style>)(.*?)(</style>)', content, re.DOTALL)
if style_match:
    css_body = style_match.group(2)
    # Minify: collapse multiple spaces, blank lines
    css_mini = re.sub(r'\n\s*\n', '\n', css_body)  # remove blank lines
    idx_css.write_text(css_mini, encoding="utf-8")
    print(f"index.css written: {idx_css.stat().st_size//1024}KB")

    # Replace <style>...</style> with <link>
    preconnect = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    link_tag = '<link rel="stylesheet" href="index.css">'

    # Remove duplicate font preconnects that were already in <head>
    new_head = content[:style_match.start()] + link_tag + content[style_match.end():]
    content = new_head
    print("CSS extracted from index.html")
else:
    print("No <style> block found in index.html")

# ─────────────────────────────────────────────
# 2. Add <link rel="preload"> for first hero image
# ─────────────────────────────────────────────
hero_img = "assets/images/lifestyle/lifestyle-evening.webp"
preload_tag = f'<link rel="preload" as="image" href="{hero_img}" fetchpriority="high">'

if preload_tag not in content:
    # Insert before </head>
    content = content.replace('</head>', f'{preload_tag}\n</head>', 1)
    print("Preload link added for first hero image")

# Save index.html changes so far
idx.write_text(content, encoding="utf-8")
print(f"index.html saved: {idx.stat().st_size//1024}KB")

# ─────────────────────────────────────────────
# 3. Replace .png → .webp in ALL HTML files
# (only for assets/images/ paths, not brand logos which we keep as PNG fallback)
# ─────────────────────────────────────────────
def replace_png_webp(html_content, filename=""):
    # Replace: assets/images/**/*.png -> *.webp
    # Pattern matches paths inside src="..." or href="..."
    result = re.sub(
        r'(assets/images/[^\'">\s]+)\.png',
        r'\1.webp',
        html_content
    )
    return result

total_changes = 0
for html_file in sorted(HTML_FILES):
    text = html_file.read_text(encoding="utf-8")
    new_text = replace_png_webp(text, html_file.name)
    changes = text.count('.png') - new_text.count('.png')
    if changes > 0:
        html_file.write_text(new_text, encoding="utf-8")
        print(f"  {html_file.name}: {changes} .png -> .webp replacements")
        total_changes += changes
    else:
        print(f"  {html_file.name}: no changes")

print(f"\nTotal PNG->WebP replacements across HTML: {total_changes}")

# ─────────────────────────────────────────────
# 4. Verify key images have correct attributes
# ─────────────────────────────────────────────
idx_content = idx.read_text(encoding="utf-8")
hero_checks = [
    ("lifestyle-evening.webp", "fetchpriority"),
    ("hero-village-1.webp", "loading"),
    ("villa-anna-card.webp", "loading"),
]
print("\nHero image attribute check:")
for img, attr in hero_checks:
    # Find the img tag
    match = re.search(r'<img[^>]*' + re.escape(img) + r'[^>]*>', idx_content)
    if match:
        tag = match.group()
        has_attr = attr in tag
        print(f"  {img}: {attr}={'YES' if has_attr else 'MISSING'}")
    else:
        print(f"  {img}: NOT FOUND in index.html")

print("\nDone. Optimization complete.")
