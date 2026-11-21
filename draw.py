# draw.py - Variant E "THE GLOBAL WIRE" - News Image entry, Saturday 21 Nov 2026.
# Wire-service monochrome: white page, ink black, grays, one red accent.
# Deterministic Pillow program (stdlib + PIL only, no network).
# Draws a 1024x1024 page and saves entry.png next to this file.
import os
from PIL import Image, ImageDraw, ImageFont
from mapdata import WORLD

BASE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(BASE, "fonts")


def PF(s):
    return ImageFont.truetype(os.path.join(FD, "PlayfairDisplay-900.ttf"), s)


def AB(s):
    return ImageFont.truetype(os.path.join(FD, "Archivo-Bold.ttf"), s)


def AM(s):
    return ImageFont.truetype(os.path.join(FD, "Archivo-Medium.ttf"), s)


INK = (17, 17, 17)
WHITE = (255, 255, 255)
LGRAY = (237, 237, 237)
MGRAY = (74, 74, 74)
GRAY2 = (198, 198, 198)
LAND = (207, 207, 207)
RED = (192, 57, 43)

REG = {
    "EUROPE": (176, 58, 46),
    "ASIA": (29, 111, 184),
    "MIDEAST": (125, 60, 152),
    "AFRICA": (30, 132, 73),
    "AMERICAS": (202, 111, 30),
    "OCEANIA": (20, 143, 119),
    "GLOBAL": (93, 109, 126),
}

W = H = 1024
M = 16            # page margin
CW = W - 2 * M    # content width = 992


def tw(d, s, f):
    return d.textlength(s, font=f)


def wrap(d, s, f, maxw):
    """Greedy word wrap; returns list of lines that each fit maxw."""
    lines, cur = [], ""
    for word in s.split():
        trial = word if not cur else cur + " " + word
        if tw(d, trial, f) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_font(d, s, maker, size, maxw, minsize=8):
    """Largest maker(size) font, stepping down, whose text fits maxw."""
    f = maker(size)
    while size > minsize and tw(d, s, f) > maxw:
        size -= 1
        f = maker(size)
    return f


def T(d, x, y, s, f, fill=INK, anchor="la"):
    d.text((x, y), s, font=f, fill=fill, anchor=anchor)


def rule(d, x0, x1, y, fill=INK, wdt=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=wdt)


def vrule(d, x, y0, y1, fill=INK, wdt=1):
    d.line([(x, y0), (x, y1)], fill=fill, width=wdt)

# ---------------------------------------------------------------- data ----
NUMBERS = [
    ("3", "weapons cross into Poland: two missiles and a jet drone"),
    ("42", "injured in the Kryvyi Rih strike, four of them children"),
    ("-5.28%", "Nasdaq's fall at Friday's close"),
    ("372,000", "people moved to shelters as Akvan hit"),
    ("€1BN", "EU military aid adopted for Ukraine"),
    ("159/1", "India at stumps in Wellington"),
]

TIMELINE = [
    ("Overnight", "Kryvyi Rih strike: two killed, 42 injured"),
    ("Morning", "Rutte flies to Warsaw over the missiles"),
    ("Midday", "Antalya: third COP31 draft due after overnight talks"),
    ("Afternoon", "Denmark expels the Russian attache"),
    ("Evening", "Stumps in Wellington: India 159/1"),
]

REGION_COUNTS = [
    ("EUROPE", 16), ("ASIA", 6), ("MIDEAST", 6), ("AFRICA", 1),
    ("AMERICAS", 8), ("OCEANIA", 1), ("GLOBAL", 2),
]

