"""animal-toon-eyes production kit — helpers for writing an EDL the way recipe.md describes (keyframed cut-out blocks,
toon eyes riding on them, jaw parts, props, sample devices). A project script imports it, registers its own pictures'
eye / jaw / shadow positions with setup(), lists its SHOTS with ABSOLUTE script times, and calls write_edl().

    import sys; sys.path.insert(0, '<repo>/styles/animal-toon-eyes'); import kit
    kit.setup(eye={...}, jaw={...}, shadow={...})
    SHOTS = [(T, 'plate/P_b', kit.HOLD(0.5, 0.5, 1.1), 'cut', kit.block('P0', T, ...) + [kit.png(...)]), ...]
    kit.write_edl(SHOTS, END, 'edl.json', 'out/video.mp4', sfx=[(t, 'sfx_pop', -14), ...], kicks=[2.6])

Times: everything in seconds of the narration (words.json); write_edl turns them into shot times (layers.shift_times).
Positions: picture fractions; full-frame cut-outs sit at x = y = 0.5, w = 1. Read positions with grid_crop(), never guess.
"""
import json, os, random, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
STYLE = os.path.dirname(os.path.abspath(__file__))
if REPO not in sys.path: sys.path.insert(0, REPO)
from vidclone.layers import shift_times   # noqa: E402

EYE, JAW, SHADOW = {}, {}, {}
LIDS = {}            # picture-name prefix -> lid colour (dark fur: sampled lids read as black slits)
EYE_GAIN = 1.3       # sample eyes are big: ~0.09 of the frame on a seated panda
NO_GAIN = set()      # close-ups whose eye size was set directly

def setup(eye=None, jaw=None, shadow=None, lids=None, no_gain=()):
    """Register the project's pictures. eye: {name: dict(l=(x, y), r=(x, y), size=.., single='l'|'r')} in sprite fractions;
    jaw: {name: dict(ellipse=[x, y, rx, ry], erot=.., pivot=[x, y], hole='#..')}; shadow: {name: (x, y, width)}."""
    EYE.update(eye or {}); JAW.update(jaw or {}); SHADOW.update(shadow or {}); LIDS.update(lids or {}); NO_GAIN.update(no_gain)

FT = lambda a, b, ease='inout': {'from': list(a), 'to': list(b), 'ease': ease}
HOLD = lambda x=0.5, y=0.5, z=1.05: FT((x, y, z), (x, y, z + 0.06))
POP = {'in': 'pop'}
NONE = {'in': 'none'}
LAND = lambda t, s=0.06: [{'t': t, 'squash': -s, 'dur': 0.07}, {'t': t + 0.07, 'squash': s, 'dur': 0.18}]   # landing squash
CHEW = lambda t0, t1, hz=3.2, dy=0.016, rot=0.0: dict(t0=t0, t1=t1, hz=hz, dy=dy, rot=rot)                  # jaw chew cycle

def icon(name, t0, t1, x, y, w, **kw): return dict(type='icon', name=name, t0=t0, t1=t1, x=x, y=y, w=w, **kw)
def png(src, t0, t1, x, y, w, **kw): return dict(type='png', src=f'props/{src}.png', t0=t0, t1=t1, x=x, y=y, w=w, **kw)
def text(s, t0, t1, x, y, size, **kw): return dict(type='text', text=s, t0=t0, t1=t1, x=x, y=y, size=size, **kw)

def eyes(img, keys, jitter=True, parent=None, mul=1.0):
    """Toon eyes for a registered picture; keys = [(t, {look, brow, open, low, mood, pupil, scale}), ...]."""
    e = EYE.get(img)
    if not e: return None
    ks = [dict(t=t, **k) for t, k in keys]
    if jitter:  # small eye darts between authored keys, like the samples
        rnd = random.Random(img + str(keys[0][0])); extra = []
        for a, b in zip(ks, ks[1:] + [dict(t=ks[-1]['t'] + 3)]):
            t = a['t'] + 0.45
            while t < b['t'] - 0.2:
                base = a.get('look', [0, 0])
                extra.append({'t': round(t, 2), 'look': [max(-1, min(1, base[0] + rnd.uniform(-0.45, 0.45))),
                                                         max(-1, min(1, base[1] + rnd.uniform(-0.3, 0.3)))]})
                t += rnd.uniform(0.4, 0.6)
        ks = sorted(ks + extra, key=lambda k: k['t'])
    if img not in NO_GAIN: mul *= EYE_GAIN
    E = {'type': 'eyes', 'size': round(e['size'] * mul, 4), 'keys': ks, 'blink': True, 'brow_w': 0.22}
    lid = next((c for p, c in LIDS.items() if img.startswith(p)), None)
    if lid: E['lid'] = lid
    for s in ('l', 'r'):
        if s in e: E[s] = list(e[s])
    if 'single' in e: E['single'] = e['single']
    if parent: E['parent'] = parent
    return E

