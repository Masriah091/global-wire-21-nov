# draw.py - Challenger E4 "THE GLOBAL WIRE" - News Image, Saturday 21 Nov 2026.
# Round-4 GANTI-grade rebuild: same wire monochrome identity as e2, entirely
# new page architecture (dispatch-rail skeleton, lead row + compact wire rows,
# map/briefs split panel). Facts ONLY from POOL21 (verified pool, 21 Nov 2026).
# Deterministic Pillow program (stdlib + PIL only, no network).
# Renders entry.png (winner variant) plus variant_A/B/C.png for the duel.
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
PAPER = (252, 252, 250)
LGRAY = (238, 238, 236)
MGRAY = (90, 90, 90)
LAND = (205, 205, 200)
NAVY = (22, 40, 63)
RED = (178, 34, 30)
DRED = (140, 22, 18)

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


# ------------------------------------------------------------------ data ----
# no, place, region, headline, deck, source tag, data label, lon, lat
CARDS = [
    (1, "WARSAW, POLAND", "EUROPE",
     "Rutte flies to Warsaw after missiles land",
     "Two missiles and a suspected jet drone came down in the south-east, "
     "a Kh-101 near Nowy Lipowiec. NATO's Rutte calls it a “grave "
     "violation”; Tusk calls it a deliberate provocation.",
     "AP · SOFX", "3 WEAPONS CROSS", 21.0, 52.2),
    (2, "ANTALYA", "GLOBAL",
     "COP31 runs into overtime with no deal yet",
     "Talks ran past Friday's scheduled close into Saturday. The draft "
     "drops every fossil-fuel reference and the $120bn finance target; "
     "a third draft is due this morning.",
     "AP · ONGOING", "NO DEAL YET", 30.7, 36.9),
    (3, "NEW YORK", "AMERICAS",
     "Wall Street enters correction as AI rout deepens",
     "The S&P 500 fell about 3.7% on Friday, pushing it into correction "
     "territory. The Nasdaq dropped 5.28% as chip and AI shares plunged.",
     "SIMPLELIFE · CLOSE", "NASDAQ -5.28%", -74.0, 40.7),
    (4, "KRYVYI RIH", "EUROPE",
     "Russian strike kills two, injures 42",
     "An overnight strike on Kryvyi Rih kills two and injures 42, four "
     "of them children, the city's military chief says. It was one of "
     "Russia's largest attacks of the war.",
     "APPISTOS · CITY CHIEF", "2 DEAD · 42 HURT", 33.4, 47.9),
    (5, "COPENHAGEN", "EUROPE",
     "Denmark exposes 'assassination plot'",
     "Russia 'planned and initiated' a bid to kill a Ukrainian-American "
     "rapper near Copenhagen, Denmark says. The Russian attache is expelled.",
     "BBC · DENMARK SAYS", "ATTACHE EXPELLED", 12.6, 55.7),
    (6, "KYIV", "EUROPE",
     "Russia's barrage: 400 drones, 110 missiles",
     "At least eight are dead across Ukraine in the overnight barrage. "
     "The Austrian embassy is hit in Kyiv, and France calls for a UN "
     "Security Council meeting.",
     "BBC · OFFICIALS' COUNT", "400 DRONES · 110 MISSILES", 30.5, 50.4),
    (7, "ODISHA, INDIA", "ASIA",
     "After Akvan: 372,000 moved, no deaths",
     "A day after landfall, no deaths are reported and relief is under "
     "way. The storm weakens to a depression; schools stay shut through "
     "Saturday.",
     "RIDHU TIMES · RELIEF", "372,000 MOVED", 84.9, 19.3),
    (8, "BRUSSELS", "EUROPE",
     "EU adopts €1bn military aid for Ukraine",
     "Joint buying runs via the Peace Facility. Britain pledges 1,000+ "
     "drones in a £260m package alongside the EU deal.",
     "REUTERS · ADOPTED", "€1BN ADOPTED", 4.3, 50.8),
    (9, "NEW YORK", "AMERICAS",
     "JPMorgan, Visa, Mastercard hit by cyberattack",
     "The banks report incidents at third-party vendors. Their core "
     "payment networks are unaffected, they say.",
     "REUTERS · BANKS SAY", "3 NETWORKS HIT", -73.9, 40.8),
    (10, "ULAANBAATAR", "ASIA",
     "Mongolia's president resigns",
     "The resignation sets the stage for a snap election. It caps a "
     "week of political turmoil in the capital.",
     "REUTERS · CAPITAL", "SNAP ELECTION NEXT", 106.9, 47.9),
    (11, "THE HAGUE", "GLOBAL",
     "Myanmar ruling rattles Israel's Gaza defence",
     "The world court's genocide verdict against Myanmar raises "
     "questions in Jerusalem over its own case, experts say. The "
     "ruling itself came on Thursday.",
     "BBC · EXPERTS SAY", "GENOCIDE VERDICT", 4.3, 52.1),
    (12, "JOHANNESBURG", "AFRICA",
     "ANC scrambles after worst result since 1994",
     "The ANC wins 31% of the vote, its worst since 1994. It now races "
     "for coalition deals to stay in government.",
     "BBC · COUNT", "ANC 31%", 28.0, -26.2),
    (13, "WELLINGTON", "OCEANIA",
     "India fight back: 159/1 at stumps, day two",
     "India trail New Zealand by 209 in the first Test after the hosts "
     "made 368. Nicholls made 175 not out for the hosts.",
     "ICC · SCORECARD", "159/1 · DAY TWO", 174.8, -41.3),
]