# no, place, region, topic, headline, deck (verbatim + sources), source tag,
# data label, caption band, pin lon, pin lat
CARDS = [
    (1, "WARSAW, POLAND", "EUROPE", "SECURITY",
     "Rutte flies to Warsaw after missiles land",
     "Two missiles and a suspected jet drone came down in the south-east, "
     "a Kh-101 near Nowy Lipowiec. Rutte calls it a \u201cgrave "
     "violation\u201d; Tusk a deliberate provocation. (AP)",
     "AP - SOFX", "3 WEAPONS CROSS", "WARSAW - EMERGENCY TALKS",
     21.0, 52.2),
    (2, "ANTALYA", "GLOBAL", "CLIMATE",
     "COP31 runs into overtime with no deal yet",
     "Talks ran past Friday's close into Saturday. The draft drops every "
     "fossil-fuel reference and the $120bn finance target; a third draft "
     "is due this morning. (AP)",
     "Ongoing - AP", "NO DEAL YET", "ANTALYA - COP31 OVERTIME",
     30.7, 36.9),
    (3, "NEW YORK", "AMERICAS", "MARKETS",
     "Wall Street enters correction as AI rout deepens",
     "The S&P 500 fell about 3.7% on Friday, pushing it into correction "
     "territory. The Nasdaq dropped 5.28% as chip and AI shares plunged. "
     "(SimpleLife)",
     "Friday's close", "NASDAQ -5.28%", "NEW YORK - FRIDAY'S CLOSE",
     -74.0, 40.7),
    (4, "KRYVYI RIH", "EUROPE", "WAR",
     "Russian strike kills two, injures 42",
     "An overnight strike kills two and injures 42, four of them "
     "children, the city's military chief says. (AppiStos)",
     "City chief says", "2 DEAD - 42 HURT", "KRYVYI RIH - OVERNIGHT STRIKE",
     33.4, 47.9),
    (5, "COPENHAGEN", "EUROPE", "SECURITY",
     "Denmark exposes 'assassination plot'",
     "Russia \u2018planned and initiated\u2019 a bid to kill a "
     "Ukrainian-American rapper near Copenhagen, Denmark says. (BBC)",
     "Denmark says - BBC", "ATTACHE\nEXPELLED", "COPENHAGEN - PLOT EXPOSED",
     12.6, 55.7),
    (6, "KYIV", "EUROPE", "WAR",
     "Russia's barrage: 400 drones, 110 missiles",
     "Eight dead across Ukraine; Austria's embassy is hit in Kyiv. "
     "France seeks a UN Security Council meeting. (BBC)",
     "Officials' count", "400 DRONES -\n110 MISSILES",
     "KYIV - OVERNIGHT BARRAGE",
     30.5, 50.4),
    (7, "ODISHA, INDIA", "ASIA", "CYCLONE",
     "After Akvan: 372,000 moved, no deaths",
     "A day after landfall, no deaths are reported and relief is under "
     "way. Schools stay shut through Saturday. (Ridhu Times)",
     "Relief reports", "372,000 MOVED", "ODISHA - AKVAN AFTERMATH",
     84.9, 19.3),
    (8, "BRUSSELS", "EUROPE", "AID",
     "EU adopts 1bn euro military aid for Ukraine",
     "Joint buying runs via the Peace Facility. Britain pledges 1,000+ "
     "drones in a 260m-pound package. (Reuters)",
     "Adopted - EU", "€1BN ADOPTED", "BRUSSELS - AID ADOPTED",
     4.3, 50.8),
    (9, "NEW YORK", "AMERICAS", "CYBER",
     "JPMorgan, Visa, Mastercard cyberattack",
     "The banks report vendor incidents. Their core payment networks "
     "are unaffected, they say. (Reuters)",
     "Banks say", "3 NETWORKS HIT", "NEW YORK - VENDOR INCIDENTS",
     -73.9, 40.8),
    (10, "ULAANBAATAR", "ASIA", "POLITICS",
     "Mongolia's president resigns",
     "The resignation sets the stage for a snap election. It caps a "
     "week of political turmoil in the capital. (Reuters)",
     "Capital reports", "SNAP ELECTION NEXT", "ULAANBAATAR - RESIGNATION",
     106.9, 47.9),
    (11, "THE HAGUE", "GLOBAL", "COURT",
     "Myanmar ruling rattles Israel's Gaza defence",
     "The genocide verdict on Myanmar raises questions in Jerusalem "
     "over Israel's own case, experts say. (BBC)",
     "Experts say", "GENOCIDE VERDICT", "THE HAGUE - WORLD COURT",
     4.3, 52.1),
    (12, "JOHANNESBURG", "AFRICA", "ELECTION",
     "ANC scrambles after worst result since 1994",
     "The ANC wins 31% of the vote, its worst since 1994. It now races "
     "for coalition deals to stay in government. (BBC)",
     "Count - BBC", "ANC 31%", "JOHANNESBURG - THE COUNT",
     28.0, -26.2),
    (13, "WELLINGTON", "OCEANIA", "SPORT",
     "India fight back: 159/1 at stumps, day two",
     "India trail by 209 after the hosts made 368. Nicholls made 175 "
     "not out for the hosts. (ICC)",
     "Scorecard - ICC", "159/1 - DAY TWO", "WELLINGTON - DAY TWO",
     174.8, -41.3),
]

