"""render_ep06.py — EP06 "La Mala Hora" (New Mexico, Hispanic New Mexican legend) in the Dark Atlas Tales style, Milo narration.
Usage: python -I render_ep06.py <dark_atlas_dir> [stills "t1,t2,..." [out.jpg]]
Per-episode variations (see skill: bảng biến thể): title = a descanso candle gutters out and its smoke forms the title;
soft transitions = SHADOW WIPE (her dark shawl sweeps across the frame); camera = long LATERAL slides + very slow push-ins;
grade = cold indigo/violet near-monochrome with one warm accent (chile ristra red); reveal = SLOW HEAD TURN at the crossroads;
hook accent = her shadow walks across the hook card behind the letters; cold open = a figure standing dead still at a crossroads.
Scene plan + T() anchors: EP06_la_mala_hora/TT/out/05-TT-KIT-SCENES-la-mala-hora-new-mexico.md
"""
import sys, os, json, math, random, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from style import *

ROOT = sys.argv[1]; EP = os.path.join(ROOT, "EP06_la_mala_hora")
FB = os.path.join(ROOT, "fonts", "Oswald-Bold.ttf"); FR = os.path.join(ROOT, "fonts", "Oswald-Regular.ttf")
words = [w for s in json.load(open(os.path.join(EP, "voice_milo_transcript.json"), encoding="utf-8")) for w in s["words"]]
norm = lambda s: "".join(c for c in s.lower() if c.isalnum())
def T(word, n=1, end=False):
    k = 0
    for w in words:
        if norm(w["w"]) == norm(word):
            k += 1
            if k == n: return w["e"] if end else w["s"]
    raise KeyError((word, n))
VOICE_END = words[-1]["e"]; END = VOICE_END + 0.75

STY = json.load(open(os.path.join(EP, "style.json"), encoding="utf-8"))
tup = lambda k: tuple(STY[k])
SKY_T6, SKY_B6 = tup("sky_t"), tup("sky_b")
EARTH, EARTH_D, EARTH_L = tup("earth"), tup("earth_d"), tup("earth_l")
ADOBE, ADOBE_D, ADOBE_L = tup("adobe"), tup("adobe_d"), tup("adobe_l")
CHAM, CHAM_D = tup("chamisa"), tup("chamisa_d")
REB, REB_D, REB_S = tup("rebozo"), tup("rebozo_d"), tup("rebozo_sheen")
MSK, MSK_D, MEYE, MTEETH = tup("mh_skin"), tup("mh_skin_d"), tup("mh_eye"), tup("mh_teeth")
DEN, DEN_D, TAN = tup("walker_denim"), tup("walker_denim_d"), tup("walker_tan")
SHAWL, SHAWL_D = tup("wife_shawl"), tup("wife_shawl_d")
RIS, RIS_D = tup("ristra"), tup("ristra_d")
CROSS = tup("descanso_cross"); FLOWERS = [tuple(c) for c in STY["plastic_flowers"]]
VOTIVE = tup("votive"); ZIA_Y, ZIA_R = tup("zia_sign_yellow"), tup("zia_sign_red"); FLASH = tup("flash_jumpscare")
SKIN = (196, 156, 124); SKIN_D = (160, 122, 96); DK = (8, 7, 10); HAIRD = (22, 18, 18)
TORCH = (255, 236, 190)

def dim(c, k): return tuple(int(min(255, v * k)) for v in c[:3])
def flk(lt, ph=0.0): return 0.82 + 0.10 * math.sin(lt * 9 + ph) + 0.08 * math.sin(lt * 23 + ph * 2)
BG = (-460, -120, 1540, 2040)       # wide plates for long lateral slides

# ================= scenery =================
def nm_sky(P, seed, stars_n=200):
    P.gfill(SKY_T6, SKY_B6); stars(P, (P.x0, P.y0, P.x1, P.y0 + (P.y1 - P.y0) * 0.5), stars_n, seed, a=150)

def sangre(P, base, seed, hmin=200, hmax=360):
    mountains(P, base, range_peaks(P.x0 - 200, P.x1 + 200, base, hmin, hmax, 140, 230, seed), light=(78, 74, 104), dark=(54, 50, 76), haze=(40, 34, 60))
    haze(P, base, 130, (46, 40, 70), 150)

def chamisa(P, x, y, s, col, seed):
    r = random.Random(seed)
    for _ in range(8): P.ell((x + r.uniform(-50, 50) * s, y - r.uniform(20, 70) * s, x + r.uniform(-50, 50) * s + 56 * s, y + 6 * s), dim(col, r.uniform(0.8, 1.1)))
    for _ in range(5): P.line([(x + 25 * s, y), (x + r.uniform(-20, 70) * s, y - r.uniform(40, 80) * s)], dim(col, 0.6), 3 * s)

def floor(P, y, seed, n=40):
    P.gpoly([(P.x0, y), (P.x1, y), (P.x1, P.y1), (P.x0, P.y1)], EARTH, EARTH_D, y, P.y1)
    r = random.Random(seed)
    for i in range(n):
        yy = y + 30 + (i / n) ** 1.4 * (P.y1 - y - 120); s = 0.25 + (yy - y) / (P.y1 - y) * 1.3
        chamisa(P, r.uniform(P.x0, P.x1), yy, s, CHAM_D, seed + i)

def bottom_dark(P): P.gpoly([(P.x0, 1860), (P.x1, 1860), (P.x1, P.y1), (P.x0, P.y1)], (6, 6, 10, 0), (3, 3, 5, 255))

def road(P, vx, vy, w_far, w_near, y_near, col=None):
    """dirt road receding to (vx, vy): w_far at the horizon, w_near at y_near."""
    c = col or dim(EARTH_L, 0.9)
    P.gpoly([(vx - w_far / 2, vy), (vx + w_far / 2, vy), (540 + w_near / 2, y_near), (540 - w_near / 2, y_near)], dim(c, 0.75), c, vy, y_near)
    for k in (-1, 1): P.line([(vx + k * w_far * 0.18, vy), (540 + k * w_near * 0.2, y_near)], dim(c, 0.82), 6)      # wheel ruts

def cross_road(P, y, h_far, h_near_y, col=None):
    """the crossing road: a band across the frame widening toward the camera."""
    c = col or dim(EARTH_L, 0.85)
    P.gpoly([(P.x0, y - h_far / 2), (P.x1, y - h_far / 2), (P.x1, y + h_far / 2), (P.x0, y + h_far / 2)], dim(c, 0.8), c)

def descanso(P, x, base, s, seed=0, candle=False):
    r = random.Random(seed)
    P.ell((x - 60 * s, base - 14 * s, x + 60 * s, base + 14 * s), (0, 0, 0, 90))
    for i in range(5): P.ell((x - 50 * s + i * 22 * s, base - 22 * s, x - 22 * s + i * 22 * s, base + 4 * s), dim(EARTH_L, r.uniform(0.7, 1.0)))   # stones
    P.rect((x - 9 * s, base - 260 * s, x + 9 * s, base), CROSS); P.rect((x - 62 * s, base - 200 * s, x + 62 * s, base - 182 * s), CROSS)
    P.line([(x + 9 * s, base - 255 * s), (x + 9 * s, base - 4 * s)], dim(CROSS, 0.7), 3 * s)
    for i in range(7):                                                                                               # plastic flowers
        fx = x + r.uniform(-50, 50) * s; fy = base - r.uniform(150, 215) * s; P.circ(fx, fy, r.uniform(9, 14) * s, FLOWERS[i % 3])
    P.line([(x - 40 * s, base - 191 * s), (x + 40 * s, base - 191 * s)], (40, 100, 60), 4 * s)
    if candle:
        P.rrect((x + 26 * s, base - 70 * s, x + 56 * s, base - 8 * s), 4 * s, (200, 60, 70)); P.rect((x + 30 * s, base - 66 * s, x + 52 * s, base - 30 * s), (230, 150, 110))

def zia_sign(P, x, base, s, num="68"):
    P.rect((x - 7 * s, base - 300 * s, x + 7 * s, base), (70, 70, 80))
    P.rect((x - 70 * s, base - 430 * s, x + 70 * s, base - 290 * s), ZIA_Y)
    cx, cy = x, base - 360 * s
    P.circ(cx, cy, 30 * s, ZIA_R)
    for ang in (0, 90, 180, 270):
        a = math.radians(ang)
        for j in range(4):
            o = (j - 1.5) * 9 * s; px, py = -math.sin(a) * o, math.cos(a) * o
            P.line([(cx + math.cos(a) * 34 * s + px, cy + math.sin(a) * 34 * s + py), (cx + math.cos(a) * 58 * s + px, cy + math.sin(a) * 58 * s + py)], ZIA_R, 4 * s)
    f = ImageFont.truetype(FB, max(8, int(26 * s * P.k))); P.d.text(P.P(cx, cy), num, font=f, fill=ZIA_Y + (255,), anchor="mm")

