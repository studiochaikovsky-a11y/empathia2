# -*- coding: utf-8 -*-
"""Generate the Empathia Village agent sales brochure (A4, 4 pages)."""
import io
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

W, H = A4  # 595.27 x 841.89

INK = HexColor('#0B0C0D')
SURFACE = HexColor('#141517')
GOLD = HexColor('#C8A96E')
WHITE = HexColor('#FFFFFF')
MUT = HexColor('#9A9C9E')
DIM = HexColor('#6E7072')

SITE = 'empathia-seychelles.com'
PHONE = '+248 271 51 02'
EMAIL = 'info@empathia-seychelles.com'

def img_reader(path, crop_ratio=None):
    """Open image (any format PIL knows), optionally center-crop to ratio w/h."""
    im = Image.open(path).convert('RGB')
    if crop_ratio:
        w, h = im.size
        target = crop_ratio
        if w / h > target:
            nw = int(h * target)
            x = (w - nw) // 2
            im = im.crop((x, 0, x + nw, h))
        else:
            nh = int(w / target)
            y = (h - nh) // 2
            im = im.crop((0, y, w, y + nh))
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=88)
    buf.seek(0)
    return ImageReader(buf)

def logo_reader():
    im = Image.open('assets/images/brand/logo-emblem.webp').convert('RGBA')
    buf = io.BytesIO()
    im.save(buf, 'PNG')
    buf.seek(0)
    return ImageReader(buf)

def spaced(c, x, y, text, font='Helvetica', size=8, color=GOLD, track=2.2, center=False):
    c.setFont(font, size)
    c.setFillColor(color)
    t = c.beginText()
    if center:
        total = c.stringWidth(text, font, size) + track * (len(text) - 1)
        x = x - total / 2
    t.setTextOrigin(x, y)
    t.setCharSpace(track)
    t.textOut(text)
    t.setCharSpace(0)  # Tc persists in the page graphics state — reset it
    c.drawText(t)

def wrap_text(c, text, font, size, max_w):
    words = text.split()
    lines, cur = [], ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if c.stringWidth(test, font, size) <= max_w:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(c, x, y, text, font='Helvetica', size=9.5, leading=15.5, color=MUT, max_w=460):
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrap_text(c, text, font, size, max_w):
        c.drawString(x, y, line)
        y -= leading
    return y

def page_bg(c):
    c.setFillColor(INK)
    c.rect(0, 0, W, H, stroke=0, fill=1)

def footer(c, page_no):
    c.setStrokeColor(HexColor('#2A2C2E'))
    c.setLineWidth(0.5)
    c.line(48, 42, W - 48, 42)
    spaced(c, 48, 30, 'EMPATHIA VILLAGE', size=6.5, color=DIM, track=2)
    spaced(c, W - 48 - 150, 30, f'{SITE}  ·  {page_no}', size=6.5, color=DIM, track=1.2)

# ════════════════════════ PAGE 1 — COVER ════════════════════════
c = canvas.Canvas('empathia-village-agent-brochure.pdf', pagesize=A4)
c.setTitle('Empathia Village — Agent Sales Pack')
c.setAuthor('Empathia Village · Kensington Construction & Development')

page_bg(c)
hero_h = 400
c.drawImage(img_reader('assets/images/project/hero-village-1.jpg', crop_ratio=W / hero_h),
            0, H - hero_h, width=W, height=hero_h)
# soft dark fade at the bottom edge of the photo
c.setFillColor(INK)
c.setFillAlpha(0.55)
c.rect(0, H - hero_h, W, 60, stroke=0, fill=1)
c.setFillAlpha(1)

logo = logo_reader()
lw = 64
lh = lw * 975 / 574
c.drawImage(logo, W / 2 - lw / 2, H - hero_h - lh - 36, width=lw, height=lh, mask='auto')

y = H - hero_h - lh - 78
spaced(c, W / 2, y, 'EMPATHIA VILLAGE', size=24, color=WHITE, track=7, center=True)
y -= 26
c.setFont('Times-Italic', 13.5)
c.setFillColor(GOLD)
c.drawCentredString(W / 2, y, 'Private Luxury Residences · Baie Lazare · Mahé, Seychelles')
y -= 36
c.setStrokeColor(GOLD)
c.setLineWidth(0.7)
c.line(W / 2 - 26, y, W / 2 + 26, y)
y -= 30
spaced(c, W / 2, y, 'AGENT SALES PACK · 2026', size=9, color=MUT, track=3.5, center=True)