# no, text (verbatim from POOL21, source in parens), region, pin lon, pin lat
BRIEFS = [
    (14, "Kathmandu Nepal's new leader Balendra Shah faces an India "
     "test (BBC)", "ASIA", 85.3, 27.7),
    (15, "Washington US releases more UFO footage filmed in the Middle "
     "East (BBC)", "AMERICAS", -77.0, 38.9),
    (16, "Los Angeles Hyundai unveils the 2027 Elantra at the auto "
     "show (Fast Company)", "AMERICAS", -118.2, 34.1),
    (17, "Cardiff Lauren Price beats Kotaskova to become undisputed "
     "champion (BBC)", "EUROPE", -3.2, 51.5),
    (18, "Paris Three police are sentenced over the beating of Michel "
     "Zecler (BBC)", "EUROPE", 2.4, 48.9),
    (19, "Oxford Life, 22 years minimum, for the Thames drowning "
     "murder (BBC)", "EUROPE", -1.3, 51.8),
    (20, "New York Nikhil Gupta gets 19+ years over the Sikh murder "
     "plot (BBC)", "AMERICAS", -74.0, 40.7),
    (21, "Cincinnati Fiona the hippo dies after eating a hat (AP)",
     "AMERICAS", -84.5, 39.1),
    (22, "Washington US sanctions four Iranians over oil revenues "
     "(OFAC)", "AMERICAS", -77.1, 38.8),
    (23, "Hormuz A tanker is struck and on fire in the Strait of "
     "Hormuz (UKMTO)", "MIDEAST", 56.3, 26.6),
    (24, "Los Angeles A jury convicts the man who started the "
     "Palisades Fire (AP)", "AMERICAS", -118.3, 34.0),
    (25, "Frankfurt ECB names Boone and Brunnermeier for its Executive "
     "Board (Reuters)", "EUROPE", 8.7, 50.1),
    (26, "Buenos Aires Argentina's Senate backs a disability "
     "framework, 71-0 (AP)", "AMERICAS", -58.4, -34.6),
    (27, "Riyadh A Saudi coalition intercepts Houthi missiles over "
     "Riyadh (Reuters)", "MIDEAST", 46.7, 24.6),
    (28, "Barcelona A pill is hailed as a breakthrough for pancreatic "
     "cancer (Reuters)", "EUROPE", 2.2, 41.4),
    (29, "Gaza On World Children's Day, Palestinian children appeal "
     "for help (UN)", "MIDEAST", 34.3, 31.5),
    (30, "Madrid Amnesty says Spanish police used excess force in the "
     "strike (AP)", "EUROPE", -3.7, 40.4),
    (31, "Rome Italian workers and students march against Meloni's "
     "government (AFP)", "EUROPE", 12.5, 41.9),
    (32, "Jeddah Saudi Arabia warns of thunderstorms through Tuesday "
     "(SPA)", "MIDEAST", 39.2, 21.5),
    (33, "Kuala Lumpur Malaysia to send 10,000 Rohingya to Turkey for "
     "training (Reuters)", "ASIA", 101.7, 3.1),
    (34, 'Kharkiv Ukraine says it has finished a "Bear Trap" in the '
     "Kharkiv area (Ukrinform)", "EUROPE", 36.2, 49.9),
    (35, "Islamabad Pakistan's minerals are worth $8-10 trillion, its "
     "minister says (Reuters)", "ASIA", 73.1, 33.7),
    (36, "Singapore US presses Singapore and Malaysia on Iran "
     "sanctions (Reuters)", "ASIA", 103.8, 1.35),
    (37, "Paris France seeks a UN council meeting on the Kyiv strikes "
     "(AFP)", "EUROPE", 2.3, 48.8),
    (38, "Kyiv The war tally: 771 Ukrainians killed, 2,300+ missing "
     "(homevo)", "EUROPE", 30.6, 50.5),
    (39, "Ankara Turkey welcomes the World Court's Myanmar ruling "
     "(Anadolu)", "MIDEAST", 32.9, 39.9),
    (40, "Turin ATP semis are set: Alcaraz v Shelton, Zverev v "
     "Medvedev (ATP)", "EUROPE", 7.7, 45.1),
]

DATECHECK = (
    "Left out as Friday 20 November's news: Kyiv's three bridges hit, "
    "Akvan's landfall at Gopalpur, COP31's final day ending with no deal, "
    "Asia's AI sell-off (Taipei -6.2%), the UK-EU reset deal, Phillips's 118. "
    "Not yet happened: final COP31 text, ATP semi results, BepiColombo's "
    "Mercury orbit entry (due today)."
)

FOOTER_L = ("Every story here happened, or was first reported, on Saturday "
            "21 November 2026. Contested claims are attributed.")
FOOTER_R = "Sources named beside each story - original drawings"

# ------------------------------------------------------------- scenes -----
# Each scene draws inside (x, y, w, h): flat gray shapes; red is reserved
# for the data element of the story.
def scene1(d, x, y, w, h):  # Kyiv: river, three bridges, red missile arcs
    d.polygon([(x, y + h * 0.62), (x + w * 0.45, y + h * 0.45),
               (x + w, y + h * 0.72), (x + w, y + h), (x, y + h)],
              fill=GRAY2)
    for i, bx in enumerate((0.14, 0.47, 0.78)):
        by = y + h * (0.52 + 0.07 * i)
        d.line([(x + w * bx, by), (x + w * (bx + 0.2), by)], fill=INK, width=3)
        d.line([(x + w * (bx + 0.04), by), (x + w * (bx + 0.04), by + h * 0.3)],
               fill=INK, width=2)
        d.line([(x + w * (bx + 0.16), by), (x + w * (bx + 0.16), by + h * 0.3)],
               fill=INK, width=2)
        sx, sy = x + w * (bx - 0.06), y + h * 0.06
        ex, ey = x + w * (bx + 0.1), by - 2
        for t in range(9):
            tt = t / 8.0
            px = sx + (ex - sx) * tt
            py = sy + (ey - sy) * tt * tt
            if t:
                d.line([(ox, oy), (px, py)], fill=RED, width=2)
            ox, oy = px, py


def scene2(d, x, y, w, h):  # Akvan: spiral storm, coast, red landfall dot
    cx, cy = x + w * 0.38, y + h * 0.52
    for r in (0.42, 0.3, 0.18):
        d.arc([cx - w * r, cy - h * r * 1.6, cx + w * r, cy + h * r * 1.6],
              start=20, end=320, fill=MGRAY, width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=INK)
    coast = [(x + w * 0.78 + 6 * ((i % 2) * 2 - 1), y + i * h / 6.0)
             for i in range(7)]
    d.line(coast, fill=INK, width=2)
    d.polygon(coast + [(x + w, y + h), (x + w, y)], fill=(214, 214, 214))
    d.line(coast, fill=INK, width=2)
    lx, ly = x + w * 0.79, y + h * 0.52
    d.ellipse([lx - 6, ly - 6, lx + 6, ly + 6], outline=RED, width=3)


