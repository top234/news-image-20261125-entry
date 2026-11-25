#!/usr/bin/env python3
"""Draw 'THE WORLD IN ONE DAY' - Wednesday 25 November 2026 - as a 1024x1024 PNG.

All text and numbers are hardcoded from FACTS.md (the coordinator's research file).
No clock, no network, no randomness: the same input always draws the same bytes.
Run:  python3 generate.py <output_dir>   (writes <output_dir>/entry.png)
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT_NAME = "entry.png"

PAPER = (248, 243, 230)   # newsprint cream
CARD = (255, 253, 246)    # card white
INK = (20, 20, 20)
RED = (168, 30, 36)
NAVY = (23, 63, 107)
TEAL = (15, 107, 92)
AMBER = (183, 121, 31)
GREY = (91, 91, 91)
RULE = (120, 110, 95)
SKY = (214, 228, 238)
SEA = (46, 105, 150)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)   # noqa: E731
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)          # noqa: E731
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)     # noqa: E731
F_SANS = lambda s: font("DejaVuSans.ttf", s)            # noqa: E731


def wrap(text, fnt, width, draw):
    """Greedy word wrap; returns list of lines that fit `width` pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None, align="left", width=None):
    """Draw lines; returns y after the last line."""
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in lines:
        if align == "center":
            draw.text((x + (width - draw.textlength(line, font=fnt)) / 2, y), line,
                      font=fnt, fill=fill)
        else:
            draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def chip(draw, x, y, num, fill, size=22):
    draw.rectangle([x, y, x + size, y + size], fill=fill)
    fnt = F_SANS_B(13)
    t = str(num)
    draw.text((x + (size - draw.textlength(t, font=fnt)) / 2, y + 3),
              t, font=fnt, fill=(255, 255, 255))


# ---------------------------------------------------------------- illustrations
def draw_tower(draw, x, y, w, h):
    """Riyadh skyline: tallest tower centre, smoke, drone. (x, y) top-left."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(196, 188, 168))  # ground
    # side buildings
    for bx, bw, bh in [(6, 34, 62), (46, 28, 84), (228, 30, 70), (262, 36, 56)]:
        draw.rectangle([x + bx, y + h - 26 - bh, x + bx + bw, y + h - 26],
                       fill=(90, 100, 112))
        for wy in range(y + h - 26 - bh + 8, y + h - 34, 14):
            draw.rectangle([x + bx + 5, wy, x + bx + bw - 5, wy + 6], fill=(210, 220, 228))
    # tallest tower (PIF Tower)
    tx, tw, th = x + 108, 74, 92
    draw.rectangle([tx, y + h - 26 - th, tx + tw, y + h - 26], fill=(52, 66, 84))
    draw.polygon([(tx, y + h - 26 - th), (tx + tw, y + h - 26 - th),
                  (tx + tw / 2, y + 2)], fill=(52, 66, 84))
    for wy in range(y + h - 26 - th + 12, y + h - 34, 13):
        draw.rectangle([tx + 8, wy, tx + tw - 8, wy + 6], fill=(150, 190, 215))
    # red impact flash at the tower crown
    cx, cy = tx + tw / 2, y + h - 26 - th + 6
    draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 220, 80))
    # smoke puffs flanking the spire, kept inside the illustration
    for sx, sy, r in [(cx - 52, cy + 10, 8), (cx + 52, cy + 6, 7), (cx - 44, cy + 26, 6)]:
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(150, 150, 148))
    # drone top-right
    dx, dy = x + w - 42, y + 22
    draw.ellipse([dx - 5, dy - 4, dx + 5, dy + 4], fill=INK)
    draw.line([dx - 12, dy - 8, dx + 12, dy + 8], fill=INK, width=2)
    draw.line([dx - 12, dy + 8, dx + 12, dy - 8], fill=INK, width=2)
    draw.line([dx, dy + 4, dx, dy + 26], fill=INK, width=1)


def draw_ship(draw, x, y, w, h):
    """Cargo ship at sea with a drone above. (x, y) top-left."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x, y + 62, x + w, y + h], fill=SEA)
    for wy in range(y + 66, y + h - 4, 12):  # wave lines
        for wx in range(x + 8, x + w - 8, 44):
            draw.arc([wx, wy, wx + 22, wy + 8], 180, 360, fill=(190, 220, 235), width=2)
    # hull
    draw.polygon([(x + 30, y + 96), (x + 250, y + 96), (x + 268, y + 116),
                  (x + 30, y + 116)], fill=(40, 44, 52))
    draw.rectangle([x + 30, y + 88, x + 250, y + 96], fill=(120, 30, 34))
    # containers
    cols = [RED, (220, 170, 40), TEAL, NAVY, (200, 90, 30)]
    for i, c in enumerate(cols):
        draw.rectangle([x + 44 + i * 38, y + 62, x + 44 + i * 38 + 34, y + 88], fill=c)
    # bridge
    draw.rectangle([x + 238, y + 52, x + 262, y + 88], fill=(235, 235, 228))
    draw.rectangle([x + 240, y + 58, x + 260, y + 66], fill=NAVY)
    # drone + dotted path
    dx, dy = x + 88, y + 18
    draw.ellipse([dx - 5, dy - 4, dx + 5, dy + 4], fill=INK)
    draw.line([dx - 12, dy - 8, dx + 12, dy + 8], fill=INK, width=2)
    draw.line([dx - 12, dy + 8, dx + 12, dy - 8], fill=INK, width=2)
    for i in range(6):
        draw.ellipse([dx + 8 + i * 10, dy + 22 + i * 5 - 2,
                      dx + 12 + i * 10, dy + 22 + i * 5 + 2], fill=RED)
    # splash near the bow
    for sx, sy, r in [(x + 276, y + 100, 5), (x + 284, y + 92, 4), (x + 270, y + 90, 3)]:
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(235, 245, 250))


