# draw.py - Challenger R5 "THE GLOBAL WIRE" - News Image, Saturday 21 Nov 2026.
# Round-5 rebuild for @maseiah990, structured on the pixel-measured dissection
# of NI21's #1 (giggs18, 990,658): date-only masthead, claims bar, day-parts
# bar, three EQUAL leads, 10 minis, uniform card anatomy (64/60px saturated
# scenes, black slug box, CONFIRMED chip, black location bar, red circle
# badge), dot-matrix map + one-line briefs, DATE CHECK with dated discards
# and an Unverified clause. No numbers strip, no tally bar.
# Account delta: SATURATION - r4 was the fleet's palest page; every scene
# here is a flat BRIGHT saturated fill with one big subject (>=50% of scene
# height, max 3 large elements). Facts ONLY from POOL21 (21 Nov 2026).
# Deterministic Pillow program (stdlib + PIL only, no network).
import math
import os
from PIL import Image, ImageDraw, ImageFont
from mapdata import LANDMASSES

BASE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(BASE, "fonts")


def PF(s):
    return ImageFont.truetype(os.path.join(FD, "PlayfairDisplay-900.ttf"), s)


def AB(s):
    return ImageFont.truetype(os.path.join(FD, "Archivo-Bold.ttf"), s)


def AM(s):
    return ImageFont.truetype(os.path.join(FD, "Archivo-Medium.ttf"), s)


# ---------------------------------------------------------------- palette ---
PAPER = (245, 241, 224)
INK = (18, 18, 18)
WHITE = (255, 255, 255)
RED = (192, 40, 25)
BLACK = (10, 10, 10)
NAVY = (14, 31, 52)
SAND = (247, 206, 149)
SKY = (58, 144, 224)
TEAL = (16, 158, 178)
GOLD = (244, 178, 32)
GREEN = (46, 168, 84)
ORANGE = (238, 116, 32)
PURPLE = (122, 62, 168)
PINK = (226, 84, 128)

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
M = 14
CW = W - 2 * M  # 996


def tw(d, s, f):
    return d.textlength(s, font=f)


def wrap(d, s, f, maxw):
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


def trunc(d, s, f, maxw):
    if tw(d, s, f) <= maxw:
        return s
    while s and tw(d, s + "…", f) > maxw:
        s = s[:-1]
    return s.rstrip() + "…"


def T(d, x, y, s, f, fill=INK, anchor="la"):
    d.text((x, y), s, font=f, fill=fill, anchor=anchor)


def fit_font(d, s, make, size, maxw, minsize=9):
    f = make(size)
    while tw(d, s, f) > maxw and size > minsize:
        size -= 1
        f = make(size)
    return f