# key stats row
stats = [('30', 'AVAILABLE PLOTS'), ('FREEHOLD', 'FULL TITLE'), ('FROM $800,000', 'VILLA & LAND'), ('FROM 3%', 'AGENT COMMISSION')]
bw = (W - 96) / 4
sy = 96
c.setStrokeColor(HexColor('#3A3C3E'))
c.setLineWidth(0.5)
for i, (v, l) in enumerate(stats):
    x = 48 + i * bw
    c.line(x + 6, sy + 34, x + bw - 6, sy + 34)
    c.setFont('Times-Italic', 14)
    c.setFillColor(GOLD)
    c.drawCentredString(x + bw / 2, sy + 14, v)
    spaced(c, x + bw / 2, sy, l, size=5.8, color=DIM, track=1.6, center=True)
c.showPage()

# ════════════════════════ PAGE 2 — THE PROJECT ════════════════════════
page_bg(c)
spaced(c, 48, H - 64, 'THE PROJECT', size=8, color=GOLD, track=3)
c.setFont('Times-Italic', 24)
c.setFillColor(WHITE)
c.drawString(48, H - 94, 'A Private Village Above Baie Lazare')

y = H - 124
y = para(c, 48, y,
    'Empathia Village is a private estate of 30 available villa plots on the granite hillside above Baie Lazare. '
    'Adjacent plots can be combined for a larger private estate, subject to technical review and final documentation. '
    'The project is set on one of the most celebrated bays of the Indian Ocean, on the south-west coast of Mahé, Seychelles. '
    'The estate is positioned between the Four Seasons and Kempinski resorts, around 30 minutes from the '
    'international airport with direct connections to Europe, the Middle East and Asia.', max_w=500)
y -= 4
y = para(c, 48, y,
    'Following new Seychelles legislation that lifted the moratorium on foreign property ownership, '
    'international buyers receive full freehold title to both villa and land — transferable, inheritable '
    'and mortgageable, subject to the applicable approvals. Residency support is available, while eligibility '
    'is determined by the relevant Seychelles authorities for each buyer.', max_w=500)

# facts grid
facts = [
    ('30', 'Available plots'),
    ('600–2,000 m²', 'Plot sizes'),
    ('Freehold', 'Villa and land, full title'),
    ('From $800,000', 'Villa and plot'),
    ('2030', 'Estate completion'),
    ('Class 1', 'Licence valid through 2028'),
    ('USD · EUR · GBP', 'Payment currencies'),
    ('From 3%', 'Commission per completed client'),
]
gx, gy = 48, y - 30
colw = (W - 96) / 4
rowh = 64
for i, (v, l) in enumerate(facts):
    col, row = i % 4, i // 4
    x = gx + col * colw
    yy = gy - row * rowh
    c.setStrokeColor(HexColor('#C8A96E'))
    c.setLineWidth(0.6)
    c.setStrokeAlpha(0.45)
    c.line(x, yy + 24, x + colw - 14, yy + 24)
    c.setStrokeAlpha(1)
    c.setFont('Times-Italic', 12.5)
    c.setFillColor(GOLD)
    c.drawString(x, yy + 8, v)
    c.setFont('Helvetica', 6.6)
    c.setFillColor(MUT)
    c.drawString(x, yy - 4, l.upper())

y = gy - 2 * rowh - 18
spaced(c, 48, y, 'THE PRICE INCLUDES', size=8, color=GOLD, track=3)
y -= 20
includes = [
    'Land plot and freehold title',
    'Full villa construction and interior finishing',
    'Landscaping, garden and estate infrastructure',
    'Seychelles residency permit application',
    'Staged payments aligned with construction milestones',
    'Individual customisation of layout, size and plot available',
]
c.setFont('Helvetica', 9)
for item in includes:
    c.setFillColor(GOLD)
    c.drawString(48, y, '—')
    c.setFillColor(MUT)
    c.drawString(64, y, item)
    y -= 16.5

