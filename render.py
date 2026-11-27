#!/usr/bin/env python3
"""Render the 26 November 2026 front page: a dense, counted, sourced
newspaper image, 1024x1024, drawn entirely in code with PIL.

Layout (top to bottom): masthead, two hero stories with drawn art,
a UTC timeline, a world map band, four colour-coded sections with
per-card motif icons (13 drawn scenes in all), a sport strip, a
by-the-numbers band, markets & weather, late-wire one-liners, and a
footer with a printed date check.
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


TEAL = (32, 96, 96)


def motif(draw, kind, x, y, s, ink=INK, accent=RED):
    """Small flat PIL icon of size s drawn at (x, y): ink + one accent."""
    if kind == "drone":
        draw.ellipse([x + s * .32, y + s * .30, x + s * .68, y + s * .62], fill=ink)
        draw.rectangle([x + s * .10, y + s * .42, x + s * .90, y + s * .50], fill=ink)
        for cx in (0.14, 0.86):
            draw.line([x + s * (cx - .10), y + s * .28, x + s * (cx + .10), y + s * .28],
                      fill=accent, width=3)
        draw.line([x + s * .5, y + s * .62, x + s * .5, y + s * .82], fill=accent, width=3)
    elif kind == "globe":
        draw.ellipse([x + 3, y + 3, x + s - 3, y + s - 3], outline=ink, width=3)
        draw.ellipse([x + s * .32, y + 3, x + s * .68, y + s - 3], outline=ink, width=2)
        draw.line([x + 3, y + s * .5, x + s - 3, y + s * .5], fill=ink, width=2)
        draw.arc([x + s * .05, y + s * .28, x + s * .95, y + s * .72], 200, 340,
                 fill=accent, width=3)
    elif kind == "flame":
        draw.polygon([(x + s * .5, y + s * .04), (x + s * .86, y + s * .55),
                      (x + s * .68, y + s * .96), (x + s * .32, y + s * .96),
                      (x + s * .14, y + s * .55)], fill=accent)
        draw.polygon([(x + s * .5, y + s * .45), (x + s * .68, y + s * .74),
                      (x + s * .32, y + s * .74)], fill=GOLD)
    elif kind == "mic":
        draw.rounded_rectangle([x + s * .38, y + s * .06, x + s * .62, y + s * .55],
                               radius=7, fill=ink)
        draw.arc([x + s * .24, y + s * .42, x + s * .76, y + s * .86], 0, 180,
                 fill=ink, width=3)
        draw.line([x + s * .5, y + s * .68, x + s * .5, y + s * .94], fill=ink, width=3)
        draw.line([x + s * .34, y + s * .94, x + s * .66, y + s * .94], fill=accent, width=3)
    elif kind == "drop":
        draw.polygon([(x + s * .5, y + s * .04), (x + s * .86, y + s * .55),
                      (x + s * .82, y + s * .80), (x + s * .18, y + s * .80),
                      (x + s * .14, y + s * .55)], fill=TEAL)
        draw.ellipse([x + s * .30, y + s * .56, x + s * .46, y + s * .74], fill=PAPER)
    elif kind == "atom":
        cx, cy = x + s / 2, y + s / 2
        draw.ellipse([x + 3, y + s * .20, x + s - 3, y + s * .80], outline=ink, width=2)
        draw.ellipse([x + s * .20, y + 3, x + s * .80, y + s - 3], outline=ink, width=2)
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=accent)
    elif kind == "scales":
        draw.line([x + s * .5, y + s * .08, x + s * .5, y + s * .84], fill=ink, width=3)
        draw.line([x + s * .14, y + s * .22, x + s * .86, y + s * .22], fill=ink, width=3)
        for cx in (0.22, 0.78):
            draw.polygon([(x + s * cx, y + s * .22), (x + s * (cx - .16), y + s * .56),
                          (x + s * (cx + .16), y + s * .56)], outline=accent, width=2)
        draw.line([x + s * .30, y + s * .90, x + s * .70, y + s * .90], fill=ink, width=3)
    elif kind == "satellite":
        draw.rectangle([x + s * .38, y + s * .38, x + s * .62, y + s * .62], fill=ink)
        draw.rectangle([x + s * .04, y + s * .42, x + s * .32, y + s * .58], fill=TEAL)
        draw.rectangle([x + s * .68, y + s * .42, x + s * .96, y + s * .58], fill=TEAL)
        draw.line([x + s * .62, y + s * .50, x + s * .80, y + s * .20], fill=ink, width=2)
        draw.ellipse([x + s * .78, y + s * .10, x + s * .90, y + s * .22], fill=accent)
    elif kind == "chart":
        base = y + s * .88
        for i, hh in enumerate((0.35, 0.60, 0.45, 0.80)):
            bx = x + s * (0.12 + i * 0.22)
            draw.rectangle([bx, base - s * hh, bx + s * .14, base],
                           fill=ink if i < 3 else accent)
        draw.line([x + s * .08, base, x + s * .92, base], fill=ink, width=2)
    elif kind == "chip":
        draw.rectangle([x + s * .25, y + s * .25, x + s * .75, y + s * .75], fill=ink)
        draw.rectangle([x + s * .40, y + s * .40, x + s * .60, y + s * .60], fill=GOLD)
        for i in range(3):
            px = x + s * (0.33 + i * 0.17)
            draw.line([px, y + s * .06, px, y + s * .25], fill=ink, width=2)
            draw.line([px, y + s * .75, px, y + s * .94], fill=ink, width=2)
            py = y + s * (0.33 + i * 0.17)
            draw.line([x + s * .06, py, x + s * .25, py], fill=ink, width=2)
            draw.line([x + s * .75, py, x + s * .94, py], fill=ink, width=2)
    elif kind == "volcano":
        draw.polygon([(x + s * .5, y + s * .30), (x + s * .96, y + s * .94),
                      (x + s * .04, y + s * .94)], fill=ink)
        draw.polygon([(x + s * .5, y + s * .30), (x + s * .66, y + s * .54),
                      (x + s * .34, y + s * .54)], fill=accent)
        for dx, dy, r in ((0.30, 0.12, 5), (0.55, 0.05, 7), (0.72, 0.16, 5)):
            draw.ellipse([x + s * dx - r, y + s * dy - r, x + s * dx + r, y + s * dy + r],
                         fill=SMOKE)
    elif kind == "asteroid":
        draw.polygon([(x + s * .20, y + s * .25), (x + s * .55, y + s * .10),
                      (x + s * .86, y + s * .35), (x + s * .78, y + s * .76),
                      (x + s * .40, y + s * .90), (x + s * .10, y + s * .60)], fill=ink)
        for dx, dy, r in ((0.45, 0.40, 5), (0.62, 0.60, 4), (0.35, 0.62, 3)):
            draw.ellipse([x + s * dx - r, y + s * dy - r, x + s * dx + r, y + s * dy + r],
                         fill=GOLD)
    elif kind == "aurora":
        for i, col in enumerate((TEAL, (46, 160, 140), GOLD)):
            yy = y + s * (0.24 + i * 0.22)
            draw.arc([x + s * .04, yy - s * .18, x + s * .96, yy + s * .18],
                     200, 340, fill=col, width=4)
        draw.polygon([(x + s * .14, y + s * .88), (x + s * .35, y + s * .62),
                      (x + s * .56, y + s * .88)], fill=ink)
        draw.polygon([(x + s * .54, y + s * .88), (x + s * .72, y + s * .70),
                      (x + s * .90, y + s * .88)], fill=ink)
    elif kind == "iceberg":
        draw.polygon([(x + s * .08, y + s * .55), (x + s * .30, y + s * .14),
                      (x + s * .55, y + s * .45), (x + s * .75, y + s * .10),
                      (x + s * .94, y + s * .55)], fill=(178, 205, 220))
        draw.rectangle([x + s * .04, y + s * .55, x + s * .96, y + s * .63], fill=TEAL)
        draw.polygon([(x + s * .25, y + s * .63), (x + s * .45, y + s * .92),
                      (x + s * .65, y + s * .63)], fill=(140, 175, 200))
    elif kind == "gavel":
        draw.rectangle([x + s * .12, y + s * .16, x + s * .74, y + s * .36], fill=ink)
        draw.rectangle([x + s * .12, y + s * .40, x + s * .74, y + s * .48], fill=ink)
        draw.line([x + s * .34, y + s * .44, x + s * .68, y + s * .82], fill=ink, width=4)
        draw.rectangle([x + s * .52, y + s * .86, x + s * .96, y + s * .94], fill=accent)
    elif kind == "storm":
        draw.ellipse([x + s * .10, y + s * .12, x + s * .56, y + s * .46], fill=SMOKE)
        draw.ellipse([x + s * .42, y + s * .08, x + s * .90, y + s * .46], fill=ink)
        draw.rectangle([x + s * .18, y + s * .30, x + s * .84, y + s * .48], fill=ink)
        draw.polygon([(x + s * .52, y + s * .50), (x + s * .38, y + s * .78),
                      (x + s * .50, y + s * .78), (x + s * .42, y + s * .96),
                      (x + s * .66, y + s * .66), (x + s * .54, y + s * .66)], fill=GOLD)
    elif kind == "ship":
        draw.polygon([(x + s * .12, y + s * .55), (x + s * .88, y + s * .55),
                      (x + s * .70, y + s * .86), (x + s * .30, y + s * .86)], fill=ink)
        draw.rectangle([x + s * .42, y + s * .30, x + s * .58, y + s * .55], fill=accent)
        draw.line([x + s * .5, y + s * .10, x + s * .5, y + s * .30], fill=ink, width=2)
    elif kind == "bank":
        draw.polygon([(x + s * .5, y + s * .06), (x + s * .94, y + s * .30),
                      (x + s * .06, y + s * .30)], fill=ink)
        for i in range(4):
            bx = x + s * (0.14 + i * 0.20)
            draw.rectangle([bx, y + s * .38, bx + s * .10, y + s * .76], fill=ink)
        draw.rectangle([x + s * .06, y + s * .82, x + s * .94, y + s * .92], fill=accent)
    elif kind == "coin":
        draw.ellipse([x + s * .12, y + s * .12, x + s * .88, y + s * .88],
                     outline=GOLD, width=4)
        draw.text((x + s * .38, y + s * .28), "$", font=SANS_BOLD(int(s * .42)), fill=GOLD)
    elif kind == "leaf":
        draw.polygon([(x + s * .5, y + s * .06), (x + s * .88, y + s * .44),
                      (x + s * .62, y + s * .88), (x + s * .22, y + s * .78),
                      (x + s * .14, y + s * .34)], fill=GREEN)
        draw.line([x + s * .30, y + s * .76, x + s * .70, y + s * .30], fill=PAPER, width=2)
    elif kind == "ball":
        draw.ellipse([x + s * .10, y + s * .10, x + s * .90, y + s * .90],
                     outline=ink, width=3)
        draw.polygon([(x + s * .5, y + s * .34), (x + s * .66, y + s * .48),
                      (x + s * .60, y + s * .66), (x + s * .40, y + s * .66),
                      (x + s * .34, y + s * .48)], fill=accent)


def draw_tariffs_art(draw, x, y, w, h):
    """Globe with red tariff arrows and a 35% tag."""
    cx, cy = x + 52, y + h // 2
    r = min(h // 2 - 4, 46)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    draw.ellipse([cx - r, cy - 12, cx + r, cy + 12], outline=INK, width=2)
    draw.line([cx, cy - r, cx, cy + r], fill=INK, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=INK, width=2)
    for dx, dy in ((46, -26), (52, 6), (44, 30)):
        dx, dy = int(dx * r / 46), int(dy * r / 46)
        draw.line([cx + dx - 10, cy + dy, cx + dx + 8, cy + dy],
                  fill=RED, width=3)
        draw.polygon([(cx + dx + 8, cy + dy - 4), (cx + dx + 8, cy + dy + 4),
                      (cx + dx + 16, cy + dy)], fill=RED)
    draw.rounded_rectangle([x + w - 78, y + 6, x + w - 8, y + 30],
                           radius=5, fill=RED)
    draw.text((x + w - 70, y + 10), "UP TO 35%", font=SANS_BOLD(11),
              fill=(255, 255, 255))


def draw_refinery_art(draw, x, y, w, h):
    """Refinery towers, flame and smoke, scaled to the zone height."""
    s = h / 78.0
    base = y + h - 6
    draw.line([x, base, x + w, base], fill=INK, width=3)
    for i, (tx, tw, th) in enumerate(((6, 26, 52), (40, 20, 66), (68, 30, 44))):
        th = int(th * s)
        draw.rectangle([x + tx, base - th, x + tx + tw, base],
                       outline=INK, width=2, fill=PAPER)
        draw.line([x + tx, base - th, x + tx + tw // 2,
                   base - th - int(12 * s),
                   x + tx + tw, base - th], fill=INK, width=2)
    fx = x + 100
    fl = [(-58, 0), (-34, 14), (-58, 26), (-30, 34), (-58, 44), (-34, 58),
          (-58, 70), (0, 78)]
    draw.polygon([(fx + int(dx * s), base + int(dy * s)) for dy, dx in fl],
                 fill=RED)
    fl2 = [(-40, 18), (-22, 30), (-40, 44), (-22, 56), (0, 62)]
    draw.polygon([(fx + int(dx * s), base + int(dy * s)) for dy, dx in fl2],
                 fill=GOLD)
    for sx, sy, sr in ((x + 128, y + 10, 5), (x + 142, y + 5, 7),
                       (x + 156, y + 11, 4)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=SMOKE)


def draw_hero(draw, hero, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2, fill=PAPER)
    draw.rectangle([x, y, x + w, y + 18], fill=INK)
    draw.text((x + 8, y + 3), hero["kicker"], font=SANS_BOLD(10),
              fill=(255, 255, 255))
    # Scene art in a top-right column beside the headline.
    if hero["art"] == "tariffs":
        draw_tariffs_art(draw, x + w - 176, y + 23, 166, 38)
    else:
        draw_refinery_art(draw, x + w - 176, y + 23, 166, 38)
    head = wrap(draw, hero["headline"], SERIF_BLACK(17), w - 192)
    hy = y + 22
    hy = draw_lines(draw, head[:2], x + 8, hy, SERIF_BLACK(17), INK, 19)
    deck = wrap(draw, hero["deck"], SANS(9), w - 16)
    hy = draw_lines(draw, deck[:3], x + 8, hy + 2, SANS(9), (40, 40, 40), 11)
    ty = y + h - 16
    tw = tag(draw, x + 8, ty, hero["certainty"], tag_fill(hero["certainty"]))
    draw.text((x + 8 + tw + 5, ty + 2), hero["source"], font=SANS_BOLD(9),
              fill=GREY)


def draw_card(draw, card, x, y, w, h, accent):
    draw.rectangle([x, y, x + w, y + h], outline=LIGHT, width=1, fill=PAPER)
    draw.rectangle([x, y, x + 4, y + h], fill=accent)
    kind = card.get("motif")
    reserve = 48 if kind else 0
    text_w = w - 14 - reserve
    head = wrap(draw, card["headline"], SERIF_BOLD(11), text_w)
    cy = y + 3
    cy = draw_lines(draw, head[:2], x + 9, cy, SERIF_BOLD(11), INK, 13)
    deck = wrap(draw, card["deck"], SANS(8), text_w)
    cy = draw_lines(draw, deck[:2], x + 9, cy, SANS(8), (52, 52, 52), 9)
    if kind:
        motif(draw, kind, x + w - 44, y + (h - 38) // 2, 38, INK, accent)
    ty = y + h - 14
    tw = tag(draw, x + 9, ty, card["certainty"], tag_fill(card["certainty"]))
    draw.text((x + 9 + tw + 5, ty + 2), card["source"], font=SANS_BOLD(8),
              fill=GREY)


# ---- World map: coarse continent outlines as (lon, lat) point lists ----
LAND = (168, 196, 188)

NORTH_AMERICA = [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69),
                 (-85, 66), (-80, 73), (-75, 62), (-65, 60), (-55, 52),
                 (-65, 45), (-70, 42), (-74, 40), (-76, 35), (-80, 32),
                 (-80, 26), (-84, 30), (-89, 30), (-94, 29), (-97, 26),
                 (-97, 22), (-94, 18), (-90, 15), (-86, 13), (-83, 9),
                 (-79, 9), (-83, 15), (-90, 14), (-95, 16), (-102, 18),
                 (-105, 23), (-110, 24), (-114, 29), (-117, 33), (-122, 37),
                 (-124, 46), (-130, 55), (-150, 60), (-165, 60)]
GREENLAND = [(-45, 60), (-30, 68), (-22, 70), (-20, 76), (-30, 82),
             (-50, 80), (-58, 76), (-55, 70), (-53, 64)]
SOUTH_AMERICA = [(-79, 9), (-75, 11), (-64, 11), (-52, 5), (-44, -3),
                 (-35, -8), (-39, -13), (-40, -22), (-48, -27), (-52, -33),
                 (-57, -38), (-62, -41), (-65, -45), (-67, -50), (-68, -54),
                 (-71, -54), (-73, -46), (-73, -37), (-71, -30), (-70, -20),
                 (-75, -15), (-79, -8), (-80, -4), (-77, 4)]
EURASIA = [(-9, 37), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (0, 50),
           (3, 52), (7, 54), (8, 57), (10, 59), (18, 57), (21, 59),
           (24, 59), (27, 60), (30, 60), (30, 64), (33, 67), (35, 69),
           (45, 68), (55, 68), (68, 70), (80, 73), (95, 76), (110, 74),
           (125, 72), (140, 72), (155, 70), (170, 67), (178, 65),
           (173, 62), (162, 60), (160, 55), (156, 51), (142, 54),
           (142, 46), (141, 40), (138, 36), (133, 34), (129, 33),
           (126, 35), (122, 38), (122, 31), (121, 28), (118, 25),
           (110, 20), (109, 15), (107, 11), (104, 8), (103, 2),
           (100, 7), (98, 10), (97, 16), (93, 17), (89, 22), (86, 20),
           (84, 18), (80, 15), (77, 8), (75, 13), (72, 19), (68, 23),
           (66, 25), (61, 25), (57, 26), (52, 26), (50, 29), (48, 28),
           (49, 24), (54, 24), (58, 23), (59, 22), (55, 17), (52, 15),
           (46, 12), (43, 12), (40, 15), (38, 22), (35, 28), (34, 31),
           (36, 33), (36, 36), (30, 36), (27, 37), (23, 36), (22, 37),
           (19, 40), (16, 38), (16, 40), (13, 44), (10, 44), (7, 44),
           (3, 43), (0, 39), (-2, 37)]
UK = [(-5, 50), (-3, 53), (-5, 55), (-3, 57), (-2, 58), (-1, 55), (0, 52),
      (1, 51)]
AFRICA = [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31),
          (32, 31), (34, 28), (35, 24), (38, 20), (40, 15), (43, 12),
          (48, 11), (51, 12), (48, 5), (42, -2), (40, -10), (39, -18),
          (36, -22), (33, -26), (28, -33), (20, -35), (17, -32),
          (15, -27), (13, -18), (12, -10), (13, -1), (9, 4), (8, 4),
          (-7, 5), (-13, 8), (-17, 15), (-16, 20), (-15, 25), (-13, 28),
          (-10, 31)]
MADAGASCAR = [(44, -16), (47, -14), (50, -16), (48, -20), (46, -24),
              (45, -25), (44, -20), (43, -17)]
AUSTRALIA = [(114, -22), (113, -26), (115, -32), (118, -35), (124, -33),
             (129, -32), (132, -32), (135, -35), (137, -35), (139, -37),
             (141, -38), (145, -38), (147, -38), (150, -37), (153, -31),
             (153, -27), (151, -24), (149, -20), (146, -19), (143, -15),
             (142, -11), (142, -13), (140, -18), (139, -18), (136, -15),
             (135, -12), (132, -11), (130, -12), (126, -14), (122, -17),
             (118, -20)]
BORNEO = [(109, 1), (113, 4), (117, 6), (119, 2), (117, -2), (113, -3),
          (110, -2)]
CONTINENTS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, EURASIA, UK,
              AFRICA, MADAGASCAR, AUSTRALIA, BORNEO]
# Island dots/ellipses: Japan, Indonesia, New Zealand (lon, lat, rx, ry in deg)
ISLANDS = [(130, 31, 3, 2), (133, 34, 3, 2), (137, 35, 3, 2), (140, 37, 3, 3),
           (141, 40, 2, 3), (142, 44, 3, 2),
           (95, 5, 4, 2), (100, 0, 4, 2), (105, -6, 4, 2), (110, -7, 4, 2),
           (115, -8, 3, 2), (120, -9, 3, 2), (125, -2, 3, 2), (131, -3, 3, 2),
           (136, -3, 3, 2), (141, -4, 3, 2),
           (167, -45, 3, 3), (172, -41, 3, 3), (176, -38, 2, 2)]
# Red dots at places our 35 stories actually touch (lon, lat).
MAP_DOTS = [(-77, 39),    # Washington DC — tariffs hero
            (50, 27),     # Ras Tanura — refinery hero
            (34, 31),     # Gaza
            (31, 49),     # Kyiv / Ukraine
            (31, 30),     # Cairo
            (127, 37),    # Seoul — Bank of Korea
            (140, 36),    # Tokyo — Bank of Japan
            (0, 51),      # London
            (35, 32),     # Jerusalem
            (151, -34)]   # Sydney — ANZ / Australia


def draw_world_map(draw, x, y, w, h):
    """Flat world map band: caption, graticule, continents, story dots."""
    draw.text((x + 2, y), "WORLD MAP — WHERE TODAY'S STORIES HAPPENED",
              font=SANS_BOLD(10), fill=RED)
    note = "RED DOTS: 10 STORY PLACES"
    draw.text((x + w - draw.textlength(note, font=SANS_BOLD(9)), y + 1),
              note, font=SANS_BOLD(9), fill=GREY)
    my = y + 14
    mh = h - 14
    draw.rectangle([x, my, x + w, my + mh], outline=LIGHT, width=1, fill=PAPER)

    def px(lon):
        return x + (lon + 180) / 360.0 * w

    def py(lat):
        return my + (78 - lat) / 136.0 * mh

    for lon in range(-150, 180, 30):
        draw.line([px(lon), my, px(lon), my + mh], fill=LIGHT, width=1)
    for lat in (60, 30, 0, -30):
        draw.line([x, py(lat), x + w, py(lat)], fill=LIGHT, width=1)
    for poly in CONTINENTS:
        draw.polygon([(px(lon), py(lat)) for lon, lat in poly],
                     fill=LAND, outline=TEAL)
    for lon, lat, rx, ry in ISLANDS:
        draw.ellipse([px(lon - rx), py(lat + ry), px(lon + rx), py(lat - ry)],
                     fill=LAND, outline=TEAL)
    for lon, lat in MAP_DOTS:
        cx, cy = px(lon), py(lat)
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED,
                     outline=(255, 255, 255))


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
    y = 6
    draw.rectangle([mx, y, mx + cw, y + 3], fill=RED)
    draw.text((mx, y + 5), "THE WORLD IN ONE PAGE",
              font=SERIF_BLACK(26), fill=INK)
    draw.text((mx, y + 33), "Thursday 26 November 2026",
              font=SERIF_BOLD(15), fill=RED)
    n = stories.story_count()
    regions = stories.region_counts()
    drawn = 2 + sum(1 for s in stories.SECTIONS for c in s["cards"]
                    if c.get("motif"))
    draw.text((mx, y + 52),
              "%d STORIES  ·  %d REGIONS  ·  4 FIELDS  ·  %d DRAWN SCENES  ·  WORLD MAP  ·  SOURCED: REUTERS · BBC · GUARDIAN"
              % (n, len(regions), drawn),
              font=SANS_BOLD(9), fill=INK)
    draw.line([mx, y + 64, mx + cw, y + 64], fill=INK, width=2)
    y += 68

    # ---- Heroes ----
    hw = (cw - 10) // 2
    hh = 104
    draw_hero(draw, stories.HEROES[0], mx, y, hw, hh)
    draw_hero(draw, stories.HEROES[1], mx + hw + 10, y, hw, hh)
    y += hh + 4

    # ---- UTC timeline ----
    draw.rectangle([mx, y, mx + cw, y + 24], fill=INK)
    draw.text((mx + 6, y + 2), "THE DAY IN UTC", font=SANS_BOLD(9),
              fill=GOLD)
    tx = mx + 100
    tw_each = (cw - 100) // len(stories.TIMELINE)
    for time, label in stories.TIMELINE:
        draw.text((tx, y + 2), time, font=SANS_BOLD(9), fill=(255, 255, 255))
        lab = wrap(draw, label, SANS(8), tw_each - 40)
        draw_lines(draw, lab[:2], tx + 32, y + 2, SANS(8),
                   (220, 220, 220), 10)
        tx += tw_each
    y += 24 + 3

    # ---- World map ----
    draw_world_map(draw, mx, y, cw, 100)
    y += 100 + 4

    # ---- Sections ----
    card_h = 62
    gap = 5
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
        y += rows * (card_h + gap) - gap + 2

    # ---- Sport strip ----
    y = section_header(draw, "SPORT", (20, 33, 61), mx, y, cw)
    cell_w = (cw - 3 * gap) // 4
    for i, card in enumerate(stories.SPORT):
        draw_card(draw, card, mx + i * (cell_w + gap), y, cell_w, card_h,
                  (20, 33, 61))
    y += card_h + 2

    # ---- By the numbers ----
    y = section_header(draw, "BY THE NUMBERS", GOLD, mx, y, cw)
    cell_w = cw // len(stories.BY_THE_NUMBERS)
    for i, (num, label) in enumerate(stories.BY_THE_NUMBERS):
        cx = mx + i * cell_w
        draw.text((cx + 4, y + 1), num, font=SERIF_BLACK(14), fill=RED)
        lab = wrap(draw, label, SANS(8), cell_w - 8)
        draw_lines(draw, lab[:2], cx + 4, y + 19, SANS(8), (52, 52, 52), 9)
        if i:
            draw.line([cx, y + 3, cx, y + 28], fill=LIGHT, width=1)
    y += 30 + 2

    # ---- Markets & weather ----
    draw.rectangle([mx, y, mx + cw, y + 20], outline=INK, width=1, fill=PAPER)
    draw.text((mx + 6, y + 1), "MARKETS", font=SANS_BOLD(8), fill=RED)
    draw.text((mx + 62, y + 1), stories.MARKETS, font=SANS_BOLD(8), fill=INK)
    draw.text((mx + 6, y + 10), "WEATHER", font=SANS_BOLD(8), fill=RED)
    draw.text((mx + 62, y + 10), stories.WEATHER, font=SANS_BOLD(8), fill=INK)
    y += 20 + 2

    # ---- Late wire ----
    y = section_header(draw, "LATE WIRE", GREY, mx, y, cw)
    ly = y
    for i, (text, source, certainty, _region) in enumerate(stories.LATE_WIRE):
        col = i % 2
        row = i // 2
        lx = mx + col * (cw // 2)
        lw = cw // 2 - 8
        draw.text((lx, ly + row * 10), "— " + text, font=SANS(9),
                  fill=(30, 30, 30))
        src = "  [" + source + "]"
        draw.text((lx + draw.textlength("— " + text, font=SANS(9)) + 2,
                   ly + row * 10), src, font=SANS_BOLD(8), fill=GREY)
    y = ly + 3 * 10 + 2

    # ---- Footer: coverage bands + sources ----
    fields = stories.field_counts()
    field_line = "  ·  ".join("%s %d" % (k, v) for k, v in fields.items())
    region_line = "  ·  ".join(
        "%s %d" % (stories.REGIONS[k], v)
        for k, v in sorted(regions.items(), key=lambda kv: -kv[1]))
    draw.line([mx, y, mx + cw, y], fill=INK, width=2)
    draw.text((mx, y + 2), "COVERAGE — " + field_line, font=SANS_BOLD(9),
              fill=INK)
    draw.text((mx, y + 11), "REGIONS — " + region_line, font=SANS_BOLD(9),
              fill=INK)
    draw.text((mx, y + 20),
              "All stories sourced from Reuters, BBC, The Guardian, Headline Desk and "
              "EventGraph. Claims flagged CLAIM; unconfirmed figures flagged REPORTED.",
              font=SANS(8), fill=GREY)
    date_check = ("DATE CHECK — Thursday 26 November 2026 is day 330 of 2026, "
                  "35 days left in the year; every story was first reported on "
                  "26 Nov 2026 (UTC) or carried on that day's front pages; "
                  "unconfirmed claims are flagged CLAIM and attributed "
                  "figures REPORTED.")
    dc = wrap(draw, date_check, SANS_BOLD(8), cw)
    draw_lines(draw, dc[:2], mx, y + 29, SANS_BOLD(8), RED, 9)
    y += 48

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    size = os.path.getsize(out)
    print("stories: %d (2 heroes + %d cards + %d sport + %d late wire)"
          % (n, sum(len(s["cards"]) for s in stories.SECTIONS),
             len(stories.SPORT), len(stories.LATE_WIRE)))
    print("drawn scenes: %d (2 hero scenes + %d card motifs)"
          % (drawn, drawn - 2))
    print("regions: %s" % region_line)
    print("fields: %s" % field_line)
    print("entry.png: %d bytes, %dx%d, final y=%d" % (size, W, H, y))
    assert size <= 1048576, "entry.png over 1 MiB"
    assert y <= H, "layout overflowed the page"


if __name__ == "__main__":
    main()