# ------------------------------------------------------------------- data ---
# no, place, region, category, headline, deck, outlet, status, slug, lon, lat
CARDS = [
    (1, "WARSAW, POLAND", "EUROPE", "CONFLICT",
     "Rutte flies to Warsaw after missiles land",
     "Two missiles and a suspected jet drone came down in the south-east, "
     "a Kh-101 near Nowy Lipowiec. Rutte calls it a “grave violation”; "
     "Tusk a deliberate provocation.",
     "AP", "REPORTED", "3 WEAPONS CROSS", 21.0, 52.2),
    (2, "ANTALYA", "GLOBAL", "CLIMATE",
     "COP31 runs into overtime with no deal yet",
     "Talks ran past Friday's scheduled close into Saturday. The draft "
     "drops every fossil-fuel reference and the $120bn finance target; "
     "a third draft is due this morning.",
     "AP", "CONFIRMED", "NO DEAL YET", 30.7, 36.9),
    (3, "NEW YORK", "AMERICAS", "MARKETS",
     "Wall Street enters correction as AI rout deepens",
     "The S&P 500 fell about 3.7% on Friday, pushing it into correction "
     "territory. The Nasdaq dropped 5.28% as chip and AI shares plunged.",
     "SIMPLELIFE", "CONFIRMED", "NASDAQ -5.28%", -74.0, 40.7),
    (4, "KRYVYI RIH", "EUROPE", "WAR",
     "Russian strike kills two, injures 42",
     "One of Russia's largest attacks of the war, the city's military "
     "chief says.",
     "APPISTOS", "CONFIRMED", "2 DEAD · 42 HURT", 33.4, 47.9),
    (5, "COPENHAGEN", "EUROPE", "SECURITY",
     "Denmark exposes 'assassination plot'",
     "Russia planned a bid to kill a Ukrainian-American rapper, "
     "Denmark says.",
     "BBC", "CONFIRMED", "ATTACHE EXPELLED", 12.6, 55.7),
    (6, "KYIV", "EUROPE", "WAR",
     "Russia's barrage: 400 drones, 110 missiles",
     "At least eight dead across Ukraine; the Austrian embassy is "
     "hit in Kyiv.",
     "BBC", "CONFIRMED", "400 DRONES", 30.5, 50.4),
    (7, "ODISHA, INDIA", "ASIA", "STORM",
     "After Akvan: 372,000 moved, no deaths",
     "No deaths a day after landfall; relief under way, schools shut "
     "through Saturday.",
     "RIDHU TIMES", "CONFIRMED", "372,000 MOVED", 84.9, 19.3),
    (8, "BRUSSELS", "EUROPE", "AID",
     "EU adopts €1bn military aid for Ukraine",
     "Joint buying via the Peace Facility. Britain adds 1,000+ drones "
     "in a £260m package.",
     "REUTERS", "CONFIRMED", "€1BN ADOPTED", 4.3, 50.8),
    (9, "NEW YORK", "AMERICAS", "CYBER",
     "JPMorgan, Visa, Mastercard hit by cyberattack",
     "Incidents hit third-party vendors; core payment networks are "
     "unaffected, they say.",
     "REUTERS", "CONFIRMED", "3 NETWORKS HIT", -73.9, 40.8),
    (10, "ULAANBAATAR", "ASIA", "POLITICS",
     "Mongolia's president resigns",
     "Sets up a snap election after a week of political turmoil in "
     "the capital.",
     "REUTERS", "CONFIRMED", "SNAP ELECTION", 106.9, 47.9),
    (11, "THE HAGUE", "GLOBAL", "COURTS",
     "Myanmar ruling rattles Israel's Gaza defence",
     "Genocide verdict on Myanmar raises questions over Israel's own "
     "case, experts say.",
     "BBC", "CONFIRMED", "GENOCIDE VERDICT", 4.3, 52.1),
    (12, "JOHANNESBURG", "AFRICA", "ELECTION",
     "ANC scrambles after worst result since 1994",
     "The ANC wins 31%, its worst since 1994, and now races for "
     "coalition deals.",
     "BBC", "CONFIRMED", "ANC 31%", 28.0, -26.2),
    (13, "WELLINGTON", "OCEANIA", "SPORT",
     "India fight back: 159/1 at stumps, day two",
     "India trail New Zealand by 209 after the hosts made 368; "
     "Nicholls 175 not out.",
     "ICC", "CONFIRMED", "159/1 · DAY TWO", 174.8, -41.3),
]

DAYPARTS = [
    ("OVERNIGHT", "Kryvyi Rih strike: two killed, 42 injured"),
    ("MORNING", "Rutte flies to Warsaw over the missiles"),
    ("MIDDAY", "Antalya: third COP31 draft due after overnight talks"),
    ("AFTERNOON", "Denmark expels the Russian attache"),
    ("EVENING", "Stumps in Wellington: India 159/1"),
]