def scene3(d, x, y, w, h):  # Markets: gridlines, red falling line
    for i in range(3):
        gy = y + h * (0.25 + 0.25 * i)
        d.line([(x + 4, gy), (x + w - 4, gy)], fill=GRAY2, width=1)
    pts = [(x + w * (0.05 + 0.15 * i),
            y + h * (0.18 + 0.13 * i + (0.05 if i % 2 else 0)))
           for i in range(7)]
    d.line(pts, fill=RED, width=3)
    for px, py in pts:
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 9, ey - 3), (ex - 4, ey + 7)], fill=RED)


def scene4(d, x, y, w, h):  # UK-EU: two flags, red link between
    fx, fy, fw, fh = x + w * 0.08, y + h * 0.2, w * 0.3, h * 0.55
    d.rectangle([fx, fy, fx + fw, fy + fh], outline=INK, width=2)
    d.line([(fx, fy), (fx + fw, fy + fh)], fill=MGRAY, width=2)
    d.line([(fx + fw, fy), (fx, fy + fh)], fill=MGRAY, width=2)
    d.rectangle([fx + fw * 0.4, fy, fx + fw * 0.6, fy + fh], fill=MGRAY)
    d.rectangle([fx, fy + fh * 0.38, fx + fw, fy + fh * 0.62], fill=MGRAY)
    ex, ey, ew, eh = x + w * 0.62, y + h * 0.2, w * 0.3, h * 0.55
    d.rectangle([ex, ey, ex + ew, ey + eh], outline=INK, width=2)
    import math
    for i in range(12):
        a = 2 * math.pi * i / 12
        px = ex + ew / 2 + ew * 0.32 * math.cos(a)
        py = ey + eh / 2 + eh * 0.32 * math.sin(a)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=INK)
    my = y + h * 0.47
    d.line([(fx + fw + 3, my), (ex - 3, my)], fill=RED, width=3)
    d.polygon([(ex - 3, my), (ex - 11, my - 4), (ex - 11, my + 4)], fill=RED)


def scene5(d, x, y, w, h):  # COP31: globe, thermometer with red column
    cx, cy, r = x + w * 0.34, y + h * 0.52, h * 0.4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=2)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=MGRAY,
              width=1)
    d.line([(cx - r, cy - r * 0.45), (cx + r, cy - r * 0.45)], fill=MGRAY)
    d.line([(cx - r, cy + r * 0.45), (cx + r, cy + r * 0.45)], fill=MGRAY)
    tx = x + w * 0.78
    d.rectangle([tx - 3, y + h * 0.14, tx + 3, y + h * 0.72], outline=INK,
                width=2)
    d.rectangle([tx - 2, y + h * 0.34, tx + 2, y + h * 0.72], fill=RED)
    d.ellipse([tx - 8, y + h * 0.66, tx + 8, y + h * 0.66 + 16], outline=INK,
              width=2)
    d.ellipse([tx - 5, y + h * 0.66 + 3, tx + 5, y + h * 0.66 + 13], fill=RED)


def scene6(d, x, y, w, h):  # Poland: field furrows, missile, red burst
    for i in range(4):
        gy = y + h * (0.55 + 0.12 * i)
        d.line([(x + 3, gy), (x + w - 3, gy)], fill=MGRAY, width=1)
    mx, my = x + w * 0.58, y + h * 0.34
    d.polygon([(mx - 26, my - 8), (mx + 14, my + 6), (mx + 26, my + 16),
               (mx + 10, my + 20), (mx - 20, my + 4)], fill=MGRAY)
    d.polygon([(mx + 14, my + 6), (mx + 30, my + 10), (mx + 18, my + 20)],
              fill=INK)
    bx, by = mx + 30, my + 14
    for dx, dy in ((0, -9), (7, -6), (9, 2), (5, 8), (-4, 7), (-8, -2)):
        d.line([(bx, by), (bx + dx, by + dy)], fill=RED, width=2)


def scene7(d, x, y, w, h):  # Iraq: desert, two vehicles, sun
    d.ellipse([x + w * 0.06, y + h * 0.08, x + w * 0.06 + 14,
               y + h * 0.08 + 14], outline=MGRAY, width=2)
    d.rectangle([x, y + h * 0.78, x + w, y + h], fill=GRAY2)
    for vx in (0.3, 0.62):
        bx, by = x + w * vx, y + h * 0.52
        d.rectangle([bx, by, bx + w * 0.2, by + h * 0.2], fill=MGRAY)
        d.rectangle([bx + w * 0.12, by - h * 0.12, bx + w * 0.19,
                     by], fill=MGRAY)
        for wx in (0.04, 0.15):
            cx = bx + w * wx
            d.ellipse([cx - 5, by + h * 0.18, cx + 5, by + h * 0.18 + 10],
                      fill=INK)
    d.line([(x + w * 0.05, y + h * 0.9), (x + w * 0.4, y + h * 0.9)],
           fill=MGRAY, width=1)

