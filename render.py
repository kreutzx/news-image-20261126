#!/usr/bin/env python3
"""Render the 26 November 2026 front page: a dense, counted, sourced
newspaper image, 1024x1024, drawn entirely in code with PIL.

Layout (top to bottom): masthead, two hero stories with drawn art,
a UTC timeline, four colour-coded sections, a sport strip, a
by-the-numbers band, markets & weather, late-wire one-liners, footer.
The renderer counts its stories from stories.py and prints the count.
Deterministic: fixed data, no clock, no network, no randomness.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stories

W, H = 1024, 1024
CREAM = (247, 242, 231)
PAPER = (255, 253, 247)
INK = (20, 33, 61)
RED = (193, 39, 45)
GOLD = (176, 138, 28)
GREEN = (46, 111, 64)
BROWN = (146, 90, 24)
GREY = (96, 96, 92)
LIGHT = (226, 220, 205)
SMOKE = (120, 120, 116)

FONT_DIR = "/usr/share/fonts/truetype/noto"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_BLACK = lambda s: font("NotoSerif-Black.ttf", s)
SERIF_BOLD = lambda s: font("NotoSerif-Bold.ttf", s)
SERIF = lambda s: font("NotoSerif-Regular.ttf", s)
SANS = lambda s: font("NotoSans-Regular.ttf", s)
SANS_BOLD = lambda s: font("NotoSans-Bold.ttf", s)
SANS_SEMI = lambda s: font("NotoSans-SemiBold.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns a list of lines."""
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


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def tag(draw, x, y, label, fill):
    """Small certainty/source pill; returns width used."""
    fnt = SANS_BOLD(8)
    tw = draw.textlength(label, font=fnt)
    w = int(tw) + 10
    draw.rounded_rectangle([x, y, x + w, y + 13], radius=6, fill=fill)
    draw.text((x + 5, y + 2), label, font=fnt, fill=(255, 255, 255))
    return w


def tag_fill(certainty):
    return {"CONFIRMED": GREEN, "CLAIM": RED,
            "REPORTED": GOLD, "FORECAST": GREY}[certainty]