def adobe_church(P, cx, base, s, lit=0.0):
    c, d, l = ADOBE, ADOBE_D, ADOBE_L
    P.rrect((cx - 220 * s, base - 360 * s, cx + 220 * s, base), 26 * s, c)                                    # nave front
    for sx in (-1, 1):                                                                                       # two bell towers
        tx = cx + sx * 190 * s
        P.rrect((tx - 80 * s, base - 560 * s, tx + 80 * s, base), 20 * s, d if sx > 0 else c)
        P.rrect((tx - 60 * s, base - 640 * s, tx + 60 * s, base - 540 * s), 16 * s, dim(d if sx > 0 else c, 0.95))
        P.chord((tx - 28 * s, base - 630 * s, tx + 28 * s, base - 560 * s), 180, 360, (16, 12, 18)); P.rect((tx - 28 * s, base - 596 * s, tx + 28 * s, base - 566 * s), (16, 12, 18))
        P.rect((tx - 4 * s, base - 720 * s, tx + 4 * s, base - 640 * s), (40, 32, 36)); P.rect((tx - 22 * s, base - 700 * s, tx + 22 * s, base - 692 * s), (40, 32, 36))
    P.chord((cx - 70 * s, base - 230 * s, cx + 70 * s, base - 90 * s), 180, 360, (34, 22, 24)); P.rect((cx - 70 * s, base - 160 * s, cx + 70 * s, base), (34, 22, 24))   # door
    for i in range(6): P.rect((cx - 200 * s + i * 76 * s, base - 352 * s, cx - 184 * s + i * 76 * s, base - 334 * s), (60, 40, 36))  # vigas
    P.circ(cx, base - 280 * s, 22 * s, (200, 150, 90) if lit else (40, 30, 34))
    P.line([(cx - 214 * s, base - 356 * s), (cx + 214 * s, base - 356 * s)], l, 3 * s)

def adobe_house(P, x, base, w, h, lit=1.0, ristra=True, seed=0):
    P.rrect((x, base - h, x + w, base), 18, ADOBE if seed % 2 else dim(ADOBE, 0.9))
    for i in range(int(w / 60)): P.rect((x + 20 + i * 60, base - h + 14, x + 34 + i * 60, base - h + 30), (54, 36, 32))
    for wx in (x + w * 0.22, x + w * 0.62):
        P.rect((wx, base - h * 0.62, wx + w * 0.16, base - h * 0.32), (255, 196, 110) if lit > 0.5 else (24, 20, 28))
        P.rect((wx - 4, base - h * 0.62, wx + w * 0.16 + 4, base - h * 0.64), (70, 50, 40))
    if ristra: hang_ristra(P, x + w * 0.9, base - h + 24, 7, 1.0)

def hang_ristra(P, x, y, n, s):
    P.line([(x, y), (x, y + n * 26 * s + 10)], (60, 40, 30), 3 * s)
    for i in range(n):
        yy = y + 12 * s + i * 26 * s
        for dx in (-1, 1): P.poly([(x + dx * 4 * s, yy), (x + dx * 20 * s, yy + 10 * s), (x + dx * 8 * s, yy + 40 * s)], RIS if (i + dx) % 2 else RIS_D)

def pickup(P, x, base, s):
    P.ell((x - 300 * s, base - 20 * s, x + 300 * s, base + 20 * s), (0, 0, 0, 120))
    P.rrect((x - 280 * s, base - 150 * s, x + 280 * s, base - 40 * s), 20 * s, (34, 40, 52))
    P.rrect((x - 120 * s, base - 260 * s, x + 90 * s, base - 140 * s), 24 * s, (38, 44, 58)); P.rect((x - 96 * s, base - 240 * s, x + 66 * s, base - 160 * s), (14, 18, 28))
    for wx in (-180, 180): P.circ(x + wx * s, base - 40 * s, 52 * s, (10, 10, 12)); P.circ(x + wx * s, base - 40 * s, 22 * s, (60, 60, 70))
    P.circ(x + 262 * s, base - 110 * s, 16 * s, (255, 240, 200))

# ================= characters =================
def mala_hora(P, x, feet, h, view="back", wind=0.0):
    """tall woman in a long black dress; a black rebozo covers head and shoulders. view: back | three | front | sil."""
    k = h / 1000.0
    def X(v): return x + v * k
    def Y(v): return feet - v * k
    sheen = REB_S; c = REB; d = REB_D
    P.ell((X(-200), Y(16), X(200), Y(-16)), (0, 0, 0, 100))
    P.gpoly([(X(-110), Y(640)), (X(110), Y(640)), (X(190), Y(200)), (X(230 + wind * 30), Y(0)), (X(-230 + wind * 10), Y(0)), (X(-190), Y(200))], c, d, Y(640), Y(0))     # skirt
    for fx in (-120, -40, 40, 120): P.line([(X(fx * 0.5), Y(600)), (X(fx * 1.1), Y(20))], d, 6 * k)
    w = wind * 40
    P.gpoly([(X(-70), Y(1000)), (X(70), Y(1000)), (X(150), Y(860)), (X(170), Y(560)), (X(200 + w), Y(470)), (X(120), Y(500)), (X(-120), Y(500)), (X(-190 + w * 0.3), Y(480)), (X(-160), Y(560)), (X(-150), Y(860))], c, d, Y(1000), Y(470))   # rebozo
    for i in range(10): fx = -180 + i * 40 + w * (i / 10); P.line([(X(fx), Y(490)), (X(fx + w * 0.3 + 4), Y(430))], d, 4 * k)                                         # fringe
    if view == "sil":
        return
    P.arc((X(-150), Y(1010), X(150), Y(560)), 200, 340, sheen, 5 * k)                                    # violet rim light
    P.line([(X(150), Y(860)), (X(170), Y(560))], sheen, 4 * k)
    if view in ("three", "front"):
        off = 30 if view == "three" else 0
        P.ell((X(-62 + off), Y(940), X(62 + off), Y(780)), (14, 10, 18))                                 # hood opening
        P.ell((X(-46 + off), Y(925), X(46 + off), Y(795)), MSK_D if view == "three" else MSK)
        if view == "front":
            P.pie((X(-46), Y(925), X(46), Y(795)), -90, 90, MSK_D)
            for ex in (-18, 18): P.ell((X(ex - 12), Y(880), X(ex + 12), Y(864)), MEYE)
            P.line([(X(-14), Y(826)), (X(14), Y(826))], (40, 30, 40), 3 * k)

def mh_face(mode="still"):
    """big portrait of La Mala Hora: black rebozo framing a grey-violet face, split tone, milky white eyes,
    thin mouth; mode 'scream' = mouth open with thin pale teeth (jumpscare / reveal). No blood."""
    D = Painter((-60, 260, 1140, 1980), res=1.2)
    D.gpoly([(40, 2000), (110, 1320), (300, 1080), (780, 1080), (970, 1320), (1040, 2000)], REB, REB_D, 1080, 2000)   # shoulders under the shawl
    D.ell((150, 300, 930, 1500), REB); D.ell((240, 420, 840, 1400), (12, 9, 16))                                    # hood + inner shadow
    D.arc((160, 310, 920, 1490), 200, 330, REB_S, 10)
    D.ell((310, 520, 770, 1260), MSK); D.pie((310, 520, 770, 1260), -90, 90, MSK_D)                                    # face, split tone
    D.chord((290, 470, 790, 760), 180, 360, (12, 9, 16))                                                              # hood edge over the brow
    for sx in (-1, 1):
        cx = 540 + sx * 110
        D.ell((cx - 92, 760, cx + 92, 900), dim(MSK_D, 0.6))                                                          # sunken sockets
        D.ell((cx - 66, 786, cx + 66, 876), MEYE); D.ell((cx - 24, 808, cx + 24, 856), (196, 198, 208))               # milky, no pupils
        D.arc((cx - 80, 770, cx + 80, 890), 200, 340, dim(MSK_D, 0.55), 8)
    D.poly([(530, 880), (552, 880), (574, 1010), (508, 1010)], MSK_D)
    if mode == "scream":
        D.ell((430, 1060, 650, 1210), (16, 8, 14))
        for i in range(11): tx = 446 + i * 18; D.poly([(tx, 1074), (tx + 14, 1074), (tx + 7, 1118)], MTEETH)
        for i in range(10): tx = 454 + i * 19; D.poly([(tx, 1196), (tx + 14, 1196), (tx + 7, 1160)], dim(MTEETH, 0.85))
    else:
        D.line([(470, 1120), (540, 1130), (610, 1120)], (40, 26, 36), 7)
    for i in range(6): D.arc((350 + i * 4, 1180 + i * 10, 730 - i * 4, 1260 + i * 10), 20, 160, dim(MSK_D, 0.8), 3)    # cheek/jaw lines
    return D.sprite()