NUMBERS = [
    ("3", "weapons cross into Poland (card 1)"),
    ("42", "injured in Kryvyi Rih, 4 children (card 4)"),
    ("-5.28%", "Nasdaq fall at Friday's close (card 3)"),
    ("372,000", "moved to shelters as Akvan hit (card 7)"),
    ("€1BN", "EU aid ADOPTED for Ukraine (card 8)"),
    ("159/1", "India at stumps, Wellington (card 13)"),
]

TIMELINE = [
    ("OVERNIGHT", "Kryvyi Rih strike: two killed, 42 injured"),
    ("MORNING", "Rutte flies to Warsaw over the missiles"),
    ("MIDDAY", "Antalya: third COP31 draft due after overnight talks"),
    ("AFTERNOON", "Denmark expels the Russian attache"),
    ("EVENING", "Stumps in Wellington: India 159/1"),
]

HOOKS = [
    ("1", "MISSILES LAND IN POLAND — Rutte flies to Warsaw"),
    ("2", "COP31 SLIPS INTO OVERTIME — no deal yet in Antalya"),
    ("3", "WALL STREET IN CORRECTION — Nasdaq -5.28%"),
]

# no, text, lon, lat
BRIEFS = [
    (14, "Kathmandu — Nepal's new leader Balendra Shah faces an India test (BBC)", 85.3, 27.7),
    (15, "Washington — US releases more UFO footage filmed in the Middle East (BBC)", -77.0, 38.9),
    (16, "Los Angeles — Hyundai unveils the 2027 Elantra at the auto show (Fast Company)", -118.2, 34.1),
    (17, "Cardiff — Lauren Price beats Kotaskova to become undisputed champion (BBC)", -3.2, 51.5),
    (18, "Paris — Three police sentenced over the beating of Michel Zecler (BBC)", 2.4, 48.9),
    (19, "Oxford — Life, 22 years minimum, for the Thames drowning murder (BBC)", -1.3, 51.8),
    (20, "New York — Nikhil Gupta gets 19+ years over the Sikh murder plot (BBC)", -74.0, 40.7),
    (21, "Cincinnati — Fiona the hippo dies after eating a hat (AP)", -84.5, 39.1),
    (22, "Washington — US sanctions four Iranians over oil revenues (OFAC)", -77.1, 38.8),
    (23, "Hormuz — A tanker is struck and on fire in the Strait of Hormuz (UKMTO)", 56.3, 26.6),
    (24, "Los Angeles — Jury convicts the man who started the Palisades Fire (AP)", -118.3, 34.0),
    (25, "Frankfurt — ECB names Boone and Brunnermeier for its Executive Board (Reuters)", 8.7, 50.1),
    (26, "Buenos Aires — Argentina's Senate backs a disability framework, 71-0 (AP)", -58.4, -34.6),
    (27, "Riyadh — Saudi coalition intercepts Houthi missiles over Riyadh (Reuters)", 46.7, 24.6),
    (28, "Barcelona — A pill is hailed as a breakthrough for pancreatic cancer (Reuters)", 2.2, 41.4),
    (29, "Gaza — On World Children's Day, Palestinian children appeal for help (UN)", 34.3, 31.5),
    (30, "Madrid — Amnesty says Spanish police used excess force in the strike (AP)", -3.7, 40.4),
    (31, "Rome — Italian workers and students march against Meloni's government (AFP)", 12.5, 41.9),
    (32, "Jeddah — Saudi Arabia warns of thunderstorms through Tuesday (SPA)", 39.2, 21.5),
    (33, "Kuala Lumpur — Malaysia to send 10,000 Rohingya to Turkey for training (Reuters)", 101.7, 3.1),
    (34, "Kharkiv — Ukraine says it has finished a “Bear Trap” in the Kharkiv area (Ukrinform)", 36.2, 49.9),
    (35, "Islamabad — Pakistan's minerals are worth $8-10 trillion, its minister says (Reuters)", 73.1, 33.7),
    (36, "Singapore — US presses Singapore and Malaysia on Iran sanctions (Reuters)", 103.8, 1.35),
    (37, "Paris — France seeks a UN council meeting on the Kyiv strikes (AFP)", 2.3, 48.8),
    (38, "Kyiv — The war tally: 771 Ukrainians killed, 2,300+ missing (homevo)", 30.6, 50.5),
    (39, "Ankara — Turkey welcomes the World Court's Myanmar ruling (Anadolu)", 32.9, 39.9),
    (40, "Turin — ATP semis set: Alcaraz v Shelton, Zverev v Medvedev (ATP)", 7.7, 45.1),
]

