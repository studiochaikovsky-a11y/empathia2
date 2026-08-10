from pathlib import Path
from io import BytesIO

from PIL import Image
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "Empathia_Village_Brochure_EN.pdf"
W, H = A4

INK = HexColor("#171918")
DEEP = HexColor("#123D35")
GOLD = HexColor("#C4A35A")
PAPER = HexColor("#F4F0E8")
MUTED = HexColor("#AAB0AB")
CHARCOAL = HexColor("#2A2D2B")


def prepared_image(path, max_edge=1800, quality=86):
    source = Image.open(ROOT / path)
    source.thumbnail((max_edge, max_edge), Image.Resampling.LANCZOS)
    if source.mode in ("RGBA", "LA"):
        background = Image.new("RGB", source.size, "white")
        background.paste(source, mask=source.getchannel("A"))
        source = background
    else:
        source = source.convert("RGB")
    buffer = BytesIO()
    source.save(buffer, "JPEG", quality=quality, optimize=True, progressive=True)
    buffer.seek(0)
    return ImageReader(buffer)


def cover_image(c, path):
    image = prepared_image(path, max_edge=1800, quality=88)
    iw, ih = image.getSize()
    scale = max(W / iw, H / ih)
    width, height = iw * scale, ih * scale
    c.drawImage(image, (W - width) / 2, (H - height) / 2, width, height, mask="auto")


def fit_image(c, path, x, y, width, height):
    image = prepared_image(path, max_edge=1400, quality=86)
    iw, ih = image.getSize()
    scale = min(width / iw, height / ih)
    rw, rh = iw * scale, ih * scale
    c.drawImage(image, x + (width - rw) / 2, y + (height - rh) / 2, rw, rh, mask="auto")


