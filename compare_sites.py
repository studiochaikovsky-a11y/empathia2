import os, re

with open("C:/Users/Настя/Desktop/empathia-ru/index.html", encoding="utf-8") as f:
    ru = f.read()
with open("C:/Users/Настя/Desktop/клод/index.html", encoding="utf-8") as f:
    en = f.read()

ru_dir = "C:/Users/Настя/Desktop/empathia-ru"
en_dir = "C:/Users/Настя/Desktop/клод"

ru_pages = set(f for f in os.listdir(ru_dir) if f.endswith(".html") and f != "index.html")
en_pages = set(f for f in os.listdir(en_dir) if f.endswith(".html") and f != "index.html")
print("EN страницы которых нет в RU:", sorted(en_pages - ru_pages))
print("RU страницы которых нет в EN:", sorted(ru_pages - en_pages))
print()
print("topbar в RU:", "ЕСТЬ" if 'id="topbar"' in ru else "ОТСУТСТВУЕТ")
print()
en_prices = re.findall(r'\$[\d,]+', en)
ru_prices = re.findall(r'\$[\d,]+', ru)
print("EN цены:", sorted(set(en_prices)))
print("RU цены:", sorted(set(ru_prices)))
print()
# Check sections
en_secs = re.findall(r'<section[^>]*id="([^"]+)"', en)
ru_secs = re.findall(r'<section[^>]*id="([^"]+)"', ru)
ru_set = set(ru_secs)
print("EN секции отсутствующие в RU:", [s for s in en_secs if s not in ru_set])