def scene8(d, x, y, w, h):  # Italy: banner over a crowd
    bx, by, bw, bh = x + w * 0.22, y + h * 0.08, w * 0.56, h * 0.3
    d.line([(bx + 3, by - 2), (bx + 3, by + bh + h * 0.3)], fill=INK, width=2)
    d.line([(bx + bw - 3, by - 2), (bx + bw - 3, by + bh + h * 0.3)],
           fill=INK, width=2)
    d.rectangle([bx, by, bx + bw, by + bh], fill=WHITE, outline=INK, width=2)
    for i in range(9):
        hx = x + w * (0.08 + 0.1 * i)
        hy = y + h * 0.72
        d.ellipse([hx - 5, hy - 10, hx + 5, hy], fill=MGRAY)
        d.rectangle([hx - 7, hy, hx + 7, hy + h * 0.24], fill=MGRAY)


def scene9(d, x, y, w, h):  # Japan: rising bars, red trend line
    base = y + h * 0.88
    tops = []
    for i, fr in enumerate((0.3, 0.45, 0.58, 0.78)):
        bx = x + w * (0.12 + 0.2 * i)
        bw = w * 0.13
        top = base - h * fr
        d.rectangle([bx, top, bx + bw, base], fill=MGRAY if i < 3 else INK)
        tops.append((bx + bw / 2, top - 3))
    d.line(tops, fill=RED, width=3)
    ex, ey = tops[-1]
    d.polygon([(ex, ey), (ex - 9, ey + 1), (ex - 3, ey + 8)], fill=RED)
    d.line([(x + 3, base), (x + w - 3, base)], fill=INK, width=1)


def scene10(d, x, y, w, h):  # Seoul: courthouse
    cx = x + w / 2
    top = y + h * 0.1
    d.polygon([(cx - w * 0.34, top + h * 0.22), (cx + w * 0.34, top + h * 0.22),
               (cx, top)], fill=INK)
    for i in range(4):
        cxx = x + w * (0.24 + 0.17 * i)
        d.rectangle([cxx - 3, top + h * 0.3, cxx + 3, top + h * 0.78],
                    fill=MGRAY)
    d.rectangle([x + w * 0.14, top + h * 0.82, x + w * 0.86, top + h * 0.9],
                fill=INK)


def scene11(d, x, y, w, h):  # Kenya: oil derrick, red droplet
    ax, ay = x + w * 0.34, y + h * 0.06
    bx, by = x + w * 0.14, y + h * 0.92
    d.line([(bx, by), (ax, ay)], fill=INK, width=3)
    d.line([(x + w * 0.54, by), (ax, ay)], fill=INK, width=3)
    for t in (0.3, 0.55, 0.8):
        yy = ay + (by - ay) * t
        half = w * 0.2 * t
        d.line([(ax - half, yy), (ax + half, yy)], fill=MGRAY, width=2)
    d.line([(x + 3, by), (x + w - 3, by)], fill=INK, width=1)
    dx, dy = ax, y + h * 0.52
    d.polygon([(dx, dy - 10), (dx - 6, dy + 4), (dx + 6, dy + 4)], fill=RED)
    d.ellipse([dx - 6, dy, dx + 6, dy + 11], fill=RED)


def scene12(d, x, y, w, h):  # San Salvador: ballot box and paper
    bx, by, bw, bh = x + w * 0.3, y + h * 0.38, w * 0.42, h * 0.52
    d.rectangle([bx, by, bx + bw, by + bh], outline=INK, width=3)
    d.line([(bx + bw * 0.25, by + 5), (bx + bw * 0.75, by + 5)], fill=INK,
           width=3)
    d.polygon([(bx + bw * 0.38, by - h * 0.26), (bx + bw * 0.66, by - h * 0.2),
               (bx + bw * 0.6, by + 4), (bx + bw * 0.34, by - 2)], fill=WHITE,
              outline=INK)
    d.ellipse([bx + bw * 0.42, by + bh * 0.42, bx + bw * 0.58,
               by + bh * 0.42 + (bx + bw * 0.58) - (bx + bw * 0.42)],
              outline=RED, width=2)


def scene13(d, x, y, w, h):  # Wellington: stumps, bat, red ball
    sx = x + w * 0.6
    for i in range(3):
        d.line([(sx + i * 9, y + h * 0.2), (sx + i * 9, y + h * 0.85)],
               fill=INK, width=3)
    d.line([(sx - 2, y + h * 0.17), (sx + 8, y + h * 0.17)], fill=INK, width=2)
    d.line([(sx + 10, y + h * 0.17), (sx + 20, y + h * 0.17)], fill=INK,
           width=2)
    d.polygon([(x + w * 0.2, y + h * 0.85), (x + w * 0.3, y + h * 0.85),
               (x + w * 0.42, y + h * 0.2), (x + w * 0.34, y + h * 0.14)],
              fill=MGRAY)
    bx, by = x + w * 0.47, y + h * 0.38
    d.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=RED)