# no, bold lead-in, tail  (POOL21 briefs 14-40, tails cut to one hard line)
BRIEFS = [
    (14, "Kathmandu:", "Nepal's leader Balendra Shah faces an India test"),
    (15, "Washington:", "US releases more UFO footage from Middle East"),
    (16, "Los Angeles:", "Hyundai unveils the 2027 Elantra at the auto show"),
    (17, "Cardiff:", "Price beats Kotaskova to become undisputed champion"),
    (18, "Paris:", "Three police sentenced over the beating of Michel Zecler"),
    (19, "Oxford:", "Life, 22 years minimum, for the Thames drowning murder"),
    (20, "New York:", "Nikhil Gupta gets 19+ years over the Sikh murder plot"),
    (21, "Cincinnati:", "Fiona the hippo dies after eating a hat"),
    (22, "Washington:", "US sanctions four Iranians over oil revenues"),
    (23, "Hormuz:", "A tanker is struck and on fire in the strait"),
    (24, "Los Angeles:", "Jury convicts the Palisades Fire starter"),
    (25, "Frankfurt:", "ECB names Boone and Brunnermeier to its board"),
    (26, "Buenos Aires:", "Senate backs a disability framework, 71-0"),
    (27, "Riyadh:", "Saudi coalition intercepts Houthi missiles over Riyadh"),
    (28, "Barcelona:", "A pill is hailed as a breakthrough for pancreatic cancer"),
    (29, "Gaza:", "Children appeal for help on World Children's Day"),
    (30, "Madrid:", "Amnesty: police used excess force in the strike"),
    (31, "Rome:", "Workers and students march against Meloni"),
    (32, "Jeddah:", "Saudi Arabia warns of thunderstorms through Tuesday"),
    (33, "Kuala Lumpur:", "10,000 Rohingya bound for Turkey training"),
    (34, "Kharkiv:", "Ukraine says it has finished a “Bear Trap” in the area"),
    (35, "Islamabad:", "Minerals worth $8-10 trillion, minister says"),
    (36, "Singapore:", "US presses Singapore and Malaysia over Iran"),
    (37, "Paris:", "France seeks a UN council meeting on the Kyiv strikes"),
    (38, "Kyiv:", "The war tally: 771 Ukrainians killed, 2,300+ missing"),
    (39, "Ankara:", "Turkey welcomes the World Court's Myanmar ruling"),
    (40, "Turin:", "ATP semis set: Alcaraz v Shelton, Zverev v Medvedev"),
]

DATECHECK = (
    "Left out on purpose — not Saturday's news: Kyiv's three bridges hit "
    "(Fri 20 Nov) · Cyclone Akvan's landfall at Gopalpur (Fri 20 Nov) · "
    "COP31's final day ending with no deal (Fri 20 Nov) · Asia's AI "
    "sell-off, Taipei -6.2% (Fri 20 Nov) · the UK-EU reset deal "
    "(Fri 20 Nov). Unverified: the suspected jet drone in south-east "
    "Poland — its origin is unconfirmed, so it is shown as reported, "
    "not as fact. Not yet happened: any final COP31 text · the ATP "
    "semi-final results · BepiColombo's entry into orbit around "
    "Mercury (due today)."
)

FOOTER = (
    "Every story here happened, or was first reported, on Saturday 21 "
    "November 2026 · Sources: AP, BBC, Reuters, AFP, ICC, OFAC, UKMTO, "
    "UN, SPA, ATP, Anadolu, Ukrinform, SimpleLife, AppiStos, Ridhu "
    "Times, Fast Company · Original drawings"
)