def mh_eye_glints():
    E = Painter((380, 790, 700, 880), res=2)
    for sx in (-1, 1): cx = 540 + sx * 110; E.circ(cx + 22, 812, 9, (255, 255, 255)); E.circ(cx - 20, 846, 4, (220, 220, 236))
    return E.sprite()

def walker(P, x, feet, h, view="back", torch=True):
    k = h / 1000.0
    def X(v): return x + v * k
    def Y(v): return feet - v * k
    P.ell((X(-150), Y(14), X(150), Y(-14)), (0, 0, 0, 110))
    for lx in (-70, 18): P.rect((X(lx), Y(470), X(lx + 54), Y(10)), dim(TAN, 0.55)); P.rrect((X(lx - 6), Y(40), X(lx + 64), Y(0)), 8 * k, (30, 24, 22))
    P.rrect((X(-120), Y(800), X(120), Y(440)), 40 * k, DEN_D if view == "back" else DEN)
    P.line([(X(-120), Y(760)), (X(-150), Y(470))], DEN_D, 46 * k)
    if torch:
        P.line([(X(120), Y(760)), (X(190), Y(560))], DEN_D, 46 * k); P.rect((X(180), Y(590), X(250), Y(540)), (50, 50, 56)); P.circ(X(252), Y(565), 18 * k, TORCH)
    else:
        P.line([(X(120), Y(760)), (X(150), Y(470))], DEN_D, 46 * k)
    P.ell((X(-70), Y(990), X(70), Y(810)), HAIRD if view == "back" else SKIN)
    if view != "back": P.chord((X(-74), Y(1000), X(74), Y(880)), 180, 360, HAIRD)

def walker_portrait():
    D = Painter((-60, 300, 1140, 1980), res=1.2)
    D.chord((60, 1320, 1020, 2300), 180, 360, DEN); D.rect((60, 1800, 1020, 1980), DEN)
    D.poly([(380, 1360), (540, 1520), (700, 1360), (760, 1420), (540, 1640), (320, 1420)], DEN_D)                         # jacket collar
    for x in range(140, 1000, 120): D.line([(x, 1500), (x, 1980)], DEN_D, 4)
    D.rect((470, 1170, 610, 1360), SKIN_D)
    D.ell((330, 590, 750, 1220), SKIN); D.pie((330, 590, 750, 1220), -90, 90, SKIN_D)
    D.chord((310, 520, 770, 860), 180, 360, HAIRD); D.poly([(316, 700), (350, 690), (340, 900), (312, 860)], HAIRD); D.poly([(764, 700), (730, 690), (740, 900), (768, 860)], HAIRD)
    D.arc((400, 790, 500, 830), 200, 340, (70, 46, 34), 9); D.arc((580, 790, 680, 830), 200, 340, (70, 46, 34), 9)
    D.line([(546, 890), (530, 990)], (150, 110, 84), 5); D.arc((520, 980, 560, 1002), 10, 170, (150, 110, 84), 5)
    D.ell((508, 1060, 572, 1104), (70, 34, 28))
    D.glow(540, 1260, 420, (255, 232, 180), 0.45, 1.6)                                                                   # flashlight from below
    face = D.sprite()
    E = Painter((400, 840, 700, 910), res=2)
    for ex in (456, 624):
        cy = 870; E.ell((ex - 38, cy - 20, ex + 38, cy + 20), (238, 230, 218)); E.circ(ex + 12, cy, 11, (50, 34, 22)); E.circ(ex + 12, cy, 5, (6, 4, 4)); E.circ(ex + 8, cy - 4, 3, (255, 255, 255))
        E.arc((ex - 40, cy - 24, ex + 40, cy + 18), 195, 345, (24, 16, 12), 6)
    return face, E.sprite()

def woman_villager(P, x, feet, h, hands_up=False):
    """woman in a teal shawl over her head and a dark skirt (the wife). Front view, simple."""
    k = h / 1000.0
    def X(v): return x + v * k
    def Y(v): return feet - v * k
    P.ell((X(-170), Y(14), X(170), Y(-14)), (0, 0, 0, 110))
    P.gpoly([(X(-100), Y(560)), (X(100), Y(560)), (X(170), Y(0)), (X(-170), Y(0))], (40, 34, 44), (26, 22, 30), Y(560), Y(0))
    P.gpoly([(X(-70), Y(1000)), (X(70), Y(1000)), (X(150), Y(820)), (X(160), Y(500)), (X(-160), Y(500)), (X(-150), Y(820))], SHAWL, SHAWL_D, Y(1000), Y(500))
    P.ell((X(-48), Y(940), X(48), Y(800)), SKIN); P.pie((X(-48), Y(940), X(48), Y(800)), -90, 90, SKIN_D)
    P.chord((X(-56), Y(960), X(56), Y(860)), 180, 360, SHAWL_D)
    for ex in (-18, 18): P.circ(X(ex), Y(872), 6 * k, (30, 20, 18))
    if hands_up:
        for sx in (-1, 1): P.ell((X(sx * 30 - 22), Y(840), X(sx * 30 + 22), Y(790)), SKIN)
        P.ell((X(-12), Y(832), X(12), Y(812)), (50, 24, 24))

def wall_clock(P, cx, cy, r, hh=12, mm=0):
    P.rrect((cx - r * 0.5, cy + r * 0.8, cx + r * 0.5, cy + r * 3.0), r * 0.1, (70, 44, 30)); P.rect((cx - r * 0.36, cy + r * 1.0, cx + r * 0.36, cy + r * 2.8), (30, 22, 20))
    P.line([(cx, cy + r * 1.0), (cx, cy + r * 2.3)], (190, 160, 90), r * 0.04); P.circ(cx, cy + r * 2.4, r * 0.16, (200, 170, 96))     # still pendulum
    P.circ(cx, cy, r * 1.1, (80, 52, 34)); P.circ(cx, cy, r, (226, 216, 190))
    for i in range(12):
        a = math.radians(i * 30 - 90); P.line([(cx + math.cos(a) * r * 0.82, cy + math.sin(a) * r * 0.82), (cx + math.cos(a) * r * 0.94, cy + math.sin(a) * r * 0.94)], (40, 30, 24), r * (0.05 if i % 3 == 0 else 0.025))
    ah = math.radians((hh % 12) * 30 + mm * 0.5 - 90); am = math.radians(mm * 6 - 90)
    P.line([(cx, cy), (cx + math.cos(ah) * r * 0.5, cy + math.sin(ah) * r * 0.5)], (20, 16, 14), r * 0.06)
    P.line([(cx, cy), (cx + math.cos(am) * r * 0.78, cy + math.sin(am) * r * 0.78)], (20, 16, 14), r * 0.04); P.circ(cx, cy, r * 0.05, (20, 16, 14))

def smoke_puff(res=0.5):
    G = Painter((-120, -120, 120, 120), res=res, ss=1); G.glow(0, 0, 120, (150, 140, 170), 1.0, 1.2); return G.sprite()

# ================= plates =================
def crossroads_plate(seed=1, fig=True, top_down=False):
    P = Painter(BG, res=1.0)
    if top_down:
        P.gfill(dim(EARTH, 0.9), EARTH_D)
        r = random.Random(seed)
        P.rect((BG[0], 840, BG[2], 1080), dim(EARTH_L, 0.9)); P.rect((420, BG[1], 660, BG[3]), dim(EARTH_L, 0.92))
        for _ in range(70): chamisa(P, r.uniform(BG[0], BG[2]), r.uniform(BG[1], BG[3]), r.uniform(0.6, 1.1), CHAM_D, r.randint(0, 999))
        P.rect((BG[0], 840, BG[2], 1080), dim(EARTH_L, 0.9)); P.rect((420, BG[1], 660, BG[3]), dim(EARTH_L, 0.92))
        for (x, y) in ((360, 790), (720, 1130)): descanso(P, x, y, 0.5, x)
        return P.sprite()
    nm_sky(P, seed); sangre(P, 1080, seed + 1)
    floor(P, 1080, seed + 2, 34)
    road(P, 560, 1080, 30, 1300, 2040); cross_road(P, 1210, 70, 0)
    for (x, y, s) in ((240, 1260, 0.5), (900, 1300, 0.6), (60, 1760, 0.9)): descanso(P, x, y, s, int(x))
    zia_sign(P, 980, 1240, 0.55)
    bottom_dark(P)
    return P.sprite()

def village_plate(seed=7, lit=1.0):
    P = Painter(BG, res=1.0); nm_sky(P, seed); sangre(P, 1040, seed + 1, 260, 420)
    floor(P, 1150, seed + 2, 20)
    adobe_church(P, 560, 1260, 1.0, lit)
    for (x, w, h) in ((-420, 300, 220), (-90, 260, 200), (860, 300, 230), (1200, 260, 210)): adobe_house(P, x, 1300, w, h, lit, True, x)
    bottom_dark(P)
    return P.sprite()