def draw_court(draw, x, y, w, h):
    """Courthouse with columns and a gavel. (x, y) top-left."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x, y + h - 18, x + w, y + h], fill=(196, 188, 168))
    # pediment
    draw.polygon([(x + 30, y + 34), (x + w - 30, y + 34), (x + w / 2, y + 6)],
                 fill=(235, 228, 210))
    draw.rectangle([x + 30, y + 34, x + w - 30, y + 42], fill=(210, 200, 180))
    # columns
    for cx in [52, 96, 140, 184, 228]:
        draw.rectangle([x + cx, y + 42, x + cx + 16, y + h - 30], fill=(240, 236, 224))
        draw.rectangle([x + cx - 3, y + 42, x + cx + 19, y + 48], fill=(200, 190, 170))
        draw.rectangle([x + cx - 3, y + h - 36, x + cx + 19, y + h - 30], fill=(200, 190, 170))
    draw.rectangle([x + 30, y + h - 30, x + w - 30, y + h - 18], fill=(210, 200, 180))
    # gavel, bottom-right, resting on its block
    gx, gy = x + w - 78, y + h - 52
    draw.rectangle([gx - 6, gy + 16, gx + 46, gy + 24], fill=(120, 82, 40))  # block
    draw.line([gx + 8, gy + 12, gx + 38, gy - 14], fill=(96, 62, 28), width=6)  # handle
    draw.rectangle([gx + 30, gy - 22, gx + 52, gy - 6], fill=(80, 52, 24))  # head
    # verdict stamp
    draw.rectangle([x + 14, y + 8, x + 118, y + 30], outline=RED, width=2)
    draw.text((x + 20, y + 11), "GUILTY", font=F_SANS_B(15), fill=RED)


# ---------------------------------------------------------------- mini icons
def mini_icon(draw, kind, x, y, color):
    """A tiny 22x22 glyph for a small card, top-left at (x, y)."""
    if kind == "lock":  # CIA breach
        draw.arc([x + 6, y + 2, x + 16, y + 12], 180, 360, fill=color, width=2)
        draw.rectangle([x + 3, y + 10, x + 19, y + 21], fill=color)
        draw.ellipse([x + 9, y + 13, x + 13, y + 17], fill=CARD)
    elif kind == "medal":  # Giuliani
        draw.ellipse([x + 6, y + 8, x + 16, y + 18], outline=color, width=2)
        draw.line([x + 8, y + 7, x + 4, y + 1], fill=color, width=2)
        draw.line([x + 14, y + 7, x + 18, y + 1], fill=color, width=2)
    elif kind == "plane":  # NATO
        draw.polygon([(x + 11, y + 1), (x + 15, y + 12), (x + 21, y + 14),
                      (x + 14, y + 15), (x + 12, y + 21), (x + 9, y + 15),
                      (x + 1, y + 14), (x + 7, y + 12)], fill=color)
    elif kind == "tanker":  # Iran tankers
        draw.polygon([(x + 2, y + 12), (x + 20, y + 12), (x + 17, y + 19),
                      (x + 5, y + 19)], fill=color)
        draw.rectangle([x + 6, y + 5, x + 10, y + 12], fill=color)
        draw.rectangle([x + 12, y + 7, x + 16, y + 12], fill=color)
    elif kind == "scales":  # Sarkozy
        draw.line([x + 11, y + 1, x + 11, y + 19], fill=color, width=2)
        draw.line([x + 3, y + 4, x + 19, y + 4], fill=color, width=2)
        draw.polygon([(x + 1, y + 8), (x + 7, y + 8), (x + 4, y + 13)], fill=color)
        draw.polygon([(x + 15, y + 8), (x + 21, y + 8), (x + 18, y + 13)], fill=color)
    elif kind == "ball":  # cricket
        draw.ellipse([x + 7, y + 8, x + 17, y + 18], fill=color)
        draw.line([x + 2, y + 20, x + 12, y + 2], fill=color, width=3)
    elif kind == "ribbon":  # violence-against-women day
        draw.polygon([(x + 11, y + 1), (x + 15, y + 8), (x + 11, y + 21),
                      (x + 7, y + 8)], fill=color)
        draw.line([x + 11, y + 8, x + 18, y + 18], fill=color, width=2)
    elif kind == "cap":  # Seoul minister
        draw.polygon([(x + 1, y + 8), (x + 11, y + 2), (x + 21, y + 8),
                      (x + 11, y + 14)], fill=color)
        draw.line([x + 18, y + 9, x + 18, y + 17], fill=color, width=2)
    elif kind == "car":  # Waymo
        draw.rectangle([x + 2, y + 10, x + 20, y + 16], fill=color)
        draw.polygon([(x + 5, y + 10), (x + 8, y + 5), (x + 14, y + 5),
                      (x + 17, y + 10)], fill=color)
        draw.ellipse([x + 4, y + 15, x + 8, y + 19], fill=INK)
        draw.ellipse([x + 14, y + 15, x + 18, y + 19], fill=INK)
    elif kind == "chart":  # Anthropic
        draw.line([x + 2, y + 20, x + 2, y + 2], fill=color, width=2)
        draw.line([x + 2, y + 20, x + 20, y + 20], fill=color, width=2)
        draw.line([x + 4, y + 6, x + 10, y + 11, x + 15, y + 9, x + 20, y + 16],
                  fill=RED, width=2)


# ---------------------------------------------------------------- main drawing
def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 26                      # side margin
    CW = W - 2 * MX              # 972 content width

    # ---- masthead
    d.text((W / 2, 18), "THE WORLD IN ONE DAY", font=F_SERIF_B(56),
           fill=INK, anchor="ma")
    d.line([MX, 88, W - MX, 88], fill=INK, width=3)
    d.line([MX, 93, W - MX, 93], fill=INK, width=1)
    sub = "35 STORIES  ·  5 REGIONS  ·  EVERY ONE DATED WEDNESDAY 25 NOVEMBER 2026"
    d.text((W / 2, 100), sub, font=F_SANS_B(15), fill=RED, anchor="ma")

    # ---- three hero cards
    heroes = [
        (1, RED, draw_tower,
         "HOUTHIS HIT RIYADH'S TALLEST TOWER",
         "Saudi Civil Defense: at least 11 wounded in the second Houthi "
         "strike on the PIF Tower in under a week. Houthis now within "
         "60 km of Aden."),
        (2, NAVY, draw_ship,
         "ZELENSKIY CONFIRMS UKRAINE HIT RUSSIAN SHIP",
         "Kyiv confirms Saturday's drone strike on a Russian cargo ship "
         "in the Gulf of Finland. Norway urges caution; Putin calls "
         "retaliation \u201cinevitable\u201d."),
        (3, TEAL, draw_court,
         "HUAWEI CONVICTED IN US TRIAL",
         "Huawei guilty of stealing trade secrets in a sprawling US "
         "criminal trial over its Iran business \u2014 but acquitted of "
         "racketeering."),
    ]
    hy, hh, hw, gap = 124, 276, 316, 12
    for i, (num, color, scene, head, body) in enumerate(heroes):
        x = MX + i * (hw + gap)
        d.rectangle([x, hy, x + hw, hy + hh], fill=CARD, outline=INK, width=2)
        d.rectangle([x, hy, x + hw, hy + 6], fill=color)
        scene(d, x + 8, hy + 14, hw - 16, 118)
        d.text((x + 10, hy + 140), f"#{num}", font=F_SANS_B(13), fill=color)
        d.text((x + 34, hy + 140), "TOP STORY", font=F_SANS_B(12), fill=GREY)
        y = hy + 162
        y = text_block(d, x + 10, y, wrap(head, F_SERIF_B(19), hw - 20, d),
                       F_SERIF_B(19), leading=23)
        text_block(d, x + 10, y + 4, wrap(body, F_SANS(12), hw - 20, d),
                   F_SANS(12), fill=(40, 40, 40), leading=15)

    # ---- stat strip
    stats = [
        ("35", "STORIES IN THIS PAGE"),
        ("5", "REGIONS"),
        ("11", "WOUNDED IN RIYADH"),
        ("60 KM", "HOUTHIS FROM ADEN"),
        ("$83", "ANTHROPIC IPO PRICE"),
        ("2ND", "STRIKE IN A WEEK"),
    ]
    sy = 410
    d.rectangle([MX, sy, W - MX, sy + 52], fill=INK)
    sw = CW // 6
    for i, (num, label) in enumerate(stats):
        cx = MX + i * sw + sw // 2
        d.text((cx, sy + 5), num, font=F_SERIF_B(24), fill=(255, 255, 255), anchor="ma")
        d.text((cx, sy + 34), label, font=F_SANS_B(9), fill=(200, 200, 190), anchor="ma")
        if i:
            d.line([MX + i * sw, sy + 8, MX + i * sw, sy + 44], fill=(90, 90, 90), width=1)

    # ---- region bar (counts from FACTS.md: AM 10, ME 8, EU 7, AP 7, WO 3 = 35)
    regions = [("AMERICAS", 10, NAVY), ("MIDDLE EAST", 8, RED),
               ("EUROPE", 7, TEAL), ("ASIA-PACIFIC", 7, AMBER), ("WORLD", 3, GREY)]
    ry = 472
    d.text((MX, ry), "WHERE THE DAY'S NEWS CAME FROM", font=F_SANS_B(12), fill=INK)
    bx, by, bh = MX, ry + 20, 24
    x = bx
    for name, n, color in regions:
        seg = int(round(CW * n / 35))
        d.rectangle([x, by, x + seg, by + bh], fill=color)
        x += seg
    d.rectangle([bx, by, bx + CW, by + bh], outline=INK, width=1)
    lx = MX
    for name, n, color in regions:
        d.rectangle([lx, by + 32, lx + 12, by + 44], fill=color)
        d.text((lx + 16, by + 32), f"{name} {n}", font=F_SANS_B(12), fill=INK)
        lx += 16 + d.textlength(f"{name} {n}", font=F_SANS_B(12)) + 26

    # ---- small cards #4-#13
    small = [
        (4, NAVY, "lock", "CIA BREACH",
         "Unclassified data hit in a breach at the CIA and the DNI office."),
        (5, NAVY, "medal", "TRUMP HONOURS GIULIANI",
         "Presidential Medal of Freedom for ex-New York mayor."),
        (6, TEAL, "plane", "NATO TO POLAND + SPACE",
         "Early-warning jets for Poland; vow to defend space."),
        (7, RED, "tanker", "IRAN TANKERS MINED",
         "Three tankers hit by mines in the Strait of Hormuz."),
        (8, TEAL, "scales", "SARKOZY TO TRIAL",
         "Corruption case vs the ex-president goes to trial."),
        (9, GREY, "ball", "ENGLAND LEVEL T20 SERIES",
         "Eight-wicket win over Australia, chasing 185."),
        (10, GREY, "ribbon", "END VIOLENCE AGAINST WOMEN",
         "25 Nov: International Day against violence."),
        (11, AMBER, "cap", "SEOUL MINISTER QUITS",
         "Education chief resigns over exam cheating."),
        (12, NAVY, "car", "WAYMO OFF FREEWAYS",
         "Driverless taxis suspended from US freeways."),
        (13, NAVY, "chart", "ANTHROPIC SLIDES",
         "Shares fall below the $83 IPO price; ~$200bn at risk."),
    ]
    cw2, ch2, gap2 = 186, 88, 8
    sy2 = 538
    for i, (num, color, icon, title, body) in enumerate(small):
        col, row = i % 5, i // 5
        x = MX + col * (cw2 + gap2)
        y = sy2 + row * (ch2 + gap2)
        d.rectangle([x, y, x + cw2, y + ch2], fill=CARD, outline=(150, 140, 125), width=1)
        chip(d, x + 6, y + 6, num, color)
        mini_icon(d, icon, x + 34, y + 5, color)
        tlines = wrap(title, F_SANS_B(11), cw2 - 12, d)[:2]
        by2 = text_block(d, x + 6, y + 30, tlines, F_SANS_B(11), leading=13)
        max_body = max(1, (y + ch2 - 4 - by2) // 12)
        blines = wrap(body, F_SANS(10), cw2 - 12, d)[:max_body]
        text_block(d, x + 6, by2 + 2, blines, F_SANS(10), fill=(50, 50, 50), leading=12)

    # ---- dotted world map (left) + ALSO list (right)
    my = 730
    d.text((MX, my), "THE DAY ON THE MAP", font=F_SANS_B(12), fill=INK)
    d.text((372, my), "ALSO ON WEDNESDAY 25 NOVEMBER \u2014 22 MORE STORIES",
           font=F_SANS_B(12), fill=INK)
    d.line([MX, my + 18, W - MX, my + 18], fill=RULE, width=1)
    # land as (row, col_start, col_end) on a 40x15 dot grid
    land = [(1, 2, 10), (2, 1, 12), (3, 1, 11), (4, 2, 10), (5, 3, 9),
            (6, 4, 8), (7, 7, 11), (8, 8, 12), (9, 9, 12), (10, 9, 11),
            (11, 10, 11),
            (1, 21, 25), (2, 21, 26), (3, 22, 25),
            (5, 21, 26), (6, 21, 27), (7, 22, 27), (8, 22, 26), (9, 23, 25),
            (1, 26, 39), (2, 26, 40), (3, 26, 39), (4, 27, 38), (5, 27, 37),
            (9, 34, 39), (10, 35, 39)]
    gx0, gy0, step = 34, 758, 8
    landset = set()
    for r, c0, c1 in land:
        for c in range(c0, c1 + 1):
            landset.add((r, c))
    for (r, c) in landset:
        d.ellipse([gx0 + c * step - 2, gy0 + r * step - 2,
                   gx0 + c * step + 2, gy0 + r * step + 2], fill=(120, 130, 140))
    pins = [(1, 26, 5), (2, 25, 1), (3, 5, 3), (6, 21, 2), (7, 29, 5),
            (11, 36, 2), (24, 33, 6), (25, 38, 4)]
    for num, c, r in pins:
        px, py = gx0 + c * step, gy0 + r * step
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255), width=1)
        t = str(num)
        fnt = F_SANS_B(8)
        d.text((px - d.textlength(t, font=fnt) / 2, py - 4), t, font=fnt,
               fill=(255, 255, 255))
    d.text((MX, 868), "Pins: 1 Riyadh  ·  2 Gulf of Finland  ·  3 USA  ·  6 Poland",
           font=F_SANS(10), fill=GREY)
    d.text((MX, 884), "7 Strait of Hormuz  ·  11 Seoul  ·  24 Myanmar  ·  25 Osaka",
           font=F_SANS(10), fill=GREY)

    also = [
        (14, "Turkeys Freedom & Feathers spared"),
        (15, "Kim Yo-jong threatens Swiss office"),
        (16, "Pugh swims 15 km in Strait of Hormuz"),
        (17, "Fort Hood shooter seeks execution stay"),
        (18, "UN warns over Gaza hardship"),
        (19, "Eisenkot condemns settler arson"),
        (20, "New US tariffs set to be unveiled"),
        (21, "Dell lifts forecasts; Nvidia falls 7%"),
        (22, "Radar issue delays Chicago O'Hare flights"),
        (23, "Iraq PM orders Kurdish oilfields managed"),
        (24, "UN court condemns Myanmar over Rohingya"),
        (25, "First Japan\u2013ASEAN forum opens in Osaka"),
        (26, "BJP & Akali Dal ally for Punjab 2027"),
        (27, "Nepal PM ends first state visit to India"),
        (28, "EU adds restrictive measures on Russia"),
        (29, "Russia & Ukraine trade UN accusations"),
        (30, "US & Qatar discuss strategic cooperation"),
        (31, "US envoy unsure Israel aid ends this year"),
        (32, "UK panel on nuclear test veterans"),
        (33, "Man Utd fury over Yoro red card"),
        (34, "Sooryavanshi's fastest List A double ton"),
        (35, "GTA 6 keeps dominating gaming headlines"),
    ]
    ax = 372
    for i, (num, txt) in enumerate(also):
        col, row = i // 11, i % 11
        x = ax + col * 318
        y = my + 26 + row * 16
        d.text((x, y), f"{num}", font=F_SANS_B(11), fill=RED)
        d.text((x + 26, y), txt, font=F_SANS(11), fill=INK)

    # ---- DATE CHECK box
    dy = 936
    d.rectangle([MX, dy, W - MX, dy + 40], outline=INK, width=2)
    d.text((MX + 10, dy + 4),
           "DATE CHECK \u2014 TUE = the news the world woke up to on Wednesday 25 November; "
           "WED = reported on Wednesday itself.",
           font=F_SANS_B(10), fill=INK)
    d.text((MX + 10, dy + 21),
           "Sources: Reuters \u00b7 AP \u00b7 BBC \u00b7 Washington Post. "
           "Nothing in this image is from another day.",
           font=F_SANS(10), fill=INK)

    # ---- footer
    d.line([MX, 984, W - MX, 984], fill=INK, width=1)
    d.text((W / 2, 990),
           "THE WORLD IN ONE DAY  \u00b7  WEDNESDAY 25 NOVEMBER 2026  \u00b7  "
           "PRESS TIME 01:30 GMT, 25 NOV 2026",
           font=F_SANS_B(11), fill=INK, anchor="ma")
    return img


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("OUTPUT_DIR", ".")
    os.makedirs(out_dir, exist_ok=True)
    img = draw()
    img.save(os.path.join(out_dir, OUT_NAME), format="PNG", optimize=True)
    print(f"wrote {os.path.join(out_dir, OUT_NAME)} {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