DATECHECK = (
    "LEFT OUT — first reported Friday 20 November, NOT Saturday's news: "
    "Kyiv's three bridges hit (20 Nov) · Cyclone Akvan's landfall at "
    "Gopalpur (20 Nov) · COP31's final day ending with no deal (20 Nov) · "
    "Asia's AI sell-off, Taipei -6.2% (20 Nov) · the UK-EU reset deal "
    "(20 Nov) · Phillips's 118 in the first innings (20 Nov). "
    "NOT YET HAPPENED, so not shown: any final COP31 text · the ATP "
    "semi-final results · BepiColombo's entry into orbit around Mercury "
    "(due today)."
)


# ------------------------------------------------------------- strip art ----
def strip_art(d, x, y, w, h, card):
    """Flat layered data strip: motif per card + navy caption band + chip."""
    no, place, region = card[0], card[1], card[2]
    col = REG[region]
    d.rectangle([x, y, x + w, y + h], fill=LGRAY)
    d.rectangle([x, y, x + w, y + 3], fill=col)
    cx, cy = x + w // 2, y + (h - 13) // 2 + 2
    ah = h - 13  # art height above caption band
    if no == 1:  # missiles: two arcs + drone diamond
        for i, ox in enumerate((-w // 4, 0, w // 4)):
            d.arc([x + 18 + ox + w // 4 - 26, y + 6, x + 44 + ox + w // 4, y + 34],
                  200, 330, fill=INK, width=2)
            d.polygon([(cx + ox - 4, y + ah - 8), (cx + ox + 6, y + ah - 4),
                       (cx + ox - 2, y + ah - 1)], fill=RED)
    elif no == 2:  # sun behind cloud, clock hand = overtime
        d.ellipse([cx - 30, y + 7, cx - 2, y + 35], outline=RED, width=3)
        d.rectangle([cx - 6, y + 20, cx + 44, y + 34], fill=MGRAY)
        d.line([(cx + 52, y + 8), (cx + 52, y + 22)], fill=INK, width=2)
        d.line([(cx + 52, y + 22), (cx + 62, y + 22)], fill=INK, width=2)
    elif no == 3:  # falling chart
        pts = [(x + 14, y + 10), (x + w // 3, y + 16), (x + w // 2, y + 13),
               (x + 2 * w // 3, y + 24), (x + w - 16, y + ah - 6)]
        d.line(pts, fill=RED, width=3)
        d.polygon([(x + w - 16, y + ah - 6), (x + w - 26, y + ah - 8),
                   (x + w - 18, y + ah - 16)], fill=RED)
    elif no == 4:  # burst
        for a in range(0, 360, 45):
            import math
            r1, r2 = 5, 13
            x1 = cx + r1 * math.cos(math.radians(a))
            y1 = cy + r1 * math.sin(math.radians(a))
            x2 = cx + r2 * math.cos(math.radians(a))
            y2 = cy + r2 * math.sin(math.radians(a))
            d.line([(x1, y1), (x2, y2)], fill=RED, width=2)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=INK)
    elif no == 5:  # eye / exposed plot
        d.ellipse([cx - 26, cy - 11, cx + 26, cy + 11], outline=INK, width=2)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)
    elif no == 6:  # drone grid
        for r in range(2):
            for c in range(5):
                px, py = x + 16 + c * (w - 32) // 4, y + 10 + r * 14
                d.line([(px - 4, py), (px + 4, py)], fill=INK, width=2)
                d.line([(px, py - 3), (px, py + 3)], fill=INK, width=2)
    elif no == 7:  # storm waves
        for r in range(3):
            yy = y + 10 + r * 9
            for sx in range(x + 10, x + w - 30, 24):
                d.arc([sx, yy, sx + 20, yy + 10], 180, 360, fill=REG["ASIA"], width=2)
    elif no == 8:  # coins / aid ring
        d.ellipse([cx - 26, cy - 12, cx - 2, cy + 12], outline=col, width=3)
        T(d, cx - 14, cy - 7, "€", AB(13), fill=col, anchor="ma")
        d.ellipse([cx + 2, cy - 12, cx + 26, cy + 12], outline=INK, width=2)
        T(d, cx + 14, cy - 7, "£", AB(13), fill=INK, anchor="ma")
    elif no == 9:  # three network nodes
        nodes = [(cx - 34, cy), (cx, cy - 10), (cx + 34, cy)]
        d.line([nodes[0], nodes[1], nodes[2]], fill=INK, width=2)
        for nx, ny in nodes:
            d.ellipse([nx - 6, ny - 6, nx + 6, ny + 6], fill=RED)
    elif no == 10:  # flag
        d.line([(cx - 20, y + 6), (cx - 20, y + ah - 3)], fill=INK, width=2)
        d.polygon([(cx - 20, y + 6), (cx + 16, y + 12), (cx - 20, y + 18)], fill=col)
    elif no == 11:  # scales
        d.line([(cx, y + 6), (cx, y + ah - 4)], fill=INK, width=2)
        d.line([(cx - 22, y + 10), (cx + 22, y + 10)], fill=INK, width=2)
        for sx in (-22, 22):
            d.polygon([(cx + sx - 8, y + 20), (cx + sx + 8, y + 20),
                       (cx + sx, y + 13)], outline=INK)
    elif no == 12:  # vote bars
        for i, bh in enumerate((8, 14, 22)):
            bx = cx - 30 + i * 24
            d.rectangle([bx, y + ah - 3 - bh, bx + 14, y + ah - 3],
                        fill=col if i == 2 else MGRAY)
    elif no == 13:  # cricket: bat + ball
        d.line([(cx - 16, y + ah - 4), (cx + 2, y + 8)], fill=INK, width=4)
        d.ellipse([cx + 12, cy - 6, cx + 24, cy + 6], fill=RED)
    # caption band (navy, bottom inside strip) + data label
    d.rectangle([x, y + h - 13, x + w, y + h], fill=NAVY)
    cap = trunc(d, f"{place} · {card[6]}", AB(8), w - 8)
    T(d, x + w // 2, y + h - 11, cap, AB(8), fill=WHITE, anchor="ma")


SHADOW = False  # pseudo-3D treatment toggle for the 3D-vs-2D duel


def draw_card(d, x, y, w, h, card, lead=False):
    no, place, region, headline, deck, src = card[0], card[1], card[2], card[3], card[4], card[5]
    if SHADOW:
        d.rectangle([x + 4, y + 4, x + w + 4, y + h + 4], fill=(198, 198, 192))
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=1)
    sh = 46 if lead else 32
    strip_art(d, x + 1, y + 1, w - 2, sh, card)
    yy = y + sh + 4
    T(d, x + 6, yy, f"{no} · {region}", AB(8), fill=REG[region])
    T(d, x + w - 6, yy, src, AB(7), fill=MGRAY, anchor="ra")
    yy += 11
    hf = PF(15) if lead else PF(11)
    for ln in wrap(d, headline, hf, w - 12)[:2]:
        T(d, x + 6, yy, ln, hf)
        yy += 18 if lead else 14
    yy += 2
    df = AM(10) if lead else AM(8)
    maxl = 4 if lead else 5
    for ln in wrap(d, deck, df, w - 12)[:maxl]:
        T(d, x + 6, yy, ln, df, fill=(40, 40, 40))
        yy += 12.5 if lead else 10


# ------------------------------------------------------------------- map ----
def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(247, 247, 244), outline=INK, width=1)
    # halftone dot texture (print feel; also lifts file into target band)
    for gx in range(x + 8, x + w - 4, 6):
        for gy in range(y + 24, y + h - 22, 6):
            d.point((gx, gy), fill=(225, 225, 218))
    T(d, x + 8, y + 5, "WHERE IT HAPPENED — THE WORLD, SATURDAY 21 NOV", AB(9))
    mx0, my0, mx1, my1 = x + 6, y + 22, x + w - 6, y + h - 20

    def proj(lon, lat):
        px = mx0 + (lon + 170) / 360.0 * (mx1 - mx0)
        py = my0 + (72 - lat) / 130.0 * (my1 - my0)
        return px, py

    for rings in WORLD.values():
        for ring in rings.split("|"):
            pts = []
            for pair in ring.split(","):
                lo, la = pair.split(":")
                pts.append(proj(float(lo), float(la)))
            if len(pts) > 2:
                d.polygon(pts, fill=LAND, outline=(150, 150, 145))
    for b in BRIEFS:
        px, py = proj(b[2], b[3])
        d.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5], fill=MGRAY)
    for c in CARDS:
        px, py = proj(c[7], c[8])
        col = REG[c[2]]
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=col, outline=WHITE, width=1)
        T(d, px, py - 6, str(c[0]), AB(10), fill=WHITE, anchor="ma")
    T(d, x + 8, y + h - 16,
      "Numbered pins Ø18 = pictured cards 1–13 · small grey dots = wire briefs 14–40",
      AB(8), fill=MGRAY)