def scene_city(d, x, y, w, h):  # Kryvyi Rih: skyline, red burst, arcs
    base = y + h
    heights = (0.52, 0.78, 0.4, 0.66, 0.88, 0.48, 0.72, 0.56)
    bw = w / len(heights)
    for i, fr in enumerate(heights):
        bx = x + i * bw
        top = base - h * fr
        d.rectangle([bx + 1, top, bx + bw - 1, base], fill=MGRAY)
        for wy in range(int(top) + 4, int(base) - 3, 7):
            d.point((bx + bw * 0.35, wy), fill=WHITE)
            d.point((bx + bw * 0.65, wy), fill=WHITE)
    bx, by = x + w * 0.8, y + h * 0.2
    for dx, dy in ((0, -11), (8, -8), (11, 0), (8, 8), (0, 11), (-8, 8),
                   (-11, 0), (-8, -8)):
        d.line([(bx, by), (bx + dx, by + dy)], fill=RED, width=2)
    d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=RED)
    for sx in (0.08, 0.3):
        ex, ey = x + w * (sx + 0.34), y + h * 0.42
        ox, oy = x + w * sx, y + h * 0.04
        px, py = ox, oy
        for t in range(1, 9):
            tt = t / 8.0
            nx = ox + (ex - ox) * tt
            ny = oy + (ey - oy) * tt * tt
            d.line([(px, py), (nx, ny)], fill=RED, width=2)
            px, py = nx, ny


def scene_reticle(d, x, y, w, h):  # Copenhagen: rooftops under a reticle
    base = y + h
    for i, rx in enumerate((0.04, 0.3, 0.56, 0.8)):
        rw = w * 0.22
        rh = h * (0.34 if i % 2 else 0.26)
        d.rectangle([x + w * rx, base - rh + h * 0.18, x + w * rx + rw,
                     base], fill=GRAY2)
        d.polygon([(x + w * rx - 2, base - rh + h * 0.18),
                   (x + w * rx + rw + 2, base - rh + h * 0.18),
                   (x + w * rx + rw / 2, base - rh - h * 0.1)], fill=MGRAY)
    cx, cy, r = x + w * 0.5, y + h * 0.42, h * 0.34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED, width=2)
    d.line([(cx - r - 5, cy), (cx - r * 0.35, cy)], fill=RED, width=2)
    d.line([(cx + r * 0.35, cy), (cx + r + 5, cy)], fill=RED, width=2)
    d.line([(cx, cy - r - 5), (cx, cy - r * 0.35)], fill=RED, width=2)
    d.line([(cx, cy + r * 0.35), (cx, cy + r + 5)], fill=RED, width=2)
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=RED)


def scene_cyber(d, x, y, w, h):  # Cyberattack: payment cards, warning
    for i, ox in enumerate((0.04, 0.22, 0.4)):
        cx, cy = x + w * ox, y + h * (0.16 + 0.1 * i)
        cw, ch = w * 0.3, h * 0.58
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=WHITE, outline=INK,
                    width=2)
        d.rectangle([cx, cy + ch * 0.18, cx + cw, cy + ch * 0.36],
                    fill=MGRAY)
        d.rectangle([cx + cw * 0.1, cy + ch * 0.52, cx + cw * 0.3,
                     cy + ch * 0.76], outline=INK, width=1)
        d.line([(cx + cw * 0.45, cy + ch * 0.64), (cx + cw * 0.9,
                 cy + ch * 0.64)], fill=GRAY2, width=2)
    tx, ty = x + w * 0.84, y + h * 0.5
    d.polygon([(tx, ty - h * 0.34), (tx - w * 0.09, ty + h * 0.3),
               (tx + w * 0.09, ty + h * 0.3)], outline=RED, width=3)
    T(d, tx - tw(d, "!", AB(15)) / 2, ty - h * 0.05, "!", AB(15), fill=RED)


def scene_mongolia(d, x, y, w, h):  # Mongolia: steppe, ger, flag
    d.ellipse([x + w * 0.82, y + h * 0.06, x + w * 0.82 + 13,
               y + h * 0.06 + 13], outline=MGRAY, width=2)
    d.rectangle([x, y + h * 0.78, x + w, y + h], fill=GRAY2)
    d.line([(x + 2, y + h * 0.7), (x + w * 0.4, y + h * 0.6),
            (x + w * 0.75, y + h * 0.68), (x + w - 2, y + h * 0.62)],
           fill=MGRAY, width=1)
    gx, gy = x + w * 0.3, y + h * 0.78
    gw, gh = w * 0.3, h * 0.42
    d.rectangle([gx, gy - gh, gx + gw, gy], fill=WHITE, outline=INK, width=2)
    d.polygon([(gx - 3, gy - gh), (gx + gw + 3, gy - gh),
               (gx + gw / 2, gy - gh - h * 0.22)], fill=WHITE, outline=INK)
    d.rectangle([gx + gw * 0.4, gy - gh * 0.55, gx + gw * 0.6, gy],
                outline=INK, width=2)
    d.line([(gx + gw / 2, gy - gh - h * 0.22), (gx + gw / 2, gy - gh - 3)],
           fill=INK, width=1)
    px = x + w * 0.72
    d.line([(px, y + h * 0.78), (px, y + h * 0.16)], fill=INK, width=2)
    d.rectangle([px, y + h * 0.16, px + w * 0.13, y + h * 0.38], fill=WHITE,
                outline=INK, width=1)
    d.rectangle([px + w * 0.02, y + h * 0.2, px + w * 0.05, y + h * 0.34],
                fill=RED)


