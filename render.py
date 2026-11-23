#!/usr/bin/env python3
"""Render entry.png for news-image-20261122 v2 (build-time only, PIL allowed here).

A newspaper front page for Sunday 22 November 2026. The grader program
(main.ts) only copies this pre-rendered PNG; it never runs this script.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 20                      # margin
CW = W - 2 * M              # 984 content width

PAPER = (246, 240, 224)
INK = (26, 26, 26)
NAVY = (20, 38, 74)
NAVY2 = (44, 63, 102)
RED = (178, 35, 27)
GREY = (90, 90, 90)
RULE = (60, 60, 60)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SERIF = FD + "DejaVuSerif.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, lines, x, y, f, fill, lh, align="left", width=None):
    for line in lines:
        if align == "center":
            d.text((x + (width - d.textlength(line, font=f)) / 2, y), line,
                   font=f, fill=fill)
        else:
            d.text((x, y), line, font=f, fill=fill)
        y += lh
    return y


def hline(d, y, color=RULE, width=2, x0=M, x1=W - M):
    d.line([(x0, y), (x1, y)], fill=color, width=width)


def gradient(d, box, top, bottom):
    x0, y0, x1, y1 = box
    for yy in range(y0, y1):
        t = (yy - y0) / max(1, (y1 - y0 - 1))
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        d.line([(x0, yy), (x1, yy)], fill=c)


# ---------------------------------------------------------------- scenes
def scene_cop31(d, x, y, w, h):
    """Plenary hall: screen, rows of delegates, walking-out figures,
    cracked globe and a NO DEAL placard."""
    gradient(d, (x, y, x + w, y + h), (24, 42, 78), (52, 74, 116))
    # back screen
    d.rectangle([x + 18, y + 10, x + 330, y + 52], fill=(12, 24, 52),
                outline=(150, 170, 200), width=2)
    d.text((x + 34, y + 16), "COP31", font=font(SERIF_B, 26), fill=(255, 255, 255))
    d.text((x + 150, y + 24), "ANTALYA  •  FINAL PLENARY",
           font=font(SANS_B, 13), fill=(255, 196, 66))
    # podium
    d.polygon([(x + 150, y + 118), (x + 210, y + 118), (x + 200, y + h - 6),
               (x + 160, y + h - 6)], fill=(96, 70, 46))
    d.rectangle([x + 168, y + 96, x + 192, y + 118], fill=(30, 30, 30))
    d.ellipse([x + 174, y + 84, x + 186, y + 96], fill=(232, 190, 150))
    d.line([(x + 186, y + 96), (x + 196, y + 82)], fill=(220, 220, 220), width=2)
    # delegate rows: desks + heads
    cols = [(120, 140, 160), (200, 90, 70), (70, 130, 90), (190, 160, 60),
            (90, 110, 180), (220, 150, 120)]
    for r in range(3):
        yy = y + 66 + r * 30
        d.polygon([(x + 20, yy + 16), (x + 330, yy + 16), (x + 340, yy + 26),
                   (x + 10, yy + 26)], fill=(70, 88, 128))
        for c in range(7):
            cx = x + 40 + c * 44
            col = cols[(r * 7 + c) % len(cols)]
            d.ellipse([cx - 7, yy - 6, cx + 7, yy + 8], fill=(232, 190, 150))
            d.pieslice([cx - 11, yy + 6, cx + 11, yy + 22], 180, 360, fill=col)
    # empty tipped chairs, centre aisle
    for cx in (x + 380, x + 420):
        d.polygon([(cx, y + 118), (cx + 26, y + 118), (cx + 20, y + 150),
                   (cx - 6, y + 150)], fill=(120, 100, 70))
        d.line([(cx + 4, y + 118), (cx - 8, y + 96)], fill=(120, 100, 70), width=3)
    # walking-out silhouettes heading right
    for cx, col in ((x + 470, (16, 22, 40)), (x + 520, (40, 26, 26))):
        d.ellipse([cx - 8, y + 78, cx + 8, y + 94], fill=(232, 190, 150))
        d.polygon([(cx - 10, y + 94), (cx + 10, y + 94), (cx + 14, y + 140),
                   (cx - 14, y + 140)], fill=col)
        d.line([(cx - 6, y + 140), (cx - 12, y + h - 4)], fill=col, width=4)
        d.line([(cx + 6, y + 140), (cx + 14, y + h - 4)], fill=col, width=4)
    # cracked globe, right
    gx, gy, gr = x + w - 130, y + 84, 58
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(96, 150, 190),
              outline=(220, 230, 240), width=3)
    d.ellipse([gx - 34, gy - 40, gx + 6, gy - 8], fill=(110, 170, 110))
    d.ellipse([gx - 6, gy + 6, gx + 38, gy + 40], fill=(110, 170, 110))
    d.ellipse([gx + 18, gy - 44, gx + 44, gy - 18], fill=(110, 170, 110))
    d.line([(gx - 30, gy - 52), (gx - 12, gy - 20), (gx - 26, gy + 6),
            (gx + 2, gy + 30), (gx - 8, gy + 54)], fill=(20, 20, 20), width=4)
    d.line([(gx - 12, gy - 20), (gx + 14, gy - 34)], fill=(20, 20, 20), width=3)
    # NO DEAL placard
    px, py = x + 600, y + 16
    d.rectangle([px, py, px + 168, py + 44], fill=RED, outline=(255, 255, 255),
                width=2)
    d.text((px + 14, py + 8), "NO DEAL", font=font(SANS_B, 28), fill=(255, 255, 255))
    d.line([(px + 84, py + 44), (px + 84, py + 66)], fill=(220, 220, 220), width=4)


def scene_peru(d, x, y, w, h):
    gradient(d, (x, y, x + w, y + h), (186, 214, 232), (232, 238, 242))
    d.ellipse([x + w - 46, y + 8, x + w - 14, y + 40], fill=(255, 214, 120))
    d.polygon([(x, y + 58), (x + 80, y + 18), (x + 150, y + 58)],
              fill=(125, 148, 168))
    d.polygon([(x + 60, y + 30), (x + 80, y + 18), (x + 100, y + 30),
               (x + 88, y + 38), (x + 72, y + 38)], fill=(255, 255, 255))
    d.polygon([(x + 90, y + h), (x + 180, y + 26), (x + 260, y + h)],
              fill=(91, 114, 136))
    d.polygon([(x + 158, y + 40), (x + 180, y + 26), (x + 202, y + 40),
               (x + 190, y + 48), (x + 170, y + 48)], fill=(255, 255, 255))
    d.polygon([(x + 190, y + h), (x + 265, y + 44), (x + w, y + h)],
              fill=(60, 84, 104))
    # crack down the front slope
    d.line([(x + 250, y + 48), (x + 238, y + 62), (x + 252, y + 74),
            (x + 240, y + 88), (x + 250, y + h)], fill=(30, 30, 30), width=3)
    # shaking city at the foot
    for i, bh in enumerate((26, 34, 22, 30, 18)):
        bx = x + 12 + i * 30
        d.rectangle([bx, y + h - bh, bx + 24, y + h], fill=(46, 42, 38))
        d.rectangle([bx + 5, y + h - bh + 5, bx + 10, y + h - bh + 10],
                    fill=(255, 214, 120))
    for sx in (x + 30, x + 120, x + 210):
        d.line([(sx, y + h - 44), (sx + 8, y + h - 50), (sx + 16, y + h - 44)],
               fill=(178, 35, 27), width=2)


def scene_mexico(d, x, y, w, h):
    gradient(d, (x, y, x + w, y + h), (22, 35, 61), (16, 24, 44))
    # house
    d.polygon([(x + 30, y + 52), (x + 90, y + 30), (x + 150, y + 52)],
              fill=(10, 16, 32))
    d.rectangle([x + 38, y + 52, x + 142, y + h - 8], fill=(13, 21, 38))
    for wx in (x + 50, x + 82, x + 114):
        d.rectangle([wx, y + 62, wx + 16, y + 78], fill=(255, 214, 120))
    d.rectangle([x + 82, y + 80, x + 100, y + h - 8], fill=(30, 22, 16))
    # helicopter + searchlight
    hx, hy = x + 225, y + 22
    d.ellipse([hx - 26, hy, hx + 26, hy + 20], fill=(40, 44, 52))
    d.rectangle([hx + 20, hy + 6, hx + 58, hy + 14], fill=(40, 44, 52))
    d.line([(hx - 34, hy - 2), (hx + 34, hy - 2)], fill=(200, 200, 200), width=3)
    d.line([(hx - 30, hy - 6), (hx + 30, hy - 6)], fill=(200, 200, 200), width=2)
    d.polygon([(hx - 12, hy + 20), (hx + 12, hy + 20), (hx + 26, y + 52),
               (hx - 26, y + 52)], fill=(255, 240, 170))
    d.ellipse([hx - 4, hy + 4, hx + 6, hy + 14], fill=(255, 214, 120))
    # handcuffs, foreground right
    for cx in (x + 205, x + 255):
        d.ellipse([cx - 17, y + h - 34, cx + 17, y + h], outline=(212, 175, 55),
                  width=5)
    d.line([(x + 222, y + h - 17), (x + 238, y + h - 17)], fill=(212, 175, 55),
           width=4)
    # red / blue raid lights
    d.ellipse([x + 16, y + 12, x + 28, y + 24], fill=(255, 60, 50))
    d.ellipse([x + 34, y + 12, x + 46, y + 24], fill=(70, 120, 255))


def scene_gulf(d, x, y, w, h):
    gradient(d, (x, y, x + w, y + h), (188, 212, 230), (240, 200, 140))
    # missile trails (kept inside the panel)
    d.arc([x + 190, y + 2, x + 300, y + 58], 180, 360, fill=(255, 255, 255),
          width=3)
    d.arc([x + 212, y + 10, x + 314, y + 66], 180, 360, fill=(255, 255, 255),
          width=3)
    d.ellipse([x + 296, y + 26, x + 306, y + 36], fill=(255, 220, 90))
    d.ellipse([x + 306, y + 32, x + 314, y + 40], fill=(255, 220, 90))
    # industrial facility, left
    d.rectangle([x + 8, y + 52, x + 120, y + h - 22], fill=(52, 52, 56))
    d.rectangle([x + 20, y + 30, x + 30, y + 52], fill=(52, 52, 56))
    d.rectangle([x + 44, y + 38, x + 52, y + 52], fill=(52, 52, 56))
    d.ellipse([x + 128, y + 44, x + 168, y + 76], fill=(70, 70, 74))
    # flames on a tank
    fx = x + 138
    d.polygon([(fx, y + 62), (fx + 8, y + 40), (fx + 16, y + 54), (fx + 24, y + 34),
               (fx + 32, y + 54), (fx + 40, y + 42), (fx + 48, y + 62)],
              fill=(255, 140, 30))
    d.polygon([(fx + 10, y + 62), (fx + 18, y + 48), (fx + 26, y + 58),
               (fx + 34, y + 46), (fx + 40, y + 62)], fill=(255, 220, 90))
    # smoke
    for sx, sy, r in ((x + 150, y + 30, 12), (x + 168, y + 20, 10),
                      (x + 182, y + 30, 9)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(120, 120, 120))
    # sea + tanker
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(47, 111, 143))
    d.polygon([(x + 200, y + h - 22), (x + 310, y + h - 22), (x + 300, y + h - 8),
               (x + 210, y + h - 8)], fill=(20, 24, 30))
    d.rectangle([x + 282, y + h - 34, x + 302, y + h - 22], fill=(220, 220, 220))
    d.line([(x + 292, y + h - 46), (x + 292, y + h - 34)], fill=(20, 24, 30),
           width=2)


def scene_mercury(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(14, 18, 38))
    for sx, sy in ((x + 20, y + 14), (x + 60, y + 30), (x + 250, y + 12),
                   (x + 290, y + 40), (x + 40, y + 70), (x + 300, y + 78)):
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    # sun glow, top left (kept inside the panel)
    d.ellipse([x + 4, y + 4, x + 32, y + 32], fill=(255, 200, 80))
    d.ellipse([x + 10, y + 10, x + 26, y + 26], fill=(255, 230, 150))
    # Mercury
    px, py, pr = x + 190, y + 52, 34
    d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(184, 168, 143),
              outline=(230, 220, 205), width=2)
    for cx, cy, cr in ((px - 14, py - 10, 7), (px + 10, py + 6, 9),
                       (px + 2, py - 20, 5), (px - 2, py + 18, 6),
                       (px + 18, py - 14, 4)):
        d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(150, 134, 110))
    # orbit + spacecraft
    d.ellipse([x + 90, y + 6, x + 300, y + 96], outline=(200, 210, 230), width=2)
    sx, sy = x + 268, y + 22
    d.rectangle([sx - 8, sy - 5, sx + 8, sy + 5], fill=(220, 225, 235))
    d.rectangle([sx - 34, sy - 3, sx - 10, sy + 3], fill=(60, 110, 200))
    d.rectangle([sx + 10, sy - 3, sx + 34, sy + 3], fill=(60, 110, 200))
    d.line([(sx - 8, sy), (sx - 34, sy)], fill=(200, 200, 200), width=2)
    d.line([(sx + 8, sy), (sx + 34, sy)], fill=(200, 200, 200), width=2)
    d.text((x + 12, y + h - 20), "8 YEARS  •  10 BILLION KM",
           font=font(SANS_B, 11), fill=(255, 255, 255))


def scene_ukraine(d, x, y, w, h):
    gradient(d, (x, y, x + w, y + h), (154, 165, 173), (210, 208, 200))
    # apartment block, damaged top-right corner
    bx, by, bw, bh = x + 60, y + 14, 180, h - 26
    d.rectangle([bx, by, bx + bw, by + bh], fill=(138, 127, 116))
    d.polygon([(bx + bw, by), (bx + bw, by + 34), (bx + bw - 46, by + 34),
               (bx + bw - 30, by + 18), (bx + bw - 14, by + 26)],
              fill=(40, 36, 32))
    for r in range(5):
        for c in range(6):
            wx = bx + 12 + c * 28
            wy = by + 10 + r * 14
            if r == 0 and c >= 4:
                continue
            lit = (r * 6 + c) % 4 == 0
            d.rectangle([wx, wy, wx + 16, wy + 9],
                        fill=(255, 214, 120) if lit else (52, 48, 44))
    # smoke from the damage
    for sx, sy, r in ((bx + bw - 10, by - 2, 12), (bx + bw + 6, by - 10, 9),
                      (bx + bw - 26, by - 10, 8)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(110, 110, 110))
    # rubble + searchlight
    d.polygon([(x + 40, y + h), (x + 90, y + h - 16), (x + 140, y + h)],
              fill=(90, 84, 76))
    d.polygon([(x + 250, y + h - 12), (x + 290, y + h - 26), (x + w, y + h - 12),
               (x + w, y + h)], fill=(90, 84, 76))
    d.polygon([(x + 10, y + h), (x + 30, y + h), (x + 130, y + 30),
               (x + 110, y + 26)], fill=(255, 240, 180))


def scene_borders(d, x, y, w, h):
    # left: Estonia border barrier; right: Danish + Estonian flags
    mid = x + w // 2
    gradient(d, (x, y, mid, y + h), (200, 214, 224), (232, 236, 238))
    d.rectangle([x, y + h - 26, mid, y + h], fill=(110, 110, 110))
    d.line([(x, y + h - 26), (mid, y + h - 26)], fill=(255, 255, 255), width=2)
    for fx in range(x + 8, mid - 6, 22):
        d.line([(fx, y + 34), (fx, y + h - 26)], fill=(90, 90, 90), width=3)
    # striped barrier arm
    d.polygon([(x + 10, y + 40), (mid - 10, y + 22), (mid - 10, y + 32),
               (x + 10, y + 50)], fill=(255, 255, 255))
    for i in range(6):
        sx0 = x + 10 + i * 24
        d.polygon([(sx0, y + 48 - i * 3), (sx0 + 12, y + 45 - i * 3),
                   (sx0 + 12, y + 36 - i * 3), (sx0, y + 39 - i * 3)],
                  fill=RED)
    d.rectangle([x + 34, y + 62, x + 118, y + 88], fill=(255, 255, 255),
                outline=RED, width=3)
    d.text((x + 44, y + 67), "CLOSED", font=font(SANS_B, 16), fill=RED)
    # right: flags
    d.rectangle([mid, y, x + w, y + h], fill=(240, 238, 230))
    # Danish flag
    fx, fy = mid + 16, y + 16
    d.rectangle([fx, fy, fx + 62, fy + 42], fill=(200, 16, 46))
    d.rectangle([fx + 18, fy, fx + 26, fy + 42], fill=(255, 255, 255))
    d.rectangle([fx, fy + 17, fx + 62, fy + 25], fill=(255, 255, 255))
    d.line([(fx + 31, fy + 42), (fx + 31, fy + 58)], fill=(120, 120, 120), width=3)
    d.text((fx, fy + 60), "DENMARK", font=font(SANS_B, 10), fill=INK)
    # Estonian flag
    ex, ey = mid + 92, y + 16
    d.rectangle([ex, ey, ex + 62, ey + 42], outline=(120, 120, 120), width=1)
    d.rectangle([ex, ey, ex + 62, ey + 14], fill=(0, 114, 206))
    d.rectangle([ex, ey + 14, ex + 62, ey + 28], fill=(20, 20, 20))
    d.rectangle([ex, ey + 28, ex + 62, ey + 42], fill=(255, 255, 255))
    d.line([(ex + 31, ey + 42), (ex + 31, ey + 58)], fill=(120, 120, 120), width=3)
    d.text((ex, ey + 60), "ESTONIA", font=font(SANS_B, 10), fill=INK)


# ---------------------------------------------------------------- world map
CONTINENTS = {
    "namerica": [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 80),
                 (-80, 73), (-75, 62), (-65, 60), (-55, 47), (-70, 42),
                 (-75, 35), (-80, 26), (-90, 21), (-97, 16), (-105, 20),
                 (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-155, 58),
                 (-165, 60)],
    "greenland": [(-45, 60), (-30, 68), (-20, 70), (-30, 76), (-55, 76),
                  (-58, 70)],
    "samerica": [(-80, 10), (-75, 5), (-60, 0), (-50, 0), (-40, -5),
                 (-35, -8), (-40, -20), (-48, -28), (-58, -38), (-65, -45),
                 (-70, -55), (-73, -40), (-73, -25), (-80, -15), (-80, -5)],
    "europe": [(-10, 36), (-2, 37), (3, 38), (10, 38), (18, 40), (23, 36),
               (28, 41), (30, 46), (20, 45), (12, 44), (8, 44), (3, 43),
               (-2, 44), (-5, 48), (-2, 50), (5, 53), (8, 57), (10, 59),
               (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (25, 65),
               (20, 70), (15, 70), (10, 64), (5, 58), (0, 52), (-5, 50),
               (-10, 43)],
    "africa": [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31),
               (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (35, -18),
               (32, -28), (20, -35), (15, -27), (12, -18), (9, -1), (9, 4),
               (-8, 4), (-13, 8), (-17, 12)],
    "asia": [(30, 62), (40, 68), (60, 69), (70, 72), (90, 75), (110, 76),
             (130, 72), (160, 70), (178, 66), (170, 60), (162, 55),
             (158, 50), (142, 45), (140, 40), (130, 33), (122, 30),
             (120, 25), (110, 20), (105, 10), (100, 8), (95, 15), (90, 22),
             (85, 20), (80, 13), (77, 8), (72, 20), (66, 25), (60, 25),
             (57, 26), (52, 28), (48, 30), (44, 29), (40, 31), (36, 36),
             (30, 36), (28, 41), (26, 40)],
    "australia": [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32),
                  (135, -35), (140, -38), (145, -38), (150, -37), (153, -27),
                  (146, -19), (142, -11), (136, -12), (132, -12), (126, -14),
                  (122, -17), (114, -22)],
}
# (number, lon, lat, label)
PLACES = [
    (1, 30.7, 36.9, "ANTALYA"), (2, -76.0, -11.0, "JUNIN, PERU"),
    (3, -108.0, 25.0, "SINALOA"), (4, 50.5, 26.2, "BAHRAIN"),
    (5, 30.5, 50.8, "DYMER"), (6, 25.0, 59.0, "ESTONIA"),
    (7, 10.0, 56.0, "DENMARK"), (8, 106.0, -6.2, "CIKANDE"),
    (9, 8.0, 9.5, "NIGERIA"),
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(223, 233, 239),
                outline=(150, 160, 170), width=1)

    def px(lon, lat):
        return (x + (lon + 180) / 360 * w, y + (75 - lat) / 130 * h)

    for pts in CONTINENTS.values():
        d.polygon([px(lon, lat) for lon, lat in pts], fill=(186, 172, 136),
                  outline=(118, 108, 82))
    fnum = font(SANS_B, 11)
    for num, lon, lat, _label in PLACES:
        cx, cy = px(lon, lat)
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED,
                  outline=(255, 255, 255), width=1)
        tw = d.textlength(str(num), font=fnum)
        d.text((cx - tw / 2, cy - 6), str(num), font=fnum, fill=(255, 255, 255))


# ---------------------------------------------------------------- columns
def column(img, d, x, y, w, kicker, headline, body, scene, max_head_lines=2,
           art_h=92, max_body=3):
    f_kick = font(SANS_B, 14)
    f_head = font(SANS_B, 21)
    f_body = font(SANS, 13)
    d.text((x, y), kicker, font=f_kick, fill=RED)
    hl = wrap(d, headline, f_head, w)
    assert len(hl) <= max_head_lines, (headline, hl)
    draw_lines(d, hl, x, y + 20, f_head, INK, 22)
    ay = y + 20 + len(hl) * 22 + 6
    d.rectangle([x, ay, x + w, ay + art_h], outline=(120, 120, 120), width=1)
    # render the scene on its own tile so nothing can spill past the border
    panel = Image.new("RGB", (w - 2, art_h - 2), (255, 255, 255))
    pd = ImageDraw.Draw(panel)
    scene(pd, 0, 0, w - 2, art_h - 2)
    img.paste(panel, (x + 1, ay + 1))
    bl = wrap(d, body, f_body, w)
    assert len(bl) <= max_body, (body, bl)
    draw_lines(d, bl, x, ay + art_h + 6, f_body, INK, 15)
    return ay + art_h + 6 + len(bl) * 15


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    hline(d, 8, width=3)
    f_mast = font(SERIF_B, 56)
    t = "THE WORLD TODAY"
    d.text(((W - d.textlength(t, font=f_mast)) / 2, 12), t, font=f_mast,
           fill=NAVY)
    f_date = font(SANS_B, 15)
    t2 = "SUNDAY, 22 NOVEMBER 2026  •  ONE DAY, ONE PAGE, THE WORLD'S NEWS"
    d.text(((W - d.textlength(t2, font=f_date)) / 2, 74), t2, font=f_date,
           fill=INK)
    hline(d, 94, width=2)

    # ---- lead: COP31 collapse
    d.text((M, 102), "CLIMATE SUMMIT  •  ANTALYA, TURKEY",
           font=font(SANS_B, 16), fill=RED)
    f_lead = font(SERIF_B, 33)
    t3 = "COP31 COLLAPSES — NO DEAL ON FOSSIL FUELS"
    assert d.textlength(t3, font=f_lead) <= CW, d.textlength(t3, font=f_lead)
    d.text((M, 124), t3, font=f_lead, fill=INK)
    d.rectangle([M, 168, M + CW, 168 + 150], outline=(120, 120, 120), width=1)
    panel = Image.new("RGB", (CW - 2, 148), (255, 255, 255))
    pd = ImageDraw.Draw(panel)
    scene_cop31(pd, 0, 0, CW - 2, 148)
    img.paste(panel, (M + 1, 169))
    f_cap = font(SANS, 15)
    cap = ("EU and allies reject the “Antalya Pact” draft — it never mentions "
           "fossil fuels. Longest COP ever; first major collapse since "
           "Copenhagen 2009. President Murat Kurum concedes: no consensus.")
    cl = wrap(d, cap, f_cap, CW)
    assert len(cl) <= 2, cl
    draw_lines(d, cl, M, 324, f_cap, INK, 17)
    hline(d, 366, width=2)

    # ---- row 2
    y2 = 374
    column(img, d, M, y2, 320, "EARTHQUAKE  •  PERU",
           "M6.9 QUAKE SHAKES THE ANDES",
           "Epicentre 34 km north of Junín, 108 km deep. Felt in Lima; "
           "residents fled into the streets. No damage or casualties reported.",
           scene_peru, max_body=4)
    column(img, d, M + 332, y2, 320, "DRUG WAR  •  MEXICO",
           "“EL CHAPO ISIDRO” CAPTURED",
           "Special forces seize FBI Ten Most Wanted boss Fausto Isidro Meza "
           "Flores in Guasave, Sinaloa. 11 killed in the raid; flown to "
           "Mexico City.",
           scene_mexico, max_body=4)
    column(img, d, M + 664, y2, 320, "GULF CRISIS  •  BAHRAIN",
           "IRAN STRIKES BAHRAIN",
           "Missiles and drones set a civilian facility in Sitra ablaze; 2 "
           "hurt. IRGC claims it hit US positions and Patriot radars — "
           "unverified. Tankers hit in Hormuz.",
           scene_gulf, max_body=4)
    hline(d, 606, width=2)

    # ---- row 3
    y3 = 612
    column(img, d, M, y3, 320, "SPACE  •  MERCURY",
           "BEPICOLOMBO REACHES MERCURY",
           "After an 8-year, 10-billion-km trip, the craft slips into "
           "Mercury orbit — only the third mission there. Its burn fell short.",
           scene_mercury)
    column(img, d, M + 332, y3, 320, "WAR  •  UKRAINE",
           "DRONE HITS FLATS NEAR KYIV",
           "A Russian drone hits a five-storey block in Dymer; 14 missing, "
           "2 killed. A missile on Kryvyi Rih kills 2; 60 wounded.",
           scene_ukraine)
    column(img, d, M + 664, y3, 320, "EUROPE  •  BORDERS",
           "ESTONIA SHUTS BORDER; DENMARK EXPELS ENVOY",
           "Estonia closes five Russia crossings for six months after a GRU "
           "arson plot. Denmark expels a diplomat over an assassination plot.",
           scene_borders)
    hline(d, 832, width=2)

    # ---- world map band
    d.text((M, 840), "WHERE THE NEWS HAPPENED",
           font=font(SANS_B, 14), fill=NAVY)
    note = "★  BEPICOLOMBO NOW ORBITS MERCURY"
    d.text((W - M - d.textlength(note, font=font(SANS_B, 12)), 842), note,
           font=font(SANS_B, 12), fill=RED)
    draw_map(d, M, 858, CW, 70)
    f_leg = font(SANS, 12)
    legend = ("1 ANTALYA   2 JUNÍN, PERU   3 SINALOA, MEXICO   4 BAHRAIN   "
              "5 DYMER, UKRAINE   6 ESTONIA   7 DENMARK   8 CIKANDE, "
              "INDONESIA   9 NIGERIA")
    assert d.textlength(legend, font=f_leg) <= CW, d.textlength(legend,
                                                               font=f_leg)
    d.text((M, 932), legend, font=f_leg, fill=INK)
    hline(d, 950, width=2)

    # ---- also today
    d.text((M, 958), "ALSO TODAY — 22 NOVEMBER 2026",
           font=font(SANS_B, 15), fill=NAVY)
    f_also = font(SANS, 12)
    left = [
        "Indonesia: candy-factory fire in Cikande kills 3, ~36 missing.",
        "Nigeria: boat capsizes en route to a funeral; 24 dead.",
        "FBI investigates apparent hack of its criminal database.",
        "Markets: S&P 500 -3.7%, Nasdaq -5.3% Friday — correction.",
    ]
    right = [
        "Israel: president taps Eisenkot to form a government.",
        "West Bank: settlers torch vehicles in four villages; inquiry opened.",
        "UK and EU strike post-Brexit closer-ties deal.",
    ]
    for i, line in enumerate(left):
        d.text((M, 974 + i * 12), "▪  " + line, font=f_also, fill=INK)
    for i, line in enumerate(right):
        d.text((M + 500, 974 + i * 12), "▪  " + line, font=f_also, fill=INK)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