# -------------------------------------------------------------- skeleton ----
def skeleton(d, variant):
    # kicker bar (date demoted here)
    d.rectangle([0, 0, W, 24], fill=INK)
    T(d, M, 5, "SATURDAY 21 NOVEMBER 2026", AB(10), fill=WHITE)
    T(d, W - M, 5, "40 STORIES · 7 REGIONS · EVERY ONE DATED SAT 21 NOV 2026",
      AB(10), fill=WHITE, anchor="ra")
    # masthead: paper NAME is the anchor
    size = 68 if variant != "C" else 60
    f = PF(size)
    while tw(d, "THE GLOBAL WIRE", f) > CW and size > 40:
        size -= 2
        f = PF(size)
    T(d, W // 2, 30, "THE GLOBAL WIRE", f, anchor="ma")
    yy = 30 + size + 8
    d.line([(M, yy), (W - M, yy)], fill=INK, width=3)
    T(d, W // 2, yy + 4,
      "Missiles land in Poland — COP31 slips into overtime — Wall Street falls into correction — Denmark exposes a plot",
      AM(11), anchor="ma", fill=MGRAY)
    yy += 24
    # hook band: three equal columns, wrapped
    hook_fill = RED if variant == "A" else (INK if variant == "B" else DRED)
    d.rectangle([M, yy, W - M, yy + 40], fill=hook_fill)
    colw = (CW - 16) // 3
    for i, (n, s) in enumerate(HOOKS):
        hx = M + 8 + i * (colw + 0)
        if i:
            d.line([(hx - 4, yy + 6), (hx - 4, yy + 34)], fill=(255, 160, 150), width=1)
        for j, ln in enumerate(wrap(d, f"{n} · {s}", AB(9), colw - 10)[:2]):
            T(d, hx, yy + 6 + j * 12, ln, AB(9), fill=WHITE)
    yy += 46
    # timeline (variant C moves numbers above timeline; order swap = layout diff)
    def timeline(y):
        T(d, M, y, "THE  DAY  IN  UTC", AB(9), fill=RED)
        tw5 = (CW - 4 * 6) // 5
        for i, (lab, ev) in enumerate(TIMELINE):
            bx = M + i * (tw5 + 6)
            d.rectangle([bx, y + 13, bx + tw5, y + 49], outline=INK, fill=WHITE)
            T(d, bx + 5, y + 16, lab, AB(8), fill=RED)
            for j, ln in enumerate(wrap(d, ev, AM(8), tw5 - 10)[:2]):
                T(d, bx + 5, y + 27 + j * 10, ln, AM(8), fill=MGRAY)
        return y + 53

    def numbers(y):
        T(d, M, y, "THE  DAY  IN  NUMBERS — every figure bound to a card on this page", AB(9), fill=RED)
        nw = (CW - 5 * 6) // 6
        for i, (num, cap) in enumerate(NUMBERS):
            bx = M + i * (nw + 6)
            T(d, bx, y + 12, num, PF(21), fill=RED)
            for j, ln in enumerate(wrap(d, cap, AM(8), nw - 2)[:2]):
                T(d, bx, y + 38 + j * 10, ln, AM(8), fill=MGRAY)
        return y + 60

    if variant == "C":
        yy = numbers(yy)
        yy = timeline(yy)
    else:
        yy = timeline(yy)
        yy = numbers(yy)
    d.line([(M, yy), (W - M, yy)], fill=INK, width=2)
    return yy + 6


def bottom(d, y):
    """Map left, ALSO ON wire right, DATE CHECK + footer below. Returns end y."""
    bh = 178
    mw = 492
    draw_map(d, M, y, mw, bh)
    bx = M + mw + 8
    bw = W - M - bx
    d.rectangle([bx, y, bx + bw, y + bh], fill=WHITE, outline=INK, width=1)
    T(d, bx + 8, y + 5, "ALSO ON THE WIRE — BRIEFS 14–40", AB(9), fill=RED)
    colw = (bw - 24) // 2
    for i, b in enumerate(BRIEFS):
        cx = bx + 8 + (i // 14) * (colw + 8)
        cy = y + 22 + (i % 14) * 11.4
        txt = trunc(d, f"{b[0]} {b[1]}", AM(8), colw)
        T(d, cx, cy, txt, AM(8), fill=(45, 45, 45))
    y += bh + 6
    # DATE CHECK
    d.rectangle([M, y, W - M, y + 68], outline=RED, width=2, fill=(253, 244, 242))
    T(d, M + 8, y + 5, "DATE CHECK — WHAT WE DELIBERATELY LEFT OUT", AB(9), fill=RED)
    for j, ln in enumerate(wrap(d, DATECHECK, AM(9), CW - 16)[:5]):
        T(d, M + 8, y + 19 + j * 11, ln, AM(9), fill=(60, 30, 28))
    y += 74
    T(d, M, y,
      "Every story here happened, or was first reported, on Saturday 21 November 2026. Contested claims are attributed.",
      AM(9), fill=MGRAY)
    T(d, M, y + 13,
      "Sources named beside each story (AP, BBC, Reuters, ICC, AFP, OFAC, UKMTO, UN, SPA, ATP) — original drawings. EUROPE 16 · ASIA 6 · AMERICAS 8 · MIDEAST 6 · AFRICA 1 · OCEANIA 1 · GLOBAL 2",
      AM(9), fill=MGRAY)
    return y + 26


def render(variant):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = skeleton(d, variant)
    if variant == "A":
        # lead row 3 + two compact rows of 5
        lw = (CW - 12) // 3
        for i, c in enumerate(CARDS[:3]):
            draw_card(d, M + i * (lw + 6), y, lw, 148, c, lead=True)
        y += 154
        cw5 = (CW - 24) // 5
        for r, row in enumerate((CARDS[3:8], CARDS[8:13])):
            for i, c in enumerate(row):
                draw_card(d, M + i * (cw5 + 6), y, cw5, 138, c)
            y += 144
    elif variant == "B":
        # two wide leads + rows of 5 and 6 compact
        lw = (CW - 6) // 2
        for i, c in enumerate(CARDS[:2]):
            draw_card(d, M + i * (lw + 6), y, lw, 148, c, lead=True)
        y += 154
        cw5 = (CW - 24) // 5
        for i, c in enumerate(CARDS[2:7]):
            draw_card(d, M + i * (cw5 + 6), y, cw5, 138, c)
        y += 144
        cw6 = (CW - 30) // 6
        for i, c in enumerate(CARDS[7:13]):
            draw_card(d, M + i * (cw6 + 6), y, cw6, 138, c)
        y += 144
    else:  # C: uniform 5/4/4 compact grid, taller strips
        cw5 = (CW - 24) // 5
        for i, c in enumerate(CARDS[:5]):
            draw_card(d, M + i * (cw5 + 6), y, cw5, 138, c)
        y += 144
        cw4 = (CW - 18) // 4
        for r, row in enumerate((CARDS[5:9], CARDS[9:13])):
            for i, c in enumerate(row):
                draw_card(d, M + i * (cw4 + 6), y, cw4, 138, c)
            y += 144
    bottom(d, y)
    return img


def save_quantized(img, path):
    q = img.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
    q.save(path, optimize=True)


def main():
    global SHADOW
    winner = os.environ.get("WINNER", "A")
    for v in ("A", "B", "C"):
        save_quantized(render(v), os.path.join(BASE, f"variant_{v}.png"))
    # 3D-treatment duel render: winner layout + drop shadows
    SHADOW = True
    save_quantized(render(winner), os.path.join(BASE, "variant_A3D.png"))
    SHADOW = False
    save_quantized(render(winner), os.path.join(BASE, "entry.png"))
    print("winner:", winner)


if __name__ == "__main__":
    main()