beach_h = 168
c.drawImage(img_reader('assets/images/location/baie-lazare-beach.jpg', crop_ratio=(W - 96) / beach_h),
            48, 62, width=W - 96, height=beach_h)
footer(c, '2')
c.showPage()

# ════════════════════════ PAGE 3 — THE RESIDENCES ════════════════════════
page_bg(c)
spaced(c, 48, H - 64, 'THE RESIDENCES', size=8, color=GOLD, track=3)
c.setFont('Times-Italic', 24)
c.setFillColor(WHITE)
c.drawString(48, H - 94, 'Three Villa Designs')

villas = [
    {
        'img': 'assets/images/villas/jane/villa-jane-il.jpg',
        'name': 'Villa Jane',
        'tag': 'SINGLE STOREY · GLAZED PAVILION',
        'specs': 'from 140 m² · 2 bedrooms · private pool · plot from 600 m²',
        'desc': 'A refined single-storey residence with panoramic floor-to-ceiling glazing framing the tropical landscape and the Indian Ocean. The entry point to the collection.',
        'price': 'From $800,000',
    },
    {
        'img': 'assets/images/villas/anna/villa-anna-il.jpg',
        'name': 'Villa Anna',
        'tag': 'TWO STOREYS · GARDEN & POOL',
        'specs': 'from 240 m² · 3 bedrooms · private pool · plot from 600 m²',
        'desc': 'An elegant two-storey residence designed for seamless indoor-outdoor living: open-plan living and dining, private pool and sun terrace.',
        'price': 'From $990,000',
    },
    {
        'img': 'assets/images/villas/georgette/villa-georgette-il.jpg',
        'name': 'Villa Georgette',
        'tag': 'SIGNATURE · THREE STOREYS · PANORAMIC TERRACES',
        'specs': 'from 350 m² · 4 bedrooms · private pool · plot from 1,500 m²',
        'desc': 'The flagship three-storey residence with wide panoramic terraces and a grand private pool, commanding unobstructed views of the Indian Ocean.',
        'price': 'From $2,100,000',
    },
]

by = H - 130
block_h = 212
for v in villas:
    img_h = 118
    c.drawImage(img_reader(v['img'], crop_ratio=(W - 96) / img_h), 48, by - img_h, width=W - 96, height=img_h)
    ty = by - img_h - 20
    c.setFont('Times-Italic', 17)
    c.setFillColor(WHITE)
    c.drawString(48, ty, v['name'])
    c.setFont('Times-Italic', 13)
    c.setFillColor(GOLD)
    c.drawRightString(W - 48, ty, v['price'])
    ty -= 13
    spaced(c, 48, ty, v['tag'], size=6.2, color=GOLD, track=1.8)
    ty -= 14
    c.setFont('Helvetica', 8.2)
    c.setFillColor(MUT)
    c.drawString(48, ty, v['specs'])
    ty -= 13
    c.setFont('Helvetica', 8.2)
    c.setFillColor(DIM)
    for line in wrap_text(c, v['desc'], 'Helvetica', 8.2, W - 96):
        c.drawString(48, ty, line)
        ty -= 11.5
    by -= block_h

c.setFont('Helvetica', 7.5)
c.setFillColor(DIM)
c.drawString(48, 56, 'Every residence can be individually adapted — house area, plot size, floor plan and finishes. Floor plans and full specifications available to registered agents.')
footer(c, '3')
c.showPage()

# ════════════════════════ PAGE 4 — AGENT PROGRAMME ════════════════════════
page_bg(c)
spaced(c, 48, H - 64, 'AGENT PROGRAMME', size=8, color=GOLD, track=3)
c.setFont('Times-Italic', 24)
c.setFillColor(WHITE)
c.drawString(48, H - 94, 'Partner With Empathia Village')

y = H - 122
y = para(c, 48, y,
    'We work with a curated network of real estate agents, wealth managers, relocation advisors and property '
    'consultants worldwide. The programme rewards quality introductions with competitive, transparent '
    'compensation — paid upon successful transaction completion.', max_w=500)