def desert_road_plate(seed=11):
    P = Painter(BG, res=1.0); nm_sky(P, seed); sangre(P, 1060, seed + 1, 300, 520)
    floor(P, 1060, seed + 2, 40)
    road(P, 700, 1060, 24, 900, 2040)
    zia_sign(P, 300, 1420, 0.9, "76")
    bottom_dark(P)
    return P.sprite()

def descanso_row_plate(seed=13):
    P = Painter(BG, res=1.0); nm_sky(P, seed, 120); sangre(P, 980, seed + 1)
    floor(P, 980, seed + 2, 24)
    road(P, 300, 980, 20, 1600, 2040)
    for i, (x, y, sc) in enumerate(((620, 1000, 0.3), (760, 1030, 0.38), (900, 1070, 0.48), (1060, 1120, 0.6), (1230, 1880, 1.5), (-40, 1900, 1.6))): descanso(P, x, y, sc, i)
    bottom_dark(P)
    return P.sprite()

def descanso_close_plate(seed=17):
    P = Painter((-160, -120, 1240, 2040), res=1.0); P.gfill(SKY_T6, SKY_B6); stars(P, (-160, -120, 1240, 700), 90, seed)
    P.gpoly([(-160, 1060), (1240, 1060), (1240, 2040), (-160, 2040)], EARTH, EARTH_D)
    descanso(P, 540, 1120, 2.3, 3, candle=True); bottom_dark(P)
    return P.sprite()

def moon_plain_plate(seed=19):
    P = Painter(BG, res=1.0); nm_sky(P, seed, 150); floor(P, 1360, seed + 1, 18); road(P, 540, 1360, 40, 700, 2040); bottom_dark(P)
    return P.sprite()

def interior_plate(dawn=False, wall_only=False):
    P = Painter((-160, -120, 1240, 2040), res=1.0)
    P.gfill(dim(ADOBE, 0.45), dim(ADOBE_D, 0.35))
    for i in range(8): P.rect((-160 + i * 190, -120, -100 + i * 190, 60), (50, 34, 30))                   # vigas
    if not wall_only:
        P.rect((720, 380, 1040, 820), (70, 96, 150) if dawn else (16, 18, 34)); P.rect((872, 380, 888, 820), (50, 36, 30)); P.rect((720, 592, 1040, 606), (50, 36, 30))
        if dawn: P.glow(880, 600, 520, (120, 150, 210), 0.35, 1.4)
        hang_ristra(P, 640, 60, 11, 1.6)
        P.rect((-160, 1420, 1240, 2040), (44, 30, 28)); P.rect((-60, 1320, 640, 1360), (80, 54, 40)); P.rect((-30, 1360, 0, 1700), (60, 40, 30)); P.rect((580, 1360, 610, 1700), (60, 40, 30))
    return P.sprite()

# ================= SHOTS =================
def mk(t0, t1, fn, dissolve=0.0, wipe=False): return dict(t0=t0, t1=t1, fn=fn, dz=dissolve, wipe=wipe)