SCENES = {1: scene6, 2: scene5, 3: scene3, 4: scene_city,
          5: scene_reticle, 6: scene1, 7: scene2, 8: scene4,
          9: scene_cyber, 10: scene_mongolia, 11: scene10, 12: scene12,
          13: scene13}


def draw_strip(d, x, y, w, h, card, lead):
    no, place, region, topic = card[0], card[1], card[2], card[3]
    tag, label, caption = card[6], card[7], card[8]
    d.rectangle([x, y, x + w, y + h], fill=LGRAY)
    d.rectangle([x, y, x + w, y + 3], fill=REG[region])
    SCENES[no](d, x, y + 3, w, h - 19)
    # source tag: white pill, top-right, its own clear zone
    ftag = AB(9)
    pw = tw(d, tag, ftag) + 10
    px, py = x + w - pw - 4, y + 6
    d.rectangle([px, py, px + pw, py + 14], fill=WHITE, outline=INK, width=1)
    T(d, px + 5, py + 2, tag, ftag)
    # data label: red bold, bottom-left above the caption band, white backing
    flab = AB(13 if lead else 10)
    lines = label.split("\n")
    lh = 16 if lead else 12
    lab_h = lh * len(lines)
    lab_w = max(tw(d, ln, flab) for ln in lines)
    ly = y + h - 16 - lab_h - 3
    d.rectangle([x + 3, ly - 1, x + 3 + lab_w + 6, ly + lab_h + 1], fill=WHITE)
    for i, ln in enumerate(lines):
        T(d, x + 6, ly + i * lh, ln, flab, fill=RED)
    # caption band at the strip's bottom edge
    d.rectangle([x, y + h - 16, x + w, y + h], fill=INK)
    fcap = fit_font(d, caption, AB, 9, w - 8, 7)
    T(d, x + (w - tw(d, caption, fcap)) / 2, y + h - 12, caption, fcap,
      fill=WHITE)


def draw_card(d, x, y, w, strip_h, card, lead):
    no, place, region, topic = card[0], card[1], card[2], card[3]
    headline, deck = card[4], card[5]
    draw_strip(d, x, y, w, strip_h, card, lead)
    rline = "%d %s - %s - %s" % (no, place, region, topic)
    if lead:
        fr = fit_font(d, rline, AB, 10, w)
        T(d, x, y + strip_h + 4, rline, fr, fill=REG[region])
        fh, lh_h = AB(21), 22
        hy = y + strip_h + 19
        fd, lh_d = AM(12), 14
    else:
        fr = fit_font(d, rline, AB, 9, w, 7)
        T(d, x, y + strip_h + 3, rline, fr, fill=REG[region])
        fh, lh_h = AB(15), 16
        hy = y + strip_h + 15
        fd, lh_d = AM(11), 12
    for i, ln in enumerate(wrap(d, headline, fh, w)):
        T(d, x, hy + i * lh_h, ln, fh)
    dy = hy + 2 * lh_h + 3
    for i, ln in enumerate(wrap(d, deck, fd, w)):
        T(d, x, dy + i * lh_d, ln, fd, fill=(34, 34, 34))

# ------------------------------------------------------------- header -----
def draw_header(d):
    # kicker bar
    T(d, M, 8, "THE GLOBAL WIRE", AB(15))
    bx = M + tw(d, "THE GLOBAL WIRE", AB(15)) + 12
    T(d, bx, 11, "THE WORLD IN ONE DAY", AM(11), fill=MGRAY)
    kr = "40 STORIES - 7 REGIONS - EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
    T(d, W - M - tw(d, kr, AB(10)), 11, kr, AB(10))
    rule(d, M, W - M, 27, wdt=2)
    rule(d, M, W - M, 30, wdt=1)
    # masthead (ink of PF(58) drawn at y=33 ends at y=107; deckline at 108)
    T(d, M, 33, "Saturday 21 November 2026", PF(58))
    T(d, M, 108,
      "Missiles land in Poland - COP31 slips into overtime - Wall Street "
      "falls into correction - Denmark exposes a plot", AM(12), fill=MGRAY)
    rule(d, M, W - M, 126)
    # UTC timeline: five divided slots
    sw = CW / 5.0
    for i, (lab, ev) in enumerate(TIMELINE):
        sx = M + i * sw
        if i:
            vrule(d, sx, 132, 166, fill=GRAY2)
        T(d, sx + 6, 131, lab, AB(11), fill=RED)
        for j, ln in enumerate(wrap(d, ev, AM(10), sw - 12)):
            T(d, sx + 6, 145 + j * 11, ln, AM(10))
    rule(d, M, W - M, 172)
    # THE DAY IN NUMBERS: a ruled table, figures in red
    rule(d, M, W - M, 176)
    lab = "THE DAY IN NUMBERS"
    lw = tw(d, lab, AB(11))
    d.rectangle([W / 2 - lw / 2 - 8, 170, W / 2 + lw / 2 + 8, 182],
                fill=WHITE)
    T(d, W / 2 - lw / 2, 171, lab, AB(11))
    cw6 = CW / 6.0
    for i, (fig, cap) in enumerate(NUMBERS):
        cx = M + i * cw6
        if i:
            vrule(d, cx, 180, 234, fill=GRAY2)
        ff = fit_font(d, fig, AB, 25, cw6 - 12)
        T(d, cx + (cw6 - tw(d, fig, ff)) / 2, 183, fig, ff, fill=RED)
        for j, ln in enumerate(wrap(d, cap, AM(10), cw6 - 12)):
            T(d, cx + (cw6 - tw(d, ln, AM(10))) / 2, 213 + j * 11, ln,
              AM(10), fill=MGRAY)
    rule(d, M, W - M, 237)
    # region count strip: white chips, black border, color bullet
    T(d, M, 246, "40 STORIES BY REGION", AB(11))
    cx = M + tw(d, "40 STORIES BY REGION", AB(11)) + 14
    for name, cnt in REGION_COUNTS:
        s = "%s %d" % (name, cnt)
        chw = tw(d, s, AB(11)) + 26
        d.rectangle([cx, 242, cx + chw, 262], fill=WHITE, outline=INK,
                    width=1)
        d.rectangle([cx + 6, 248, cx + 14, 256], fill=REG[name])
        T(d, cx + 19, 246, s, AB(11))
        cx += chw + 7