def wrap_lines(text, font, size, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = word if not current else current + " " + word
        if stringWidth(candidate, font, size) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paragraph(c, text, x, y, width, size=10, leading=15, color=MUTED, font="Helvetica"):
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrap_lines(text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


def label(c, text, x, y, color=GOLD):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(x, y, text.upper())


def footer(c, page):
    c.setStrokeColor(HexColor("#444A46"))
    c.setLineWidth(0.35)
    c.line(42, 28, W - 42, 28)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6.5)
    c.drawString(42, 16, "Empathia Village - Baie Lazare, Mahe, Seychelles")
    c.drawRightString(W - 42, 16, str(page))


def page_one(c):
    cover_image(c, "assets/images/project/hero-5-hero.webp")
    c.setFillColor(INK)
    c.setFillAlpha(0.62)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillAlpha(1)
    label(c, "Baie Lazare - Mahe - Seychelles", 48, H - 66)
    c.setFillColor(white)
    c.setFont("Times-Roman", 36)
    c.drawString(48, H - 122, "Empathia Village")
    c.setFont("Times-Italic", 22)
    c.drawString(48, H - 154, "Private living. Naturally yours.")
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(48, H - 176, 118, H - 176)
    c.setFillColor(white)
    c.setFont("Helvetica", 11)
    c.drawString(48, 108, "30 private freehold villa plots")
    c.drawString(48, 88, "Adjacent available plots can be combined")
    c.drawString(48, 68, "Villas from $990,000 - estate completion planned for 2030")
    c.showPage()


def page_two(c):
    c.setFillColor(INK)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    label(c, "The estate", 42, H - 48)
    c.setFillColor(white)
    c.setFont("Times-Roman", 27)
    c.drawString(42, H - 82, "A private hillside community")
    y = paragraph(c,
        "Empathia Village is set above Baie Lazare between Four Seasons Resort Seychelles and Kempinski Seychelles Resort. "
        "The current masterplan shows all 30 plots and their sale status. Neighbouring available plots can be combined to create a larger private estate, subject to technical review and final documentation.",
        42, H - 112, W - 84, 9.5, 14)
    image_y = 278
    image_h = y - image_y - 18
    c.setFillColor(PAPER)
    c.roundRect(42, image_y, W - 84, image_h, 5, stroke=0, fill=1)
    fit_image(c, "assets/images/project/masterplan.jpg", 48, image_y + 6, W - 96, image_h - 12)

    facts = [
        ("30", "private plots in the estate"),
        ("600-2,000 m2", "plot range"),
        ("Freehold", "villa and land, subject to approvals"),
        ("2030", "full estate completion planned"),
        ("2028", "Class I licence valid through"),
        ("2 min", "to Baie Lazare beach"),
    ]
    cols = 3
    cell_w = (W - 84) / cols
    for i, (value, description) in enumerate(facts):
        col, row = i % cols, i // cols
        x = 42 + col * cell_w
        top = 244 - row * 88
        c.setStrokeColor(HexColor("#3A3E3B"))
        c.line(x, top, x + cell_w - 14, top)
        c.setFillColor(GOLD)
        c.setFont("Times-Italic", 18)
        c.drawString(x, top - 26, value)
        paragraph(c, description, x, top - 44, cell_w - 16, 7.4, 10, MUTED)
    footer(c, 2)
    c.showPage()


def page_three(c):
    c.setFillColor(DEEP)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    label(c, "The residences", 42, H - 48)
    c.setFillColor(white)
    c.setFont("Times-Roman", 27)
    c.drawString(42, H - 82, "Three villa designs")
    villas = [
        ("Villa Jane", "From $990,000", "2 bedrooms - 1 floor - from 140 m2 - plot from 600 m2", "assets/images/villas/jane/villa-jane-card.webp"),
        ("Villa Anna", "From $1,500,000", "3 bedrooms - 2 floors - from 240 m2 - plot from 600 m2", "assets/images/villas/anna/villa-anna-card.webp"),
        ("Villa Georgette", "From $2,100,000", "4 bedrooms - 3 floors - from 350 m2 - plot from 1,500 m2", "assets/images/villas/georgette/villa-georgette-card.webp"),
    ]
    y = H - 126
    for name, price, specs, image in villas:
        h = 184
        c.setFillColor(CHARCOAL)
        c.roundRect(42, y - h, W - 84, h, 5, stroke=0, fill=1)
        fit_image(c, image, 48, y - h + 6, 164, h - 12)
        c.setFillColor(white)
        c.setFont("Times-Roman", 21)
        c.drawString(232, y - 42, name)
        c.setFillColor(GOLD)
        c.setFont("Times-Italic", 16)
        c.drawString(232, y - 70, price)
        paragraph(c, specs, 232, y - 98, W - 290, 8.7, 13, MUTED)
        paragraph(c, "Private pool, tropical indoor-outdoor living and individual adaptations subject to technical review.", 232, y - 128, W - 290, 8, 12, MUTED)
        y -= h + 16
    footer(c, 3)
    c.showPage()


def page_four(c):
    c.setFillColor(INK)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    label(c, "Delivery and due diligence", 42, H - 48)
    c.setFillColor(white)
    c.setFont("Times-Roman", 27)
    c.drawString(42, H - 82, "Built by a licensed developer")
    y = paragraph(c,
        "Kensington Construction & Development holds Seychelles Class I Building Contractor licence No. 322704, valid through 2028, and presents more than 30 years of international construction experience. Phase I foundation works are underway and completion of the full estate is planned for 2030.",
        42, H - 114, W - 84, 9.5, 14)
    fit_image(c, "assets/images/brand/kensington-license.webp", 42, 360, 196, y - 386)

    x = 264
    label(c, "Included", x, y - 12)
    included = ["Private plot and title support", "Selected villa construction", "Interior finishing", "Private pool and terrace", "Landscaping and estate infrastructure"]
    iy = y - 42
    for item in included:
        c.setFillColor(GOLD)
        c.circle(x + 3, iy + 3, 2, stroke=0, fill=1)
        c.setFillColor(white)
        c.setFont("Helvetica", 8.5)
        c.drawString(x + 14, iy, item)
        iy -= 25

    label(c, "Location", x, iy - 10)
    iy = paragraph(c, "Baie Lazare, Mahe - about 2 minutes to the beach and around 30 minutes by car to Seychelles International Airport.", x, iy - 34, W - x - 42, 8.5, 13, MUTED)

    c.setFillColor(DEEP)
    c.roundRect(42, 88, W - 84, 226, 6, stroke=0, fill=1)
    label(c, "Request current details", 66, 282)
    c.setFillColor(white)
    c.setFont("Times-Roman", 24)
    c.drawString(66, 246, "Price list, plots and plans")
    paragraph(c, "Prices, specifications and purchase terms are confirmed individually and do not constitute a public offer. Residency support is available, but eligibility is subject to approval by the relevant Seychelles authorities. Rental scenarios are indicative and not guaranteed.", 66, 216, W - 132, 8.5, 13, HexColor("#CFD8D3"))
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(66, 132, "info@empathia-seychelles.com")
    c.drawString(66, 112, "+248 271 51 02 - WhatsApp available")
    footer(c, 4)
    c.showPage()


def main():
    c = canvas.Canvas(str(OUTPUT), pagesize=A4)
    c.setTitle("Empathia Village - Project Brochure")
    c.setAuthor("Empathia Village")
    page_one(c)
    page_two(c)
    page_three(c)
    page_four(c)
    c.save()
    print(f"Created {OUTPUT.name}")


if __name__ == "__main__":
    main()