def build_all():
    S = []
    XR = crossroads_plate(1); md, mg, ga = moon(820, 300, 58, res=1.4)
    MH_FAR = Painter((470, 1020, 650, 1240), res=2); mala_hora(MH_FAR, 560, 1230, 200, "back"); mh_far = MH_FAR.sprite()
    torch_beam = beam_sprite(540, 2100, 560, 1300, 160, 420, TORCH, 0.30, 0.04, res=0.4, blur=40)
    dust = []
    dr = random.Random(5); DG = glow_sprite(0, 0, 9, (170, 160, 200), power=1.3, res=1.5)
    PTS = [(dr.uniform(-300, 1400), dr.uniform(900, 1900), dr.uniform(0.5, 1.5), dr.uniform(0, 6.28)) for _ in range(46)]
    def dustI(lt, op=0.3, wind=26):
        out = []
        for (x, y, s, ph) in PTS:
            xx = -300 + ((x + 300) + lt * wind * s) % 1700; yy = y + 12 * math.sin(lt * 0.8 + ph)
            out.append(Item(DG, pos=(xx, yy), add=True, opacity=op * min(1, s), scale=s, anchor=(xx, yy)))
        return out
    # S0 — cold open: long lateral slide along the dirt road; far ahead a tiny black figure at the crossing; Zia sign in the fg
    ZS = Painter((-200, 900, 200, 2040), res=1.0); zia_sign(ZS, 0, 2000, 2.2); zfg = ZS.sprite()
    def s0(t):
        lt = t
        its = [Item(XR), Item(mg, add=True, opacity=ga), Item(md), Item(mh_far), Item(torch_beam, add=True, opacity=0.6 + 0.08 * math.sin(lt * 7))] + dustI(lt)
        its.append(Item(zfg, pos=(1200 - 900 * lt, 0), par=1.4))
        return its, (380 + 160 * lt, 1180, 1.12)
    S.append(mk(0, 0.85, s0))
    # S0J — JUMP SCARE: her face lunges at the lens full-frame, violet flash, hard shake; captions hidden
    jf = mh_face("scream"); jg = mh_eye_glints()
    JB = Painter((-60, -60, 1140, 1980), res=0.5, ss=1); JB.gfill((6, 2, 12), (2, 0, 4)); JB.glow(540, 1000, 900, (70, 30, 120), 0.9, 1.2); jbg = JB.sprite()
    RIM = glow_sprite(540, 1000, 700, (130, 80, 220), power=1.6)
    SHD = Painter((-60, 300, 1140, 1980), res=0.5, ss=1); SHD.gpoly([(-60, 300), (1140, 300), (1140, 1000), (-60, 1000)], (0, 0, 0, 215), (0, 0, 0, 0))
    SHD.glow(540, 1700, 520, (110, 60, 200), 0.55, 1.3); jshade = SHD.sprite()
    fl = Sprite(np.dstack([np.full((8, 8), FLASH[0], np.uint8), np.full((8, 8), FLASH[1], np.uint8), np.full((8, 8), FLASH[2], np.uint8), np.full((8, 8), 255, np.uint8)]), 8 / W, 0, 0)
    tj1 = T("walking", 1)
    def s0j(t):
        lt = t - 0.85; lunge = ease_out(min(1, lt / 0.16))
        z = 3.2 - 1.75 * lunge + 0.08 * lt
        sh = 26 * math.exp(-lt * 6) * math.sin(lt * 95); sv = 18 * math.exp(-lt * 6) * math.cos(lt * 83)
        its = [Item(jbg), Item(RIM, add=True, opacity=0.55), Item(jf), Item(jshade), Item(jg)]
        fo = 0.75 if lt < 0.07 else max(0, 0.35 - (lt - 0.07) * 1.2)
        if fo > 0: its.append(Item(fl, opacity=fo, par=0.0))
        return its, (540 + sh, 1060 + sv, z)
    S.append(mk(0.85, tj1, s0j))
    # S1 — "walking home alone": the walker's boots on gravel in the torch pool, descansos slip past
    BT = Painter((-460, -120, 1540, 2040), res=1.0); BT.gpoly([(-460, -120), (1540, -120), (1540, 2040), (-460, 2040)], dim(EARTH, 0.6), dim(EARTH_L, 0.8))
    r_ = random.Random(3)
    for _ in range(900): BT.circ(r_.uniform(-460, 1540), r_.uniform(-120, 2040), r_.uniform(2, 7), dim(EARTH, r_.uniform(0.6, 1.2)))
    for x in (-300, 500, 1300): descanso(BT, x, 1000, 1.2, x)
    boots = BT.sprite()
    BOOT = Painter((-200, -420, 200, 30), res=1.2); BOOT.rrect((-190, -110, 190, 20), 36, (30, 24, 22)); BOOT.rect((-90, -420, 70, -90), dim(TAN, 0.5)); BOOT.rect((-96, -150, 76, -100), (44, 36, 32)); boot = BOOT.sprite()
    pool = glow_sprite(540, 1500, 520, TORCH, power=1.5)
    t1a, t1b = T("walking", 1), T("after", 1)
    def s1(t):
        lt = t - t1a; its = [Item(boots, pos=(-260 * lt, 0)), Item(pool, add=True, opacity=0.35)]
        for i, ph in enumerate((0, math.pi)):
            st = (math.sin(lt * 6 + ph) + 1) / 2; its.append(Item(boot, pos=(380 + i * 320 + 60 * st, 1840 - 70 * max(0, math.sin(lt * 6 + ph)))))
        return its, (540, 1100, 1.0)
    S.append(mk(t1a, t1b, s1))
    # S1b — "after midnight": the twin-tower adobe church under a haloed moon, the bell swings once
    VL = village_plate(7, 0.2); vmd, vmg, vga = moon(560, 360, 70, res=1.4)
    BELL = Painter((-30, -10, 30, 50), res=2); BELL.chord((-26, -6, 26, 70), 180, 360, (60, 50, 40)); BELL.rect((-26, 30, 26, 40), (60, 50, 40)); bell = BELL.sprite()
    t1c, t1d = T("after", 1), T("and", 1)
    def s1b(t):
        lt = t - t1c; sw = 22 * math.sin(lt * 5) * math.exp(-lt * 1.2)
        return [Item(VL), Item(vmg, add=True, opacity=vga), Item(vmd), Item(bell, pos=(560 - 190, 1260 - 600), rot=sw, anchor=(370, 660))], (560, 900, 1.1 + 0.05 * lt)
    S.append(mk(t1c, t1d, s1b))
    # S2 — "and a woman in black is standing": wide crossroads, she stands dead still in the middle, back to us; slide stops
    MH_MID = Painter((380, 760, 740, 1240), res=1.6); mala_hora(MH_MID, 560, 1230, 440, "back"); mh_mid = MH_MID.sprite()
    t2a, t2b = T("and", 1), T("at", 1)
    def s2(t):
        lt = t - t2a; p = ease_out(min(1, lt / (t2b - t2a)))
        return [Item(XR), Item(mg, add=True, opacity=ga), Item(md), Item(mh_mid)] + dustI(lt + 3, 0.35), (300 + 260 * p, 1050, 1.25)
    S.append(mk(t2a, t2b, s2))
    # S2b — "at the crossroads...": closer, shawl fringe lifts in the wind, she does not move
    MHW = []
    for i in range(4):
        Pw = Painter((300, 400, 820, 1260), res=1.4); mala_hora(Pw, 560, 1240, 820, "back", wind=math.sin(i * 1.57)); MHW.append(Pw.sprite())
    t2c, t2d = T("at", 1), T("keep", 1)
    def s2b(t):
        lt = t - t2c
        return [Item(XR), Item(MHW[int(lt * 6) % 4])] + dustI(lt + 5, 0.4, 60), (560, 900, 1.5 + 0.08 * lt)
    S.append(mk(t2c, t2d, s2b))
    # S3 — hook card: KEEP WALKING. ; her shadow walks across the card behind the letters, letters flicker as it passes
    f = ImageFont.truetype(FB, 160); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    hk = "KEEP WALKING."; fs = 160
    while d.textlength(hk, font=f) > 980: fs -= 4; f = ImageFont.truetype(FB, fs)
    d.text(((W - d.textlength(hk, font=f)) / 2, 780), hk, font=f, fill=(198, 38, 38, 255))
    hook = Sprite(np.asarray(lay).copy(), 1, 0, 0); hookg = Sprite(np.asarray(lay.filter(ImageFilter.GaussianBlur(26))).copy(), 1, 0, 0)
    BAND = glow_sprite(540, 900, 640, (40, 24, 70), power=1.2)
    SHW = Painter((300, 300, 820, 1700), res=0.6); mala_hora(SHW, 560, 1680, 1300, "sil"); SHW.blur(6); shw = SHW.sprite()
    t3a, t3b = T("keep", 1), T("because", 1) - 0.05
    def s3(t):
        lt = t - t3a; dd = max(0.4, t3b - t3a); op = 1.0 if lt < dd - 0.3 else max(0, (dd - lt) / 0.3); s_ = 1 + 0.035 * lt / dd
        x = -600 + 1700 * lt / max(dd, 1.2); flick = 0.55 if abs(x) < 220 and int(lt * 30) % 3 == 0 else 1.0
        its = [Item(BAND, add=True, opacity=0.6 * op), Item(shw, pos=(x, 0), opacity=0.95 * op),
               Item(hookg, add=True, opacity=0.8 * op * flick, scale=s_, anchor=(540, 860)), Item(hook, opacity=op * flick, scale=s_, anchor=(540, 860))]
        return its, (540, 960, 1.0)
    S.append(mk(t3a, t3b, s3))
    # S4 — "Because she isn't waiting for a ride.": a pickup's headlights sweep past her at the crossing; she doesn't turn
    PK = Painter((-400, 1000, 400, 1300), res=1.2); pickup(PK, 0, 1290, 1.0); pk = PK.sprite()
    hb = beam_sprite(0, 1180, 900, 1220, 60, 600, (255, 236, 200), 0.5, 0.0, res=0.4, blur=40)
    t4a, t4b = T("because", 1), T("shes", 1)
    def s4(t):
        lt = t - t4a; x = -500 + 900 * lt
        return [Item(XR), Item(mg, add=True, opacity=ga), Item(md), Item(mh_mid), Item(hb, pos=(x, 0), add=True, opacity=0.8), Item(pk, pos=(x - 300, 0))], (520 + 60 * lt, 1050, 1.25)
    S.append(mk(t4a, t4b, s4))
    # S5 — "She's waiting to tell you": over her shoulder, the village lights far off
    VLF = village_plate(23, 1.0)
    SHO = Painter((-700, 700, 1100, 3800), res=0.6); mala_hora(SHO, 150, 3780, 3000, "back"); sho = SHO.sprite()
    t5a, t5b = T("shes", 1), T("whos", 1)
    def s5(t):
        lt = t - t5a
        return [Item(VLF, scale=0.7, anchor=(560, 1300)), Item(sho, par=1.3)], (560, 1100, 1.1 + 0.06 * lt)
    S.append(mk(t5a, t5b, s5))
    # S5b — "who's next.": a row of lit adobe windows; one window goes dark
    WR = Painter((-160, -120, 1240, 2040), res=1.0); nm_sky(WR, 29, 80)
    WR.rect((-160, 700, 1240, 1500), ADOBE_D); WR.rect((-160, 1500, 1240, 2040), EARTH_D)
    WIN = [(-60 + i * 260, 900) for i in range(5)]
    for (x, y) in WIN: WR.rect((x, y, x + 150, y + 220), (30, 22, 30)); WR.rect((x - 8, y - 8, x + 158, y), (70, 50, 40))
    hang_ristra(WR, 1150, 720, 9, 1.4); wrow = WR.sprite()
    LITW = Painter((-60, 900, 1090, 1120), res=1.0)
    lit_sprites = []
    for j in range(5):
        Lp = Painter((WIN[j][0], 900, WIN[j][0] + 150, 1120), res=1.0); Lp.rect((WIN[j][0], 900, WIN[j][0] + 150, 1120), (255, 196, 110)); Lp.line([(WIN[j][0] + 75, 900), (WIN[j][0] + 75, 1120)], (90, 60, 40), 6); lit_sprites.append(Lp.sprite())
    wglow = [glow_sprite(x + 75, 1010, 200, (255, 180, 90), power=1.6) for (x, y) in WIN]
    t5c, t5d = T("whos", 1), T("they", 1)
    def s5b(t):
        lt = t - t5c; its = [Item(wrow)]
        for j in range(5):
            o = 1.0 if (j != 2 or lt < 0.35) else 0.0
            its += [Item(wglow[j], add=True, opacity=0.4 * o), Item(lit_sprites[j], opacity=o)]
        return its, (500, 1010, 1.15)
    S.append(mk(t5c, t5d, s5b))
    # S6 — TITLE (dissolve): a votive candle on a descanso gutters and dies; its smoke curls up into the title
    DC = descanso_close_plate(31)
    FLM = Painter((-30, -80, 30, 10), res=3); FLM.poly([(-14, 0), (0, -70), (14, 0)], (255, 200, 110)); FLM.poly([(-7, 0), (0, -40), (7, 0)], (255, 246, 210)); flame = FLM.sprite()
    cglow = glow_sprite(0, 0, 260, VOTIVE, power=1.5)
    PUFF = smoke_puff()
    lab = Image.new("RGBA", (W, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(lab)
    fr = ImageFont.truetype(FR, 30); fb = ImageFont.truetype(FB, 150)
    s_ = "N E W   M E X I C O   ·   L E G E N D"
    d.rectangle([W / 2 - 22, 110, W / 2 + 22, 115], fill=(190, 46, 40, 255))
    d.text(((W - d.textlength(s_, font=fr)) / 2, 135), s_, font=fr, fill=(176, 168, 190, 255))
    nm = "LA MALA HORA"; fsz = 150
    while d.textlength(nm, font=fb) > 980: fsz -= 4; fb = ImageFont.truetype(FB, fsz)
    d.text(((W - d.textlength(nm, font=fb)) / 2, 175), nm, font=fb, fill=(232, 224, 236, 255))
    title = Sprite(np.asarray(lab).copy(), 1, 0, 0); title_b = Sprite(np.asarray(lab.filter(ImageFilter.GaussianBlur(18))).copy(), 1, 0, 0)
    cx_c, cy_c = 540 + 41 * 2.3, 1120 - 70 * 2.3
    t6a, t6b = T("they", 1), T("her", 2)
    def s6(t):
        lt = t - t6a; out_t = 0.9; alive = lt < out_t
        its = [Item(DC)]
        if alive: its += [Item(cglow, pos=(cx_c, cy_c), add=True, opacity=0.6 * flk(lt) * (1 - lt / out_t * 0.5)), Item(flame, pos=(cx_c, cy_c), scale=(0.9 + 0.15 * flk(lt)) * (1 - 0.6 * lt / out_t), anchor=(cx_c, cy_c))]
        for i in range(14):
            q = lt - out_t - i * 0.06
            if q > 0:
                y = cy_c - 80 - q * 520; x = cx_c + 70 * math.sin(q * 3 + i) - (cx_c - 540) * min(1, q * 0.8)
                its.append(Item(PUFF, pos=(x, y), add=True, opacity=max(0, 0.32 - q * 0.14), scale=0.6 + q * 1.2, anchor=(x, y)))
        ta = ease_out(min(1, max(0, (lt - out_t - 0.2) / 1.0)))
        its += [Item(title_b, opacity=ta * (1 - ta) * 1.6, par=0.0), Item(title, opacity=ta, par=0.0)]
        return its, (540, 1000 - 40 * EASE["sine"](min(1, lt / 3)), 1.1 - 0.04 * min(1, lt / 3))
    S.append(mk(t6a, t6b, s6, dissolve=0.27))
    # S7 — "Her story is told in Hispanic communities" (shadow wipe): the village at night, ristras on a portal, warm windows
    VL2 = village_plate(41, 1.0)
    t7a, t7b = T("her", 2), T("across")
    def s7(t):
        lt = t - t7a
        return [Item(VL2), Item(vmg, add=True, opacity=vga), Item(vmd, pos=(260, -40))] + dustI(lt, 0.2), (300 + 140 * lt, 1080, 1.05)
    S.append(mk(t7a, t7b, s7, wipe=True))
    # S7b — "across New Mexico": high desert, Sangre de Cristo range, road winding into the dark, Zia route sign
    DRP = desert_road_plate(43); dmd, dmg, dga = moon(300, 420, 90, res=1.3)
    t7c, t7d = T("across"), T("where", 1)
    def s7b(t):
        lt = t - t7c
        return [Item(DRP), Item(dmg, add=True, opacity=dga), Item(dmd)], (700 - 120 * lt, 1060, 1.08)
    S.append(mk(t7c, t7d, s7b))
    # S8 — "where white crosses called descansos line the back roads": a row of descansos in the torch light, lateral slide
    DRW = descanso_row_plate(47); tp = glow_sprite(0, 0, 360, TORCH, power=1.6)
    t8a, t8b = T("where", 1), T("each")
    def s8(t):
        lt = t - t8a
        return [Item(DRW), Item(tp, pos=(820 - 120 * lt, 1450), add=True, opacity=0.35)], (760 - 110 * lt, 1180, 1.12)
    S.append(mk(t8a, t8b, s8))
    # S8b — "Each one marks a place where someone died.": one weathered descanso, faded flowers trembling in the wind
    t8c, t8d = T("each"), T("according")
    def s8b(t):
        lt = t - t8c
        return [Item(DC), Item(cglow, pos=(cx_c, cy_c), add=True, opacity=0.35 * flk(lt)), Item(flame, pos=(cx_c, cy_c), scale=0.7 + 0.1 * flk(lt), anchor=(cx_c, cy_c))], (560, 900, 1.25 + 0.05 * lt)
    S.append(mk(t8c, t8d, s8b))
    # S9 — "According to the legend, she appears to people": one small traveler on foot under a huge haloed moon
    MP = moon_plain_plate(53); bmd, bmg, bga = moon(540, 780, 230, res=1.2)
    TRV = Painter((440, 1180, 680, 1420), res=2); walker(TRV, 540, 1410, 220, "back"); trv = TRV.sprite()
    t9a, t9b = T("according"), T("traveling")
    def s9(t):
        lt = t - t9a
        return [Item(MP), Item(bmg, add=True, opacity=bga), Item(bmd), Item(trv, pos=(0, -3 * abs(math.sin(lt * 5))))], (540, 1060, 1.2 - 0.05 * lt)
    S.append(mk(t9a, t9b, s9))
    # S9c — "traveling alone at night,": the flashlight finds her shape far down the road, then loses it
    t9c, t9d = T("traveling"), T("right")
    def s9c(t):
        lt = t - t9c; seen = 0.6 < lt < 1.3
        return [Item(XR), Item(torch_beam, pos=(30 * math.sin(lt * 2), 0), add=True, opacity=0.7), Item(mh_far, opacity=1.0 if seen else 0.0)], (560, 1250, 1.7 + 0.08 * lt)
    S.append(mk(t9c, t9d, s9c))
    # S9b — "right where two roads meet.": top-down view of the X, her tiny black figure exactly at the centre
    TD = crossroads_plate(57, top_down=True)
    TOP = Painter((500, 920, 580, 1000), res=3); TOP.circ(540, 960, 34, REB); TOP.arc((506, 926, 574, 994), 200, 340, REB_S, 4); top = TOP.sprite()
    t9e, t9f = T("right"), T("she", 3)
    def s9b(t):
        lt = t - t9e
        return [Item(TD, rot=6 * lt, anchor=(540, 960)), Item(top)], (540, 960, 1.1 + 0.04 * lt)
    S.append(mk(t9e, t9f, s9b))
    # S10 — "She never touches you. She doesn't have to.": the traveler walks past within arm's reach; on "have" her eyes catch light
    WK = Painter((200, 600, 900, 1260), res=1.4); walker(WK, 560, 1240, 600, "front"); wk = WK.sprite()
    MHC = Painter((300, 300, 820, 1260), res=1.4); mala_hora(MHC, 560, 1240, 900, "three"); mhc = MHC.sprite()
    EG = Painter((560, 1060, 640, 1110), res=3)
    for ex in (580, 616): EG.ell((ex - 9, 1076, ex + 9, 1090), MEYE)
    eg = EG.sprite(); egg = glow_sprite(598, 1083, 60, (220, 220, 255), power=1.6)
    t10a, t10b = T("she", 3), T("but")
    th = T("have", 1) - t10a
    def s10(t):
        lt = t - t10a; o = min(1, max(0, (lt - th) / 0.15))
        return [Item(XR, scale=1.6, anchor=(560, 1240)), Item(mhc, pos=(80, 0)), Item(eg, pos=(80, 0), opacity=o), Item(egg, pos=(80, 0), add=True, opacity=0.6 * o),
                Item(wk, pos=(-600 + 330 * lt, 0), par=1.2)], (560 + 30 * lt, 900, 1.35)
    S.append(mk(t10a, t10b, s10))
    # S11 — "But here's the terrifying part.": walker portrait, flashlight under the chin, trembling
    wface, weyes = walker_portrait()
    PB = Painter((-60, -60, 1140, 1980), res=1.0); PB.gfill((6, 6, 12), (14, 12, 24)); PB.glow(540, 1100, 700, (60, 50, 90), 0.9, 1.5); pbg = PB.sprite()
    t11a, t11b = T("but"), T("seeing")
    def s11(t):
        lt = t - t11a; sh = 2 * math.sin(lt * 31)
        return [Item(pbg), Item(wface, pos=(sh, 0)), Item(weyes, pos=(sh, 0), opacity=0 if abs(lt - 1.2) < 0.06 else 1)], (540, 960, 1.0 + 0.05 * lt)
    S.append(mk(t11a, t11b, s11))
    # S12 — "Seeing her doesn't mean you'll die.": extreme close on the walker's eye, her dark shape reflected in it
    EY = Painter((-160, -120, 1240, 2040), res=1.0); EY.gfill(SKIN_D, dim(SKIN_D, 0.7))
    EY.ell((60, 420, 1020, 1080), (236, 228, 216)); EY.circ(540, 750, 270, (64, 42, 26)); EY.circ(540, 750, 140, (6, 4, 4))
    EY.arc((40, 380, 1040, 1100), 195, 345, (40, 26, 20), 40); EY.arc((60, 540, 1020, 1120), 15, 165, dim(SKIN_D, 0.8), 18)
    eye = EY.sprite()
    RF = Painter((490, 660, 590, 840), res=2); mala_hora(RF, 540, 830, 160, "sil"); refl = RF.sprite()
    spec = glow_sprite(600, 680, 40, (255, 255, 255), power=2.5)
    t12a, t12b = T("seeing"), T("it", 1)
    def s12(t):
        lt = t - t12a; sh = 3 * math.sin(lt * 37)
        return [Item(eye), Item(refl, opacity=0.9), Item(spec, add=True, opacity=0.8)], (540 + sh, 980, 1.25 + 0.06 * lt)
    S.append(mk(t12a, t12b, s12))
    # S13 — "It means someone you love will.": family photo frame on an adobe wall, the candle beside it bends and goes out
    WL = interior_plate(False, wall_only=True)
    FR_ = Painter((300, 520, 780, 1120), res=1.2); FR_.rect((300, 520, 780, 1120), (90, 60, 40)); FR_.rect((330, 550, 750, 1090), (60, 70, 96))
    for (fx, fh) in ((450, 380), (630, 420)): FR_.ell((fx - 50, 1090 - fh, fx + 50, 1090 - fh + 110), (30, 30, 44)); FR_.rrect((fx - 80, 1090 - fh + 100, fx + 80, 1090), 30, (30, 30, 44))
    frame_s = FR_.sprite()
    CN = Painter((820, 800, 900, 1120), res=2); CN.rect((830, 900, 890, 1100), (200, 190, 176)); CN.rect((800, 1100, 920, 1120), (90, 60, 40)); candle = CN.sprite()
    t13a, t13b = T("it", 1), T("one", 2)
    def s13(t):
        lt = t - t13a; out_t = 1.4; alive = lt < out_t; bend = 20 * min(1, lt / out_t)
        its = [Item(WL, opacity=0.9 if alive else 0.55), Item(frame_s), Item(candle)]
        if alive: its += [Item(cglow, pos=(860, 880), add=True, opacity=0.6 * flk(lt)), Item(flame, pos=(860, 896), rot=-bend, scale=1.6, anchor=(860, 896))]
        else: its.append(Item(PUFF, pos=(860, 850 - (lt - out_t) * 200), add=True, opacity=max(0, 0.3 - (lt - out_t) * 0.3), scale=0.5, anchor=(860, 1150)))
        return its, (600, 960, 1.15 + 0.04 * lt)
    S.append(mk(t13a, t13b, s13))
    # S14 — "One woman saw her at a crossroads.": a woman in a teal shawl frozen at a crossing; the black figure far across
    WV = Painter((140, 700, 560, 1440), res=1.4); woman_villager(WV, 340, 1420, 700); wv = WV.sprite()
    t14a, t14b = T("one", 2), T("by")
    def s14(t):
        lt = t - t14a; p = ease_out(min(1, lt / 1.4))
        return [Item(XR), Item(mg, add=True, opacity=ga), Item(md), Item(mh_far, pos=(160, 0)), Item(wv, pos=(-120, 260), par=1.15)], (420 + 120 * p, 1150, 1.25)
    S.append(mk(t14a, t14b, s14))
    # S15 — "By morning, she learned" (shadow wipe): blue-dawn adobe kitchen, the woman with both hands at her mouth, trembling
    KI = interior_plate(True)
    WV2 = Painter((240, 500, 840, 1500), res=1.3); woman_villager(WV2, 540, 1480, 940, hands_up=True); wv2 = WV2.sprite()
    t15a, t15b = T("by"), T("her", 5)
    def s15(t):
        lt = t - t15a; sh = 2.5 * math.sin(lt * 33)
        return [Item(KI), Item(wv2, pos=(sh - 180, 120))], (500, 1050, 1.12 + 0.05 * lt)
    S.append(mk(t15a, t15b, s15, wipe=True))
    # S15b — "her husband had died...": his hat and coat on an empty chair, the cup still on the table
    CH = Painter((-160, 800, 1240, 2040), res=1.0)
    CH.rect((320, 1000, 380, 1800), (70, 48, 36)); CH.rect((320, 1360, 720, 1410), (80, 54, 40)); CH.rect((680, 1360, 720, 1800), (70, 48, 36)); CH.rect((320, 1000, 720, 1050), (80, 54, 40))
    CH.poly([(300, 1040), (420, 1030), (460, 1380), (290, 1400)], (54, 44, 40))                                     # coat over the back
    CH.ell((240, 940, 480, 1000), (90, 70, 46)); CH.ell((300, 880, 420, 990), (90, 70, 46))                         # hat
    CH.rect((-160, 1320, 260, 1350), (80, 54, 40)); CH.rrect((120, 1250, 190, 1322), 8, (200, 196, 186)); CH.arc((180, 1266, 214, 1302), 270, 90, (200, 196, 186), 6)
    chair = CH.sprite()
    t15c, t15d = T("her", 5), T("at", 4)
    def s15b(t):
        lt = t - t15c
        return [Item(KI), Item(chair)], (480, 1180, 1.25 + 0.03 * lt)
    S.append(mk(t15c, t15d, s15b))
    # S15c — "at that exact hour.": Spanish-style wall clock stopped at 12:00, pendulum still; snap push
    CK = Painter((-160, -120, 1240, 2040), res=1.0); CK.gfill(dim(ADOBE, 0.42), dim(ADOBE_D, 0.32)); wall_clock(CK, 540, 760, 230); clock = CK.sprite()
    t15e, t15f = T("at", 4), T("they", 2)
    def s15c(t):
        lt = t - t15e; z = 1.0 + 0.45 * ease_out(min(1, lt / 0.25)) + 0.04 * lt
        return [Item(clock)], (540, 900, z)
    S.append(mk(t15e, t15f, s15c))
    # S16 — "They say she doesn't always look human.": her silhouette against the moon stretches unnaturally tall
    BM = Painter(BG, res=1.0); nm_sky(BM, 61, 120); floor(BM, 1500, 62, 14); bottom_dark(BM); bm = BM.sprite()
    TM_d, TM_g, TM_a = moon(540, 760, 260, res=1.2)
    TALL = Painter((340, 300, 740, 1520), res=1.0); mala_hora(TALL, 540, 1500, 1100, "sil"); tall = TALL.sprite()
    t16a, t16b = T("they", 2), T("sometimes")
    def s16(t):
        lt = t - t16a; st = 1 + 0.35 * EASE["sine"](min(1, lt / 2.4))
        return [Item(bm), Item(TM_g, add=True, opacity=TM_a), Item(TM_d), Item(tall, scale=1.0, anchor=(540, 1500)),
                Item(tall, scale=st, anchor=(540, 1500), opacity=0.5)], (540, 1100 - 120 * EASE["sine"](min(1, lt / 2.4)), 1.05)
    S.append(mk(t16a, t16b, s16))
    # S17 — "Sometimes she's just a dark shape rolling across the road.": a black shapeless mass rolls through the torch beam
    BLB = Painter((-200, -200, 200, 200), res=1.0); rr = random.Random(9)
    for _ in range(26): a = rr.uniform(0, 6.28); dd = rr.uniform(0, 90); BLB.circ(math.cos(a) * dd, math.sin(a) * dd, rr.uniform(50, 100), (6, 4, 10))
    BLB.blur(10); blob = BLB.sprite()
    RD = desert_road_plate(67)
    t17a, t17b = T("sometimes"), T("so")
    def s17(t):
        lt = t - t17a; x = 40 + 260 * lt
        return [Item(RD), Item(torch_beam, add=True, opacity=0.7), Item(blob, pos=(x, 1620), rot=-160 * lt, anchor=(x, 1620), scale=1.6)] + dustI(lt + 1, 0.45, 80), (560 + 40 * lt, 1300, 1.2)
    S.append(mk(t17a, t17b, s17))
    # S18 — "So if you're walking home alone tonight,": LOOP of the cold open — same road, the walker from behind, figure ahead
    WB = Painter((360, 1100, 760, 1900), res=1.3); walker(WB, 560, 1880, 760, "back"); wb = WB.sprite()
    t18a, t18b = T("so"), T("dont", 1)
    def s18(t):
        lt = t - t18a
        return [Item(XR), Item(mg, add=True, opacity=ga), Item(md), Item(mh_far), Item(torch_beam, add=True, opacity=0.6), Item(wb, pos=(0, -4 * abs(math.sin(lt * 5))), par=1.15)] + dustI(lt), (380 + 160 * lt, 1180, 1.12)
    S.append(mk(t18a, t18b, s18))
    # S19b — "don't stop, and don't look back.": he walks past her at the crossing without a pause; she is behind now
    t19a, t19b = T("dont", 1), T("because", 2)
    def s19b(t):
        lt = t - t19a; x = -300 + 420 * lt
        return [Item(XR, scale=1.6, anchor=(560, 1240)), Item(mhc, pos=(-60, 0)), Item(wk, pos=(x, 0), par=1.15)], (420 + 90 * lt, 900, 1.35)
    S.append(mk(t19a, t19b, s19b))
    # S20 — "Because she isn't there for you.": her back at the empty crossroads, the walker's light shrinking in the distance
    tl = glow_sprite(0, 0, 50, TORCH, power=1.6)
    t20a, t20b = T("because", 2), T("shes", 3)
    def s20(t):
        lt = t - t20a
        return [Item(XR), Item(mg, add=True, opacity=ga), Item(md), Item(MHW[0], pos=(0, 120), scale=0.8, anchor=(560, 1240)), Item(tl, pos=(560, 1110), add=True, opacity=max(0.15, 0.8 - 0.25 * lt), scale=max(0.3, 1 - 0.3 * lt), anchor=(560, 1110))], (560, 1000, 1.45 - 0.08 * lt)
    S.append(mk(t20a, t20b, s20))
    # S21 — "She's there to tell you": her back, close; the shawl stirs; her head begins to turn
    MHT = []
    for v in ("back", "three"):
        Pv = Painter((200, 200, 920, 1300), res=1.3); mala_hora(Pv, 560, 2200, 2000, v, wind=0.4); MHT.append(Pv.sprite())
    t21a, t21b = T("shes", 3), T("whos", 2)
    def s21(t):
        lt = t - t21a; d_ = max(0.5, t21b - t21a); o = ease_io(min(1, max(0, (lt - d_ * 0.5) / (d_ * 0.5))))
        return [Item(bm), Item(TM_g, add=True, opacity=TM_a * 0.6), Item(MHT[0], opacity=1 - o), Item(MHT[1], opacity=o)], (560, 760, 1.05 + 0.04 * lt)
    S.append(mk(t21a, t21b, s21))
    # S21b — REVEAL "who's not coming home.": the slow head turn completes — her face, milky eyes, thin teeth, violet rim; hold
    rf = mh_face("scream"); rg = mh_eye_glints(); rf_still = mh_face("still")
    PB2 = Painter((-60, -60, 1140, 1980), res=1.0); PB2.gfill((4, 3, 8), (12, 10, 20)); PB2.glow(540, 900, 700, (70, 50, 120), 0.9, 1.4); pbg2 = PB2.sprite()
    VRIM = glow_sprite(540, 880, 620, (140, 100, 240), power=1.8)
    t21c = T("whos", 2); thome = T("home", 2) if sum(1 for w in words if norm(w["w"]) == "home") >= 2 else T("home", 1)
    def s21b(t):
        lt = t - t21c; turn = ease_io(min(1, lt / 0.9)); mouth = lt > (thome - t21c) + 0.1
        return [Item(pbg2), Item(VRIM, add=True, opacity=0.5 * turn), Item(rf if mouth else rf_still, pos=(220 * (1 - turn), 0), opacity=turn),
                Item(rg, pos=(220 * (1 - turn), 0), opacity=turn * (0 if abs(lt - 1.6) < 0.06 else 1))], (540, 1000, 1.05 + 0.22 * EASE["sine"](min(1, lt / 2.4)))
    S.append(mk(t21c, END, s21b))
    # ---- extra cuts on long shots (none planned: the scene plan already splits at the 05-TT-KIT-SCENES anchors) ----
    return S

# ================= captions =================
CHUNKS = ["In New Mexico,", "if you're walking home", "alone after midnight,", "and a woman", "in black is standing", "at the crossroads...", "#keep walking.",
          "Because she isn't waiting", "for a ride.", "She's waiting to tell", "you who's next.", "They call her", "La Mala Hora.", "The evil hour.",
          "Her story is told", "in Hispanic communities across", "New Mexico,", "where white crosses", "called descansos line", "the back roads.", "Each one marks",
          "a place where someone", "died.", "According to the legend,", "she appears to people", "traveling alone at night,", "right where two roads", "meet.",
          "She never touches you.", "She doesn't have to.", "But here's the terrifying", "part.", "Seeing her doesn't mean", "you'll die.", "It means someone",
          "you love will.", "One woman saw", "her at a crossroads.", "By morning,", "she learned her husband", "had died...", "at that exact hour.",
          "They say she doesn't", "always look human.", "Sometimes she's just", "a dark shape rolling", "across the road.", "So if you're walking", "home alone tonight,",
          "don't stop,", "and don't look back.", "Because she isn't there", "for you.", "She's there to tell", "you who's not coming", "home."]
RED = {"MEXICO,", "ALONE", "MIDNIGHT,", "BLACK", "CROSSROADS...", "NEXT.", "MALA", "HORA.", "EVIL", "HISPANIC", "DESCANSOS", "DIED.", "LEGEND,", "MEET.",
       "TOUCHES", "TERRIFYING", "DIE.", "LOVE", "CROSSROADS.", "HUSBAND", "EXACT", "HOUR.", "HUMAN.", "SHAPE", "STOP,", "BACK.", "HOME."}
def build_chunks():
    out = []; k = 0
    for ci, c in enumerate(CHUNKS):
        hidden = c.startswith("#"); ws = []
        for tok in c.lstrip("#").split():
            m = words[k]; k += 1
            txt = tok.upper()
            red = txt in RED and not (txt == "HOME." and ci != len(CHUNKS) - 1) and not (txt == "ALONE" and "WALKING" in c.upper() and ci > 40) and not (txt == "MEXICO," and ci > 2)
            ws.append(dict(txt=txt, s=m["s"], e=m["e"], red=red))
        out.append(dict(words=ws, hidden=hidden))
    assert k == len(words), (k, len(words))
    return out

def shadow_wipe_mask(a):
    """dark shawl edge sweeping L->R: returns (mask_new [H,W,1], dark band [H,W,1]) for progress a in 0..1."""
    xs = np.arange(W, dtype=np.float32)[None, :]; ys = np.arange(H, dtype=np.float32)[:, None]
    edge = -300 + (W + 600) * a + 120 * np.sin(ys / 260.0 + a * 3)          # wavy fabric edge
    new = np.clip((edge - xs) / 60.0, 0, 1)
    band = np.exp(-((xs - edge) / 160.0) ** 2) * 0.92
    return new[..., None], band[..., None]

def main():
    print("building shots...", flush=True)
    SH = build_all(); chunks = build_chunks(); cap = Captioner(FB, size=84)
    for a, b in zip(SH[:-1], SH[1:]): assert b["t1"] > b["t0"] and b["t0"] >= a["t1"] - 1e-6 and b["t0"] - a["t1"] < 0.1, (a["fn"].__name__, a["t1"], b["fn"].__name__, b["t0"])
    print("shots", len(SH), [(s_["fn"].__name__, round(s_["t1"] - s_["t0"], 2)) for s_ in SH], flush=True)
    def shot_at(t):
        for i, s_ in enumerate(SH):
            if t < s_["t1"]: return i
        return len(SH) - 1
    def rend(i, t): return render_frame(SH[i]["fn"], t)
    WP = 0.32
    def frame(n):
        t = n / FPS; i = shot_at(t); img = rend(i, t)
        dz = SH[i]["dz"]
        if dz and t - SH[i]["t0"] < dz and i > 0:
            a = (t - SH[i]["t0"]) / dz; a = a * a * (3 - 2 * a); img = rend(i - 1, t) * (1 - a) + img * a
        if SH[i]["wipe"] and i > 0 and t - SH[i]["t0"] < WP:                         # SHADOW WIPE: her shawl sweeps across the frame
            a = (t - SH[i]["t0"]) / WP; m, band = shadow_wipe_mask(a)
            img = (rend(i - 1, t) * (1 - m) + img * m) * (1 - band)
        hook = SH[i]["fn"].__name__ in ("s3", "s0j")
        if SH[i]["fn"].__name__ != "s3":
            img = vignette(img, 0.62)
            lum = img.mean(axis=2, keepdims=True); img = img * 0.72 + lum * 0.28                                   # near-monochrome
            img = img * np.array([0.95, 0.94, 1.08], np.float32) + np.array([2, 0, 6], np.float32)                 # EP06 grade: cold indigo/violet
        img = grain(img, 0, 2.0)
        act = None
        for c in chunks:
            if c["words"][0]["s"] <= t + 0.03: act = c
        if act and not act["hidden"] and not hook and t < VOICE_END + 0.3:
            img = cap.apply(img, act["words"], sum(1 for w in act["words"] if w["s"] <= t + 0.03))
        return np.clip(img, 0, 255).astype(np.uint8)
    if len(sys.argv) > 2:
        ts = [float(x) for x in sys.argv[2].split(",")]; ims = [Image.fromarray(frame(int(t * FPS))).resize((270, 480), Image.LANCZOS) for t in ts]
        cols = min(8, len(ims)); sheet = Image.new("RGB", (270 * cols, 480 * ((len(ims) + cols - 1) // cols)))
        for k, im in enumerate(ims): sheet.paste(im, ((k % cols) * 270, (k // cols) * 480))
        out = os.path.join(EP, sys.argv[3] if len(sys.argv) > 3 else "stills.jpg"); sheet.save(out, quality=90); print("stills", out); return
    out = os.path.join(EP, "ep06_noaudio.mp4")
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    nf = int(math.ceil(END * FPS))
    for n in range(nf):
        pr.stdin.write(frame(n).tobytes())
        if n % 150 == 0: print("frame", n, "/", nf, flush=True)
    pr.stdin.close(); pr.wait(); print("wrote", out, "%.2f s" % (nf / FPS))

if __name__ == "__main__":
    main()