# -------------------------------------------------------------- cards -----
def draw_cards(d):
    # lead row: cards 1-3, 325 wide
    for i, card in enumerate(CARDS[:3]):
        draw_card(d, M + i * 333, 266, 325, 92, card, True)
    # feature grid: cards 4-13, 2 rows x 5 cols, 196 wide
    for k, card in enumerate(CARDS[3:]):
        r, c = divmod(k, 5)
        draw_card(d, M + c * 199, 472 + r * 134, 196, 44, card, False)


# ---------------------------------------------------------------- map -----
def draw_map(d):
    T(d, M, 752, "WHERE IT HAPPENED", AB(12))
    x0, y0, x1, y1 = M, 768, M + 330, 892
    d.rectangle([x0, y0, x1, y1], fill=WHITE, outline=INK, width=1)
    ix0, iy0, iw, ih = x0 + 1, y0 + 1, 328, 122

    def proj(lon, lat):
        return (ix0 + (lon + 180) / 360.0 * iw,
                iy0 + (82 - lat) / 140.0 * ih)

    for s in WORLD.values():
        for ring in s.split("|"):
            pts = []
            for pair in ring.split(","):
                lo, la = pair.split(":")
                pts.append(proj(float(lo), float(la)))
            if len(pts) >= 3:
                d.polygon(pts, fill=LAND, outline=INK)
    for no, txt, region, lon, lat in BRIEFS:
        if lon is None:
            continue
        px, py = proj(lon, lat)
        d.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5], fill=REG[region])
    for card in CARDS:
        px, py = proj(card[9], card[10])
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=REG[card[2]],
                  outline=RED, width=2)
    for card in CARDS:
        px, py = proj(card[9], card[10])
        s = str(card[0])
        T(d, px - tw(d, s, AB(9)) / 2, py - 5, s, AB(9), fill=WHITE)
    T(d, M, 897,
      "Numbered pins = the 13 pictured stories - small dots = the briefs",
      AM(9), fill=MGRAY)

# ------------------------------------------------------------- bottom -----
def draw_bottom_right(d):
    x0 = 358
    T(d, x0, 752, "ALSO ON SATURDAY 21 NOVEMBER - 27 MORE STORIES", AB(12))
    colw = 319
    cols = [BRIEFS[:15], BRIEFS[15:]]
    wrapped = []
    for col in cols:
        lines = []
        for no, txt, region, lon, lat in col:
            lines.extend(wrap(d, "%d %s" % (no, txt), AM(10), colw))
        wrapped.append(lines)
    lh = min(11.5, 234.0 / max(len(lines) for lines in wrapped))
    for ci, lines in enumerate(wrapped):
        cx = x0 + ci * (colw + 12)
        for j, ln in enumerate(lines):
            T(d, cx, 774 + j * lh, ln, AM(10))


def draw_datecheck(d):
    d.rectangle([M, 910, M + 330, 1008], outline=RED, width=2)
    T(d, M + 8, 916, "DATE CHECK", AB(11), fill=RED)
    for j, ln in enumerate(wrap(d, DATECHECK, AM(10), 314)):
        T(d, M + 8, 932 + j * 11, ln, AM(10))


def draw_footer(d):
    rule(d, M, W - M, 1012, fill=GRAY2)
    T(d, M, 1014, FOOTER_L, AM(10), fill=MGRAY)
    T(d, W - M - tw(d, FOOTER_R, AM(10)), 1014, FOOTER_R, AM(10), fill=MGRAY)


def compose():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    draw_header(d)
    draw_cards(d)
    draw_map(d)
    draw_bottom_right(d)
    draw_datecheck(d)
    draw_footer(d)
    out = os.path.join(BASE, "entry.png")
    img.save(out)
    print("saved", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    compose()