# commission box
bx, bw_, bh = 48, W - 96, 96
byy = y - bh - 6
c.setFillColor(SURFACE)
c.rect(bx, byy, bw_, bh, stroke=0, fill=1)
c.setStrokeColor(GOLD)
c.setLineWidth(1)
c.line(bx, byy, bx, byy + bh)
c.setFont('Times-Italic', 34)
c.setFillColor(GOLD)
c.drawString(bx + 28, byy + bh - 46, 'From 3%')
c.setFont('Helvetica', 8.5)
c.setFillColor(MUT)
c.drawString(bx + 28, byy + bh - 62, 'per introduced client who completes a purchase')
c.setFont('Times-Italic', 17)
c.setFillColor(WHITE)
c.drawRightString(bx + bw_ - 28, byy + bh - 46, 'Partner terms')
c.setFont('Helvetica', 8.5)
c.setFillColor(MUT)
c.drawRightString(bx + bw_ - 28, byy + bh - 62, 'rate and timing recorded in the agreement')

# benefits two columns
y = byy - 30
spaced(c, 48, y, 'WHAT REGISTERED AGENTS RECEIVE', size=8, color=GOLD, track=3)
y -= 22
benefits = [
    ('Marketing materials', 'Digital brochure, high-resolution renders, floor plans, pricing sheets and presentation decks.'),
    ('Discovery tour support', 'Private client visits to the estate, with accommodation arranged on Eden Island.'),
    ('Dedicated support', 'A named contact, fast response times and deal support throughout the transaction.'),
    ('Exclusive inventory access', 'Early notification of new plot releases and phase openings before public announcement.'),
    ('Investment documentation', 'Market analysis, rental yield projections and residency permit documentation.'),
    ('Transparent payment', 'Commission paid directly to your agency or personally on signed contract and payment receipt.'),
]
colw2 = (W - 96 - 24) / 2
rowh2 = 64
for i, (t, d) in enumerate(benefits):
    col, row = i % 2, i // 2
    x = 48 + col * (colw2 + 24)
    yy = y - row * rowh2
    c.setFont('Helvetica-Bold', 8.5)
    c.setFillColor(WHITE)
    c.drawString(x, yy, t.upper())
    c.setFont('Helvetica', 8)
    c.setFillColor(MUT)
    ly = yy - 13
    for line in wrap_text(c, d, 'Helvetica', 8, colw2):
        c.drawString(x, ly, line)
        ly -= 11
y = y - 3 * rowh2 - 8

# how it works
spaced(c, 48, y, 'HOW IT WORKS', size=8, color=GOLD, track=3)
y -= 20
steps = ['Register as an agent', 'Introduce your client', 'We run the sales process', 'Commission on completion']
sw = (W - 96) / 4
for i, s in enumerate(steps):
    x = 48 + i * sw
    c.setFont('Times-Italic', 13)
    c.setFillColor(GOLD)
    c.drawString(x, y, f'{i+1}.')
    c.setFont('Helvetica', 7.6)
    c.setFillColor(MUT)
    ly = y - 13
    for line in wrap_text(c, s, 'Helvetica', 7.6, sw - 16):
        c.drawString(x, ly, line)
        ly -= 10

# contacts
y -= 56
c.setFillColor(SURFACE)
c.rect(48, y - 64, W - 96, 76, stroke=0, fill=1)
spaced(c, 68, y - 8, 'CONTACT', size=7, color=GOLD, track=2.5)
c.setFont('Helvetica', 9.5)
c.setFillColor(WHITE)
c.drawString(68, y - 26, f'{PHONE}   ·   WhatsApp: wa.me/2482715102')
c.drawString(68, y - 42, EMAIL)
c.drawString(68, y - 58, f'https://{SITE}   ·   Instagram @seychelles.empathia')

c.setFont('Helvetica', 6.3)
c.setFillColor(DIM)
disc = ('Prices, floor plans, areas, images, purchase terms and any other information in this document are provided for general information purposes only and do not '
        'constitute a public offer. Current pricing, availability, specifications, payment terms and transaction procedure are confirmed individually upon request.')
ly = 68
for line in wrap_text(c, disc, 'Helvetica', 6.3, W - 96):
    c.drawString(48, ly, line)
    ly -= 8.5
footer(c, '4')
c.save()
print('OK: empathia-village-agent-brochure.pdf')