# ----------------------------------------------------------------- scenes ---
# Every scene: one flat BRIGHT saturated fill + ONE big subject (>=50% of
# scene height), max 3 large elements. Slug box + chip are drawn by the
# card routine on top of the scene.
def scene(d, x, y, w, h, no):
    cx = x + w // 2
    if no == 1:  # Warsaw: two big missiles over warm sand sky
        d.rectangle([x, y, x + w, y + h], fill=SAND)
        d.rectangle([x, y + h - 9, x + w, y + h], fill=GREEN)
        for cxx, cyy in ((x + w * 0.40, y + 24), (x + w * 0.66, y + 30)):
            d.ellipse([cxx - 26, cyy - 8, cxx + 26, cyy + 8], fill=(252, 250, 244))
            d.ellipse([cxx - 12, cyy - 13, cxx + 14, cyy + 4], fill=(252, 250, 244))
        for ox, oy, ln in ((-w // 4, 6, 46), (w // 6, 2, 54)):
            x0, y0 = cx + ox, y + oy
            x1, y1 = x0 + ln * 0.72, y0 + ln * 0.70
            d.line([(x0, y0), (x1, y1)], fill=(238, 238, 232), width=12)
            d.line([(x0, y0), (x1, y1)], fill=INK, width=2)
            d.polygon([(x1, y1), (x1 - 13, y1 - 3), (x1 - 3, y1 - 13)], fill=RED)
            d.polygon([(x0, y0), (x0 + 11, y0 - 6), (x0 + 6, y0 + 9)], fill=ORANGE)
    elif no == 2:  # Antalya: huge sun over a conference hall
        d.rectangle([x, y, x + w, y + h], fill=SKY)
        d.ellipse([x + 26, y + 20, x + 86, y + 34], fill=(252, 250, 244))
        d.ellipse([x + 44, y + 14, x + 76, y + 28], fill=(252, 250, 244))
        d.ellipse([x + w - 62, y + 4, x + w - 10, y + 56], fill=GOLD)
        d.rectangle([x + 14, y + h - 26, x + w - 14, y + h], fill=NAVY)
        d.rectangle([x + 14, y + h - 33, x + w - 14, y + h - 26], fill=WHITE)
        for wx in range(x + 24, x + w - 28, 16):
            d.rectangle([wx, y + h - 20, wx + 8, y + h - 8], fill=GOLD)
    elif no == 3:  # New York: giant falling chart
        d.rectangle([x, y, x + w, y + h], fill=(186, 224, 250))
        pts = [(x + 8, y + 8), (x + w * 0.32, y + 16), (x + w * 0.52, y + 12),
               (x + w * 0.72, y + 30), (x + w - 14, y + h - 12)]
        d.polygon(pts + [(x + w - 14, y + h), (x + 8, y + h)],
                  fill=(245, 160, 140))
        d.line(pts, fill=RED, width=6)
        ex, ey = pts[-1]
        d.polygon([(ex, ey), (ex - 20, ey - 4), (ex - 6, ey - 20)], fill=RED)
        for bx, bw_, bh in ((6, 16, 20), (30, 12, 14), (w - 52, 14, 17)):
            d.rectangle([x + bx, y + h - bh, x + bx + bw_, y + h],
                        fill=(28, 78, 186))
    elif no == 4:  # Kryvyi Rih: navy night, one huge burst
        d.rectangle([x, y, x + w, y + h], fill=NAVY)
        bx, by = cx, y + h // 2 - 2
        for a in range(0, 360, 30):
            r = 24 if a % 60 == 0 else 16
            d.line([(bx, by), (bx + r * math.cos(math.radians(a)),
                              by + r * math.sin(math.radians(a)))],
                   fill=ORANGE, width=4)
        d.ellipse([bx - 11, by - 11, bx + 11, by + 11], fill=GOLD)
        d.rectangle([x, y + h - 10, x + w, y + h], fill=BLACK)
    elif no == 5:  # Copenhagen: one giant eye
        d.rectangle([x, y, x + w, y + h], fill=TEAL)
        d.ellipse([cx - 62, y + 9, cx + 62, y + h - 9], fill=WHITE)
        d.ellipse([cx - 20, y + h // 2 - 20, cx + 20, y + h // 2 + 20], fill=RED)
        d.ellipse([cx - 8, y + h // 2 - 8, cx + 8, y + h // 2 + 8], fill=BLACK)
    elif no == 6:  # Kyiv: dusk sky, three big drones
        d.rectangle([x, y, x + w, y + h // 2], fill=PURPLE)
        d.rectangle([x, y + h // 2, x + w, y + h], fill=ORANGE)
        for ox, oy in ((-w // 3, 12), (0, 6), (w // 3, 14)):
            px, py = cx + ox, y + oy
            d.line([(px - 15, py), (px + 15, py)], fill=BLACK, width=5)
            d.line([(px, py - 9), (px, py + 9)], fill=BLACK, width=5)
            d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=BLACK)
        d.rectangle([x, y + h - 10, x + w, y + h], fill=BLACK)
    elif no == 7:  # Odisha: one huge cyclone spiral over teal sea
        d.rectangle([x, y, x + w, y + h], fill=TEAL)
        bx, by = cx, y + h // 2
        for r in (26, 19, 12):
            d.arc([bx - r, by - r, bx + r, by + r], 300, 300 + 290,
                  fill=WHITE, width=5)
        d.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=GOLD)
        d.rectangle([x, y + h - 8, x + w, y + h], fill=(10, 92, 140))
    elif no == 8:  # Brussels: royal blue, one giant gold euro coin
        d.rectangle([x, y, x + w, y + h], fill=(28, 78, 186))
        bx, by = cx, y + h // 2
        d.ellipse([bx - 27, by - 27, bx + 27, by + 27], fill=GOLD)
        d.ellipse([bx - 27, by - 27, bx + 27, by + 27], outline=(146, 96, 8), width=3)
        T(d, bx, by - 15, "€", AB(30), fill=(120, 74, 4), anchor="ma")
    elif no == 9:  # New York cyber: three towers + giant bolt
        d.rectangle([x, y, x + w, y + h], fill=(64, 196, 232))
        d.ellipse([x + 104, y + 20, x + 152, y + 32], fill=(252, 250, 244))
        for bx, bw_, bh in ((10, 26, 46), (44, 30, 54), (82, 24, 40)):
            d.rectangle([x + bx, y + h - bh, x + bx + bw_, y + h], fill=NAVY)
            for wy in range(y + h - bh + 6, y + h - 6, 10):
                d.rectangle([x + bx + 5, wy, x + bx + 12, wy + 5], fill=GOLD)
        bx, by = x + w - 42, y + 4
        d.polygon([(bx + 16, by), (bx, by + 30), (bx + 12, by + 30),
                   (bx + 2, by + 54), (bx + 30, by + 24), (bx + 17, by + 24)],
                  fill=RED)
    elif no == 10:  # Ulaanbaatar: one big waving flag over steppe
        d.rectangle([x, y, x + w, y + h], fill=SKY)
        d.rectangle([x, y + h - 12, x + w, y + h], fill=GREEN)
        px = x + 22
        d.line([(px, y + 4), (px, y + h - 4)], fill=INK, width=4)
        d.rectangle([px, y + 4, px + 96, y + 38], fill=RED)
        d.rectangle([px + 32, y + 4, px + 64, y + 38], fill=(28, 78, 186))
        d.rectangle([px, y + 20, px + 96, y + 24], fill=GOLD)
    elif no == 11:  # The Hague: big scales of justice on gold
        d.rectangle([x, y, x + w, y + h], fill=(250, 214, 120))
        bx, by = cx, y + 6
        d.line([(bx, by), (bx, y + h - 6)], fill=INK, width=5)
        d.line([(bx - 52, by + 8), (bx + 52, by + 8)], fill=INK, width=5)
        d.ellipse([bx - 6, by - 4, bx + 6, by + 8], fill=RED)
        for sx in (-52, 52):
            d.line([(bx + sx, by + 8), (bx + sx - 14, by + 34)], fill=INK, width=3)
            d.line([(bx + sx, by + 8), (bx + sx + 14, by + 34)], fill=INK, width=3)
            d.arc([bx + sx - 17, by + 24, bx + sx + 17, by + 44], 0, 180,
                  fill=INK, width=4)
        d.rectangle([bx - 20, y + h - 8, bx + 20, y + h - 3], fill=INK)
    elif no == 12:  # Johannesburg: three giant vote bars, tallest red
        d.rectangle([x, y, x + w, y + h], fill=SAND)
        d.ellipse([x + 12, y + 22, x + 58, y + 34], fill=(252, 250, 244))
        base = y + h - 6
        for i, (bh, col) in enumerate(((18, (120, 120, 116)),
                                       (30, (70, 70, 70)), (48, RED))):
            bx = cx - 52 + i * 38
            d.rectangle([bx, base - bh, bx + 26, base], fill=col)
        T(d, cx + 40, y + 6, "31%", AB(17), fill=RED, anchor="ma")
    elif no == 13:  # Wellington: big bat, ball and stumps on green
        d.rectangle([x, y, x + w, y + h // 2], fill=SKY)
        d.rectangle([x, y + h // 2, x + w, y + h], fill=GREEN)
        d.ellipse([x + 14, y + 18, x + 58, y + 29], fill=(252, 250, 244))
        d.rectangle([x + 60, y + h // 2 + 12, x + w - 60, y + h // 2 + 16],
                    fill=(252, 250, 244))
        d.line([(cx - 46, y + h - 8), (cx - 6, y + 10)], fill=(146, 96, 8), width=9)
        d.ellipse([cx + 16, y + 12, cx + 38, y + 34], fill=RED)
        for i in range(3):
            sx = x + w - 34 + i * 9
            d.line([(sx, y + h - 26), (sx, y + h - 6)], fill=GOLD, width=4)


# ------------------------------------------------------------------ cards ---
def draw_card(d, x, y, w, card, lead=False):
    no, place, region, cat, headline, deck, outlet, status, slug = card[:9]
    sh = 64 if lead else 60
    scene(d, x, y, w, sh, no)
    # chip first: white, black border, top-right INSIDE scene
    chip = f"{status} – {outlet}"
    cf = fit_font(d, chip, AB, 9, 118 if lead else 104, minsize=7)
    cw_ = tw(d, chip, cf) + 9
    d.rectangle([x + w - cw_, y, x + w, y + 16], fill=WHITE, outline=BLACK, width=1)
    T(d, x + w - cw_ + 4, y + 3, chip, cf, fill=INK)
    # slug: black box top-left INSIDE scene, sized against the real chip
    sf = AB(10) if lead else AB(8)
    slug_t = trunc(d, slug, sf, w - cw_ - 8)
    sw = tw(d, slug_t, sf) + 10
    d.rectangle([x, y, x + sw, y + 16], fill=BLACK)
    T(d, x + 5, y + 3, slug_t, sf, fill=WHITE)
    # location bar: black, full card width
    ly = y + sh
    d.rectangle([x, ly, x + w, ly + 20], fill=BLACK)
    lf = fit_font(d, place, AB, 12, w - 12, minsize=9)
    T(d, x + 6, ly + 4, place, lf, fill=WHITE)
    # badge row: red filled circle + REGION · CATEGORY in red bold caps
    by = ly + 25
    r = 10
    d.ellipse([x + 1, by, x + 1 + 2 * r, by + 2 * r], fill=RED)
    T(d, x + 1 + r, by + 4, str(no), AB(11), fill=WHITE, anchor="ma")
    rf = fit_font(d, f"{region} · {cat}", AB, 12 if lead else 11, w - 30,
                  minsize=9)
    T(d, x + 27, by + 4, f"{region} · {cat}", rf, fill=RED)
    # headline serif bold (lead one line ~16px; mini ~13px up to 2 lines)
    hy = by + 27
    if lead:
        hf = fit_font(d, headline, PF, 17, w - 4, minsize=13)
        T(d, x + 1, hy, headline, hf)
        hy += 24
    else:
        hf = PF(13)
        lines = wrap(d, headline, hf, w - 4)
        if len(lines) > 2:
            hf = fit_font(d, headline, PF, 12, w - 4, minsize=10)
            lines = wrap(d, headline, hf, w - 4)
        for ln in lines[:2]:
            T(d, x + 1, hy, ln, hf)
            hy += 16
        if len(lines) == 1:
            hy += 16
    # deck sans ~11px, <=3 lines, then the card body stays EMPTY (by design)
    df = AM(11) if lead else AM(10)
    pitch = 13 if lead else 12
    for ln in wrap(d, deck, df, w - 4)[:3 if lead else 2]:
        T(d, x + 1, hy, ln, df, fill=(38, 38, 38))
        hy += pitch


# -------------------------------------------------------------------- map ---
def continent_of(lon, lat):
    if lon < -30:
        return "AMERICAS"
    if lat < -10 and lon > 108:
        return "OCEANIA"
    if lon >= 35 and 12 < lat < 42 and lon < 63:
        return "MIDEAST"
    if lat >= 36 and lon < 45:
        return "EUROPE"
    if lat < 36 and lon < 52:
        return "AFRICA"
    return "ASIA"


def draw_map(d, x, y, w, h):
    mx0, my0, mx1, my1 = x + 2, y + 2, x + w - 2, y + h - 20

    def proj(lon, lat):
        px = mx0 + (lon + 168) / 360.0 * (mx1 - mx0)
        py = my0 + (76 - lat) / 132.0 * (my1 - my0)
        return px, py

    # landmass polygons with bounding boxes for the inside test
    rings = []
    for _name, pts in LANDMASSES:
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        rings.append((min(xs), min(ys), max(xs), max(ys), pts))

    def inside(lon, lat):
        for x0, y0, x1, y1, pts in rings:
            if x0 <= lon <= x1 and y0 <= lat <= y1:
                hit = False
                j = len(pts) - 1
                for i in range(len(pts)):
                    xi, yi = pts[i]
                    xj, yj = pts[j]
                    if (yi > lat) != (yj > lat) and \
                            lon < (xj - xi) * (lat - yi) / (yj - yi) + xi:
                        hit = not hit
                    j = i
                if hit:
                    return True
        return False

    step = 5.5
    lon = -166.0
    while lon < 190:
        lat = 74.0
        while lat > -56:
            if inside(lon, lat):
                px, py = proj(lon, lat)
                col = REG[continent_of(lon, lat)]
                d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=col)
            lat -= 3.4
        lon += 3.4
    # numbered pins for the 13 pictured stories
    nudge = {1: (0, -3), 5: (-5, -4), 6: (5, 3), 8: (-6, 2), 11: (-3, 6),
             3: (-4, -3), 9: (5, 4)}
    for c in CARDS:
        px, py = proj(c[9], c[10])
        dx, dy = nudge.get(c[0], (0, 0))
        px, py = px + dx, py + dy
        r = 8
        d.ellipse([px - r, py - r, px + r, py + r], fill=REG[c[2]],
                  outline=WHITE, width=2)
        T(d, px, py - 5, str(c[0]), AB(9), fill=WHITE, anchor="ma")
    # continent legend
    lx = x + 2
    ly = y + h - 15
    for name in ("EUROPE", "ASIA", "MIDEAST", "AFRICA", "AMERICAS", "OCEANIA"):
        d.rectangle([lx, ly + 1, lx + 8, ly + 9], fill=REG[name])
        T(d, lx + 11, ly, name, AB(8), fill=INK)
        lx += 11 + tw(d, name, AB(8)) + 9


# ------------------------------------------------------------------ briefs --
def draw_briefs(d, x, y, w):
    colw = (w - 12) // 2
    per = (len(BRIEFS) + 1) // 2
    nf, lf, tf = AB(9), AB(9), AM(9)
    for i, (no, lead, tail) in enumerate(BRIEFS):
        cx = x + (i // per) * (colw + 12)
        cy = y + (i % per) * 10.5
        num = f"{no} "
        T(d, cx, cy, num, nf, fill=RED)
        x1 = cx + tw(d, num, nf)
        d.text((x1, cy), lead, font=lf, fill=INK)
        x2 = x1 + tw(d, lead, lf) + 3
        tail_t = trunc(d, tail, tf, cx + colw - x2)
        d.text((x2, cy), tail_t, font=tf, fill=(38, 38, 38))


# ------------------------------------------------------------------- page ---
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # claims bar: paper name left (red caps), real counts right, red rule
    T(d, M, 5, "THE GLOBAL WIRE", AB(13), fill=RED)
    counts = "40 STORIES · 13 DRAWN · 6 CONTINENTS · ALL FROM 21 NOVEMBER"
    T(d, W - M, 6, counts, AB(11), fill=INK, anchor="ra")
    d.rectangle([M, 28, W - M, 30], fill=RED)

    # masthead = THE DATE ONLY, serif title case, cap >= 50px, natural width
    size = 100
    while size > 20:
        f = PF(size)
        bb = d.textbbox((0, 0), "S", font=f)
        if bb[3] - bb[1] <= 54:
            break
        size -= 1
    mast = "Saturday 21 November 2026"
    T(d, W // 2, 40, mast, f, anchor="ma")

    # day-parts bar
    dy = 126
    dh = 54
    d.rectangle([M, dy, M + 88, dy + dh], fill=RED)
    T(d, M + 44, dy + 8, "THE DAY", AB(11), fill=WHITE, anchor="ma")
    T(d, M + 44, dy + 22, "IN", AB(11), fill=WHITE, anchor="ma")
    T(d, M + 44, dy + 36, "PARTS", AB(11), fill=WHITE, anchor="ma")
    segw = (CW - 88 - 8) // 5
    for i, (lab, head) in enumerate(DAYPARTS):
        sx = M + 96 + i * segw
        if i:
            d.line([(sx - 5, dy + 4), (sx - 5, dy + dh - 4)],
                   fill=(205, 190, 160), width=1)
        T(d, sx, dy + 3, lab, AB(9), fill=RED)
        for j, ln in enumerate(wrap(d, head, AM(10), segw - 8)[:3]):
            T(d, sx, dy + 16 + j * 12, ln, AM(10), fill=INK)

    # three EQUAL leads
    ly = 190
    lw = (CW - 12) // 3
    for i, c in enumerate(CARDS[:3]):
        draw_card(d, M + i * (lw + 6), ly, lw, c, lead=True)

    # ten minis, 2 rows x 5
    mw = 194
    for r, row in enumerate((CARDS[3:8], CARDS[8:13])):
        ry = 382 + r * 168
        for i, c in enumerate(row):
            draw_card(d, M + i * (mw + 6), ry, mw, c)

    # section headers
    hy = 724
    T(d, M, hy, "WHERE IT HAPPENED", AB(13), fill=INK)
    T(d, W - M, hy, "ALSO ON SATURDAY 21 NOVEMBER", AB(13), fill=INK,
      anchor="ra")

    # map (bottom-left, ~40% width) + briefs right
    draw_map(d, M, 746, 396, 168)
    draw_briefs(d, 424, 748, W - M - 424)

    # DATE CHECK: red outline, red label block left, dated discards +
    # Unverified clause + not-yet (fits without costing a card or brief)
    cy = 924
    ch = 62
    d.rectangle([M, cy, W - M, cy + ch], outline=RED, width=2)
    d.rectangle([M, cy, M + 92, cy + ch], fill=RED)
    T(d, M + 46, cy + 16, "DATE", AB(12), fill=WHITE, anchor="ma")
    T(d, M + 46, cy + 31, "CHECK", AB(12), fill=WHITE, anchor="ma")
    for j, ln in enumerate(wrap(d, DATECHECK, AM(10), CW - 92 - 18)[:4]):
        T(d, M + 104, cy + 6 + j * 13, ln, AM(10), fill=(50, 26, 22))

    # footer, one line
    ff = fit_font(d, FOOTER, AM, 9, CW, minsize=7)
    T(d, M, 998, FOOTER, ff, fill=(90, 84, 70))
    return img


def save_quantized(img, path):
    q = img.quantize(colors=256, method=Image.MEDIANCUT,
                     dither=Image.FLOYDSTEINBERG)
    q.save(path, optimize=True)


def main():
    img = render()
    save_quantized(img, os.path.join(BASE, "entry.png"))
    img.resize((300, 300), Image.LANCZOS).save(
        os.path.join(BASE, "entry-300.png"))
    print("rendered entry.png + entry-300.png")


if __name__ == "__main__":
    main()