def draw_tariffs_art(draw, x, y, w, h):
    """Globe with red tariff arrows and a 35% tag."""
    cx, cy = x + 52, y + h // 2
    r = min(h // 2 - 4, 46)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    draw.ellipse([cx - r, cy - 12, cx + r, cy + 12], outline=INK, width=2)
    draw.line([cx, cy - r, cx, cy + r], fill=INK, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=INK, width=2)
    for dx, dy in ((46, -26), (52, 6), (44, 30)):
        draw.line([cx + dx - 14, cy + dy, cx + dx + 12, cy + dy],
                  fill=RED, width=3)
        draw.polygon([(cx + dx + 12, cy + dy - 5), (cx + dx + 12, cy + dy + 5),
                      (cx + dx + 22, cy + dy)], fill=RED)
    draw.rounded_rectangle([x + w - 78, y + 6, x + w - 8, y + 30],
                           radius=5, fill=RED)
    draw.text((x + w - 70, y + 10), "UP TO 35%", font=SANS_BOLD(11),
              fill=(255, 255, 255))


def draw_refinery_art(draw, x, y, w, h):
    """Refinery towers, flame and smoke, scaled to the zone height."""
    s = h / 62.0
    base = y + h - 6
    draw.line([x, base, x + w, base], fill=INK, width=3)
    for i, (tx, tw, th) in enumerate(((6, 26, 52), (40, 20, 66), (68, 30, 44))):
        th = int(th * s)
        draw.rectangle([x + tx, base - th, x + tx + tw, base],
                       outline=INK, width=2, fill=PAPER)
        draw.line([x + tx, base - th, x + tx + tw // 2,
                   base - th - int(12 * s),
                   x + tx + tw, base - th], fill=INK, width=2)
    fx = x + 112
    fl = [(-58, 0), (-34, 14), (-58, 26), (-30, 34), (-58, 44), (-34, 58),
          (-58, 70), (0, 78)]
    draw.polygon([(fx + dx, base + int(dy * s)) for dy, dx in fl], fill=RED)
    fl2 = [(-40, 18), (-22, 30), (-40, 44), (-22, 56), (0, 62)]
    draw.polygon([(fx + dx, base + int(dy * s)) for dy, dx in fl2], fill=GOLD)
    for sx, sy, sr in ((150, y + 12, 7), (166, y + 6, 9), (184, y + 13, 6)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=SMOKE)


def draw_hero(draw, hero, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2, fill=PAPER)
    draw.rectangle([x, y, x + w, y + 18], fill=INK)
    draw.text((x + 8, y + 3), hero["kicker"], font=SANS_BOLD(10),
              fill=(255, 255, 255))
    art_h = 30
    if hero["art"] == "tariffs":
        draw_tariffs_art(draw, x + 10, y + h - art_h - 20, w - 20, art_h)
    else:
        draw_refinery_art(draw, x + 10, y + h - art_h - 20, w - 20, art_h)
    text_w = w - 16
    head = wrap(draw, hero["headline"], SERIF_BLACK(18), text_w)
    hy = y + 23
    hy = draw_lines(draw, head[:2], x + 8, hy, SERIF_BLACK(18), INK, 20)
    deck = wrap(draw, hero["deck"], SANS(10), text_w)
    hy = draw_lines(draw, deck[:3], x + 8, hy + 2, SANS(10), (40, 40, 40), 12)
    ty = y + h - 16
    tw = tag(draw, x + 8, ty, hero["certainty"], tag_fill(hero["certainty"]))
    draw.text((x + 8 + tw + 5, ty + 2), hero["source"], font=SANS_BOLD(9),
              fill=GREY)


def draw_card(draw, card, x, y, w, h, accent):
    draw.rectangle([x, y, x + w, y + h], outline=LIGHT, width=1, fill=PAPER)
    draw.rectangle([x, y, x + 4, y + h], fill=accent)
    head = wrap(draw, card["headline"], SERIF_BOLD(12), w - 14)
    cy = y + 4
    cy = draw_lines(draw, head[:2], x + 9, cy, SERIF_BOLD(12), INK, 14)
    deck = wrap(draw, card["deck"], SANS(9), w - 14)
    cy = draw_lines(draw, deck[:2], x + 9, cy + 1, SANS(9), (52, 52, 52), 10)
    ty = y + h - 14
    tw = tag(draw, x + 9, ty, card["certainty"], tag_fill(card["certainty"]))
    draw.text((x + 9 + tw + 5, ty + 2), card["source"], font=SANS_BOLD(8),
              fill=GREY)


def section_header(draw, name, color, x, y, w):
    draw.rectangle([x, y, x + w, y + 16], fill=color)
    draw.text((x + 6, y + 2), name, font=SANS_BOLD(10), fill=(255, 255, 255))
    return y + 16


def main():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    mx = 12
    cw = W - 2 * mx

    # ---- Masthead ----
    y = 10
    draw.rectangle([mx, y, mx + cw, y + 3], fill=RED)
    draw.text((mx, y + 6), "THE WORLD IN ONE PAGE",
              font=SERIF_BLACK(30), fill=INK)
    draw.text((mx, y + 40), "Thursday 26 November 2026",
              font=SERIF_BOLD(17), fill=RED)
    n = stories.story_count()
    regions = stories.region_counts()
    draw.text((mx, y + 60),
              "%d STORIES  ·  %d REGIONS  ·  4 FIELDS  ·  SOURCED: REUTERS · BBC · AP · GUARDIAN"
              % (n, len(regions)),
              font=SANS_BOLD(10), fill=INK)
    draw.line([mx, y + 74, mx + cw, y + 74], fill=INK, width=2)
    y += 80

    # ---- Heroes ----
    hw = (cw - 10) // 2
    hh = 134
    draw_hero(draw, stories.HEROES[0], mx, y, hw, hh)
    draw_hero(draw, stories.HEROES[1], mx + hw + 10, y, hw, hh)
    y += hh + 6

    # ---- UTC timeline ----
    draw.rectangle([mx, y, mx + cw, y + 30], fill=INK)
    draw.text((mx + 6, y + 3), "THE DAY IN UTC", font=SANS_BOLD(10),
              fill=GOLD)
    tx = mx + 108
    tw_each = (cw - 108) // len(stories.TIMELINE)
    for time, label in stories.TIMELINE:
        draw.text((tx, y + 3), time, font=SANS_BOLD(10), fill=(255, 255, 255))
        lab = wrap(draw, label, SANS(9), tw_each - 44)
        draw_lines(draw, lab[:2], tx + 34, y + 3, SANS(9),
                   (220, 220, 220), 11)
        tx += tw_each
    y += 30 + 5

    # ---- Sections ----
    card_h = 68
    gap = 6
    for section in stories.SECTIONS:
        cards = section["cards"]
        cols = 4 if len(cards) > 5 else len(cards)
        rows = (len(cards) + cols - 1) // cols
        y = section_header(draw, section["name"], section["color"], mx, y, cw)
        cell_w = (cw - (cols - 1) * gap) // cols
        for i, card in enumerate(cards):
            r, c = divmod(i, cols)
            cx = mx + c * (cell_w + gap)
            cy = y + r * (card_h + gap)
            last = (c == cols - 1 and r == rows - 1
                    and len(cards) % cols != 0)
            wdt = cell_w
            if last and len(cards) % cols:
                wdt = cell_w + (cols - len(cards) % cols) * (cell_w + gap)
            draw_card(draw, card, cx, cy, wdt, card_h, section["color"])
        y += rows * (card_h + gap) - gap + 4

    # ---- Sport strip ----
    y = section_header(draw, "SPORT", (20, 33, 61), mx, y, cw)
    cell_w = (cw - 3 * gap) // 4
    for i, card in enumerate(stories.SPORT):
        draw_card(draw, card, mx + i * (cell_w + gap), y, cell_w, card_h,
                  (20, 33, 61))
    y += card_h + 4

    # ---- By the numbers ----
    y = section_header(draw, "BY THE NUMBERS", GOLD, mx, y, cw)
    cell_w = cw // len(stories.BY_THE_NUMBERS)
    for i, (num, label) in enumerate(stories.BY_THE_NUMBERS):
        cx = mx + i * cell_w
        draw.text((cx + 4, y + 2), num, font=SERIF_BLACK(15), fill=RED)
        lab = wrap(draw, label, SANS(8), cell_w - 8)
        draw_lines(draw, lab[:2], cx + 4, y + 21, SANS(8), (52, 52, 52), 10)
        if i:
            draw.line([cx, y + 3, cx, y + 36], fill=LIGHT, width=1)
    y += 36 + 4

    # ---- Markets & weather ----
    draw.rectangle([mx, y, mx + cw, y + 24], outline=INK, width=1, fill=PAPER)
    draw.text((mx + 6, y + 2), "MARKETS", font=SANS_BOLD(9), fill=RED)
    draw.text((mx + 62, y + 2), stories.MARKETS, font=SANS_BOLD(9), fill=INK)
    draw.text((mx + 6, y + 13), "WEATHER", font=SANS_BOLD(9), fill=RED)
    draw.text((mx + 62, y + 13), stories.WEATHER, font=SANS_BOLD(9), fill=INK)
    y += 24 + 4

    # ---- Late wire ----
    y = section_header(draw, "LATE WIRE", GREY, mx, y, cw)
    ly = y
    for i, (text, source, certainty, _region) in enumerate(stories.LATE_WIRE):
        col = i % 2
        row = i // 2
        lx = mx + col * (cw // 2)
        lw = cw // 2 - 8
        draw.text((lx, ly + row * 11), "— " + text, font=SANS(10),
                  fill=(30, 30, 30))
        src = "  [" + source + "]"
        draw.text((lx + draw.textlength("— " + text, font=SANS(10)) + 2,
                   ly + row * 11), src, font=SANS_BOLD(8), fill=GREY)
    y = ly + 3 * 11 + 4

    # ---- Footer: coverage bands + sources ----
    fields = stories.field_counts()
    field_line = "  ·  ".join("%s %d" % (k, v) for k, v in fields.items())
    region_line = "  ·  ".join(
        "%s %d" % (stories.REGIONS[k], v)
        for k, v in sorted(regions.items(), key=lambda kv: -kv[1]))
    draw.line([mx, y, mx + cw, y], fill=INK, width=2)
    draw.text((mx, y + 3), "COVERAGE — " + field_line, font=SANS_BOLD(9),
              fill=INK)
    draw.text((mx, y + 13), "REGIONS — " + region_line, font=SANS_BOLD(9),
              fill=INK)
    draw.text((mx, y + 22),
              "All stories sourced from Reuters, BBC, The Guardian, Headline Desk and "
              "EventGraph. Claims flagged CLAIM; unconfirmed figures flagged REPORTED.",
              font=SANS(8), fill=GREY)
    y += 30

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    size = os.path.getsize(out)
    print("stories: %d (2 heroes + %d cards + %d sport + %d late wire)"
          % (n, sum(len(s["cards"]) for s in stories.SECTIONS),
             len(stories.SPORT), len(stories.LATE_WIRE)))
    print("regions: %s" % region_line)
    print("fields: %s" % field_line)
    print("entry.png: %d bytes, %dx%d, final y=%d" % (size, W, H, y))
    assert size <= 1048576, "entry.png over 1 MiB"
    assert y <= H, "layout overflowed the page"


if __name__ == "__main__":
    main()
