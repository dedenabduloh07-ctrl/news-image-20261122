#!/usr/bin/env python3
"""Draw the 22 November 2026 world-news front page (1024x1024 PNG).

Generator script only - NOT part of the entry. The entry ships entry.png
plus a stdlib-only main.py that copies it to /output.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (251, 246, 233)
PAPER = (255, 255, 255)
INK = (17, 17, 17)
RED = (176, 30, 36)
NAVY = (31, 58, 95)
GREY = (90, 86, 76)
LIGHT_BLUE = (220, 233, 245)
ORANGE = (214, 110, 30)
BORDER = (216, 205, 178)

F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def center_text(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- icons
def icon_globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=LIGHT_BLUE,
              outline=NAVY, width=4)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=NAVY, width=2)
    d.line([cx - r, cy, cx + r, cy], fill=NAVY, width=2)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
          start=200, end=340, fill=NAVY, width=2)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
          start=20, end=160, fill=NAVY, width=2)
    # red crack: no-deal zigzag
    pts = [(cx - r * 0.55, cy - r * 0.75), (cx - r * 0.15, cy - r * 0.25),
           (cx - r * 0.45, cy + r * 0.15), (cx + r * 0.05, cy + r * 0.55),
           (cx - r * 0.1, cy + r * 0.85)]
    d.line(pts, fill=RED, width=5, joint="curve")


def icon_ship(d, x, y, s):
    # s = box size; ship hull + mast + explosion star
    d.polygon([(x + 6, y + s * 0.62), (x + s - 6, y + s * 0.62),
               (x + s - 16, y + s * 0.85), (x + 16, y + s * 0.85)],
              fill=NAVY)
    d.rectangle([x + s * 0.42, y + s * 0.30, x + s * 0.58, y + s * 0.62],
                fill=NAVY)
    d.line([x + s * 0.5, y + s * 0.12, x + s * 0.5, y + s * 0.30],
           fill=NAVY, width=3)
    d.arc([x, y + s * 0.82, x + s * 0.5, y + s * 1.02], 180, 360, fill=NAVY, width=3)
    d.arc([x + s * 0.5, y + s * 0.82, x + s, y + s * 1.02], 180, 360, fill=NAVY, width=3)
    # explosion star
    cx, cy, r = x + s * 0.78, y + s * 0.22, s * 0.20
    pts = []
    for i in range(12):
        ang = math.pi * i / 6
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=ORANGE)


def icon_flame(d, x, y, s):
    cx = x + s / 2
    pts = [(cx, y + 4),
           (cx + s * 0.34, y + s * 0.42), (cx + s * 0.22, y + s * 0.42),
           (cx + s * 0.38, y + s * 0.78), (cx - s * 0.38, y + s * 0.78),
           (cx - s * 0.22, y + s * 0.42), (cx - s * 0.34, y + s * 0.42)]
    d.polygon(pts, fill=ORANGE)
    d.ellipse([cx - s * 0.14, y + s * 0.52, cx + s * 0.14, y + s * 0.78],
              fill=RED)


def icon_building(d, x, y, s):
    d.rectangle([x + s * 0.18, y + s * 0.14, x + s * 0.82, y + s * 0.92],
                outline=NAVY, width=3, fill=PAPER)
    for r in range(3):
        for c in range(3):
            wx = x + s * (0.28 + c * 0.22)
            wy = y + s * (0.24 + r * 0.22)
            d.rectangle([wx, wy, wx + s * 0.12, wy + s * 0.12], fill=NAVY)
    d.line([(x + s * 0.55, y + s * 0.14), (x + s * 0.45, y + s * 0.45),
            (x + s * 0.62, y + s * 0.68), (x + s * 0.5, y + s * 0.92)],
           fill=RED, width=4, joint="curve")


def icon_badge(d, x, y, s):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.44
    pts = []
    for i in range(10):
        ang = math.pi * i / 5 - math.pi / 2
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=NAVY)
    d.ellipse([cx - s * 0.16, cy - s * 0.16, cx + s * 0.16, cy + s * 0.16],
              fill=CREAM)
    d.ellipse([cx - s * 0.07, cy - s * 0.07, cx + s * 0.07, cy + s * 0.07],
              fill=RED)


def icon_chart(d, x, y, s):
    d.line([x + 6, y + s * 0.15, x + 6, y + s * 0.88], fill=NAVY, width=3)
    d.line([x + 6, y + s * 0.88, x + s - 6, y + s * 0.88], fill=NAVY, width=3)
    pts = [(x + 12, y + s * 0.28), (x + s * 0.35, y + s * 0.42),
           (x + s * 0.55, y + s * 0.34), (x + s - 12, y + s * 0.72)]
    d.line(pts, fill=RED, width=5, joint="curve")
    d.polygon([(x + s - 12, y + s * 0.72), (x + s - 26, y + s * 0.62),
               (x + s - 24, y + s * 0.80)], fill=RED)


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # double outer border
    d.rectangle([18, 18, W - 19, H - 19], outline=INK, width=3)
    d.rectangle([26, 26, W - 27, H - 27], outline=INK, width=1)

    # masthead
    f_mast = font(F_SERIF_B, 64)
    center_text(d, W // 2, 40, "THE WORLD TODAY", f_mast, INK)
    d.line([60, 118, W - 60, 118], fill=INK, width=2)

    # date - big and unmissable
    f_date = font(F_SANS_B, 37)
    center_text(d, W // 2, 128, "SUNDAY 22 NOVEMBER 2026", f_date, RED)

    f_tag = font(F_SERIF, 18)
    center_text(d, W // 2, 172, "World news in one image  —  the day in brief",
                f_tag, GREY)

    d.line([36, 200, W - 36, 200], fill=INK, width=3)
    d.line([36, 206, W - 36, 206], fill=INK, width=1)

    # ---------------- main story: COP31 ----------------
    icon_globe(d, 168, 322, 92)
    d.text((300, 216), "CLIMATE  ·  COP31  ·  ANTALYA, TURKEY",
           font=font(F_SANS_B, 19), fill=RED)
    f_head = font(F_SERIF_B, 45)
    y = 244
    y = draw_lines(d, 300, y,
                   wrap(d, "COP31 climate talks collapse", f_head, 660),
                   f_head, INK, 52)
    f_body = font(F_SANS, 21)
    summary = ("UN climate summit ends with no deal after countries "
               "fail to agree on fossil fuels and climate finance. "
               "The EU rejects a final text that never names fossil fuels.")
    y = draw_lines(d, 300, y + 8,
                   wrap(d, summary, f_body, 660), f_body, INK, 28)

    d.line([36, 452, W - 36, 452], fill=INK, width=2)

    # ---------------- supporting grid: 2 x 3 ----------------
    stories = [
        ("UKRAINE WAR", "Sea drone hits Russian warship",
         "Ukraine is reported to have struck a Russian warship in "
         "Benghazi port, Libya; a second ship was also hit.", icon_ship),
        ("MIDDLE EAST", "Iran strikes Bahrain and tanker",
         "Iran hits a civilian plant in Sitra, Bahrain — two hurt — "
         "and a tanker near Hormuz; a US base is also attacked.", icon_flame),
        ("UKRAINE WAR", "Missiles hit Zelenskyy's home city",
         "Russian missiles kill two, including a 7-year-old, in "
         "Kryvyi Rih and wound 60; flats near Kyiv partly collapse, "
         "three dead.", icon_building),
        ("MEXICO", "Cartel boss 'El Chapo Isidro' captured",
         "Mexican special forces seize Fausto Isidro Meza Flores in "
         "Sinaloa; 11 die in the gun battle.", icon_badge),
        ("INDONESIA", "Candy factory fire kills three",
         "A blaze at a factory in Cikande, Banten, leaves three dead "
         "and dozens missing; 36 are still sought.", icon_flame),
        ("MARKETS", "Stocks plunge as AI sell-off spreads",
         "The S&P 500 falls 3.7% and the Nasdaq 5.3%; the rout "
         "reaches Japan and South Korea.", icon_chart),
    ]
    f_lab = font(F_SANS_B, 15)
    f_h2 = font(F_SANS_B, 19)
    f_b2 = font(F_SANS, 14)
    cell_w, cell_h = 468, 136
    x0s = [36, 520]
    y0s = [466, 612, 758]
    for i, (label, head, body, icon) in enumerate(stories):
        cx = x0s[i % 2]
        cy = y0s[i // 2]
        d.rectangle([cx, cy, cx + cell_w, cy + cell_h],
                    fill=PAPER, outline=BORDER, width=1)
        icon(d, cx + 12, cy + 26, 84)
        tx = cx + 108
        d.text((tx, cy + 12), label, font=f_lab, fill=RED)
        y = draw_lines(d, tx, cy + 34,
                       wrap(d, head, f_h2, cell_w - 122), f_h2, INK, 22)
        draw_lines(d, tx, y + 2,
                   wrap(d, body, f_b2, cell_w - 122), f_b2, INK, 18)

    # ---------------- in brief strip ----------------
    d.line([36, 902, W - 36, 902], fill=INK, width=1)
    f_brief_lab = font(F_SANS_B, 15)
    f_brief = font(F_SANS, 15)
    d.text((36, 910), "IN BRIEF", font=f_brief_lab, fill=RED)
    brief1 = ("BepiColombo enters orbit around Mercury  ·  ICJ: Myanmar "
              "committed genocide against the Rohingya in 2017")
    brief2 = ("EU and Indonesia sign major trade deal after a decade of "
              "talks  ·  US Democrats win at least 258 House seats")
    draw_lines(d, 36, 930, [brief1, brief2], f_brief, INK, 20)

    # ---------------- footer ----------------
    d.line([36, 972, W - 36, 972], fill=INK, width=1)
    f_foot = font(F_SANS, 14)
    center_text(d, W // 2, 978,
                "Sources: AP · Reuters · AFP · Al Jazeera — 22 November 2026",
                f_foot, GREY)

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