def block(img, t0, x=0.5, y=0.5, w=1.0, rot=0.0, keys=(), pose=(), pivot=(0.5, 1.0), eye_keys=None, jitter=True,
          breathe=0.008, chew=None, jaw_keys=(), src=None, bid=None, **extra):
    """A pose picture / character / prop as a keyframed cut-out block, with its jaw part, contact shadow and eyes on it."""
    bid = bid or img
    B = dict(type='cutout', id=bid, src=src or f'cut/{img}.png', x=x, y=y, w=w, rot=rot, t0=t0, keys=list(keys), pose=list(pose),
             pivot=list(pivot), breathe=breathe, breathe_hz=0.9, **NONE, **extra)
    if img in SHADOW:
        sx, sy, sw = SHADOW[img]; B['shadow'] = dict(x=sx, y=sy, w=sw, h=sw * 0.14, alpha=0.4)
    if img in JAW and (chew or jaw_keys):
        P = dict(JAW[img]); P['keys'] = list(jaw_keys)
        if chew: P['chew'] = chew
        B['parts'] = [P]
    out = [B]
    if eye_keys: out.append(eyes(img, eye_keys, jitter=jitter, parent=bid))
    return [L for L in out if L]

def bites(t0, t1, food, rest, bite, mouth, period=0.55, bits='leaf_bits', bits_w=0.085):
    """Food held to the mouth on every bite: food = (prop, w), rest / bite = (x, y, rot); chewed bits pop at mouth (x, y)."""
    keys, out, t = [], [], t0
    while t + period <= t1 + 1e-6:
        keys += [{'t': t + period * 0.35, 'x': bite[0], 'y': bite[1], 'rot': bite[2], 'ease': 'out'},
                 {'t': t + period, 'x': rest[0], 'y': rest[1], 'rot': rest[2], 'ease': 'inout'}]
        if bits:
            out.append(png(bits, t + period * 0.35, t + period * 0.95, mouth[0], mouth[1], bits_w, **POP, out='pop', out_dur=0.12,
                           rot=random.Random(t).uniform(-20, 20)))
        t += period
    return [png(food[0], t0, t1, rest[0], rest[1], food[1], rot=rest[2], keys=keys, **NONE)] + out

def write_edl(SHOTS, end, path, out_mp4, sfx=(), kicks=(), cam_gain=0.45, dissolve=0.2, creep=0.02,
              grade=None, music='audio/music.mp3', voice='voice/voice.wav', words='words.json'):
    """(T, background, camera, 'cut'|'dis', layers) with absolute times -> edl.json. Camera travel is scaled by cam_gain
    (the samples keep the camera calm while pictures change)."""
    trans = lambda tr: ('cut', 0.0) if tr == 'cut' else ('dissolve', dissolve)
    starts = [T - trans(tr)[1] / 2 for T, _, _, tr, _ in SHOTS]
    shots = []
    for i, (T, src, cam, tr, lay) in enumerate(SHOTS):
        kind, d = trans(tr)
        dur = (starts[i + 1] - starts[i] + trans(SHOTS[i + 1][3])[1]) if i + 1 < len(SHOTS) else end - starts[i]
        cam = dict(cam)
        a, b = cam['from'], cam['to']; cam['to'] = [a[j] + (b[j] - a[j]) * cam_gain for j in range(3)]
        s = {'src': f'{src}.png', 'dur': round(dur, 3), 'ease': cam.get('ease', 'inout'), **cam}
        if lay: s['layers'] = shift_times(lay, starts[i])
        if i: s['trans'] = {'kind': kind, 'dur': d} if kind == 'dissolve' else {'kind': 'cut'}
        shots.append(s)
    edl = {'out': out_mp4, 'w': 1080, 'h': 1920, 'fps': 30, 'creep': creep,
           'kicks': [{'t': t, 'amp': 0.014, 'frames': 7} for t in kicks], 'shots': shots,
           'grade': grade or {'saturation': 1.0, 'contrast': 1.02, 'temperature': 7000},
           'captions': {'words': words, 'style': STYLE, 'offset': 0.0},
           'audio': {'voice': voice, 'voice_offset': 0.0, 'voice_lufs': -16, 'music': music, 'bed_db': -14, 'duck_db': 0,
                     'music_fade_out': 1.0, 'sfx': [{'src': f'audio/{f}.mp3', 't': t, 'db': db} for t, f, db in sfx],
                     'lufs': -14, 'true_peak': -1.0, 'mono': False}}
    json.dump(edl, open(path, 'w'), indent=1)
    L = [L for s in shots for L in s.get('layers', [])]
    print(len(shots), 'shots;', len(L), 'layers;', sum(x['type'] == 'cutout' for x in L), 'blocks;',
          sum(x['type'] == 'eyes' for x in L), 'eye sets;', sum(bool(x.get('parts')) for x in L), 'jaw parts')
    return edl

def grid_crop(picture, out, cx, cy, half=0.12, step=0.01):
    """Crop around (cx, cy) with a labelled grid in PICTURE fractions — read eye centres, jaw ellipses, prop anchors off it."""
    from PIL import Image, ImageDraw, ImageFont
    im = Image.open(picture).convert('RGB'); w, h = im.size; f = ImageFont.load_default()
    x0, x1 = cx - half, cx + half; y0, y1 = cy - half * w / h, cy + half * w / h
    cr = im.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))).resize((640, 640)); d = ImageDraw.Draw(cr)
    for axis, (a0, a1) in ((0, (x0, x1)), (1, (y0, y1))):
        v = round(a0 / step) * step
        while v <= a1:
            p = (v - a0) / (a1 - a0) * 640; major = round(v / step) % 5 == 0
            col = (255, 0, 0) if major else ((255, 200, 0) if axis == 0 else (0, 200, 255))
            d.line([(p, 0), (p, 640)] if axis == 0 else [(0, p), (640, p)], fill=col, width=1)
            if major: d.text((p + 2, 2) if axis == 0 else (2, p + 2), f'{v:.2f}', fill=(255, 0, 0), font=f)
            v += step
    cr.save(out, quality=85)
    return out
