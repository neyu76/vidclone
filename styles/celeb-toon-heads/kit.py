"""celeb-toon-heads production kit — helpers for EDLs in this style (see recipe.md).

Builds on the animal-toon-eyes kit (cut-out blocks, keyframes, props, split_long, grid_crop) and adds what this channel
format needs on top: the countdown badge (screen overlay, 10 -> 1 on fact boundaries), the red edge pulse for violent /
shock words, an optional own-handle watermark, pose cycles for walking blocks and the paper-flip turn-around.

    import sys; sys.path.insert(0, '<repo>/styles/celeb-toon-heads'); import kit
    kit.setup(shadow={'zayn_walk1': (0.5, 0.93, 0.35)})
    SHOTS = [(T, 'plate/street', kit.HOLD(), 'cut', kit.walk('zayn_walk', T, T + 2.0, frm=-0.2, to=0.55)), ...]
    over = kit.countdown(fact_starts=[3.6, 9.0, ...], end=END, out_dir='art/ui') + kit.red_pulse([33.8], 'art/ui')
    kit.write_edl(SHOTS, END, 'edl.json', 'out/video.mp4', overlays=over, sfx=[...])

Times are narration seconds (words.json), positions picture fractions — same conventions as the animal kit.
"""
import importlib.util, json, os

STYLE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(STYLE, '..', '..'))
_spec = importlib.util.spec_from_file_location('ate_kit', os.path.join(REPO, 'styles', 'animal-toon-eyes', 'kit.py'))
base = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(base)

# re-export the generic block helpers
FT, HOLD, POP, NONE, LAND = base.FT, base.HOLD, base.POP, base.NONE, base.LAND
icon, png, text, block, split_long, grid_crop = base.icon, base.png, base.text, base.block, base.split_long, base.grid_crop
setup = base.setup
base.IDLE.update(breathe=0.006, sway=0.0)   # people stand still in the samples; only a faint breathe
CFG = json.load(open(os.path.join(STYLE, 'style.json')))

def _font(px, name=None):
    from PIL import ImageFont
    return ImageFont.truetype(os.path.join(REPO, 'fonts', name or CFG['countdown'].get('font', 'Rubik-Black.ttf')), px)

def badge_png(n, out, px=256, style=None):
    """Countdown badge as RGBA PNG: white disc with a soft grey bevel and a heavy black number (S01-S03),
    or style 'text': white 'n.' with a thick black outline (S04)."""
    from PIL import Image, ImageDraw, ImageFilter
    c = CFG['countdown']; style = style or c.get('style', 'badge')
    im = Image.new('RGBA', (px, px), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if style == 'badge':
        r = px * 0.46; cx = cy = px / 2
        sh = Image.new('RGBA', (px, px), (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse([cx - r, cy - r + px * 0.02, cx + r, cy + r + px * 0.02], fill=(0, 0, 0, 90))
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(px * 0.02))); d = ImageDraw.Draw(im)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(205, 205, 205, 255))                  # bevel rim
        r2 = r * 0.93; d.ellipse([cx - r2, cy - r2 - px * 0.01, cx + r2, cy + r2 - px * 0.01], fill=(244, 244, 244, 255))
        f = _font(int(px * (0.5 if n < 10 else 0.42)))
        d.text((cx, cy), str(n), font=f, fill=c.get('number', '#111111'), anchor='mm')
    else:
        f = _font(int(px * 0.55), 'TitanOne-Regular.ttf')
        d.text((px / 2, px / 2), f'{n}.', font=f, fill='#ffffff', anchor='mm', stroke_width=int(px * 0.05), stroke_fill='#000000')
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True); im.save(out)
    return out

def countdown(fact_starts, end, out_dir, start=None, frm=None, style=None):
    """Screen overlays for the badge. fact_starts = narration times where each fact begins ('First off', 'Next', 'Even
    weirder', ...), or split points inside long facts. The badge shows frm (10) from `start` (after the title line) and steps
    down at each start; the last number holds to the end. Fewer facts than numbers: the remaining numbers are spread over
    the longest facts so the count still reaches 1 (the samples do this — 7-9 told facts, badge 10 -> 1)."""
    c = CFG['countdown']; frm = frm or c['from']; start = c['start_s'] if start is None else start
    ts = sorted(t for t in fact_starts if t > start)
    while len(ts) < frm - 1:                       # split the longest gap until there are frm - 1 steps
        pts = [start] + ts + [end]
        i = max(range(len(pts) - 1), key=lambda k: pts[k + 1] - pts[k])
        ts = sorted(ts + [round((pts[i] + pts[i + 1]) / 2, 2)])
    ts = ts[:frm - 1]
    times = [start] + ts + [end]
    out = []
    for k in range(frm):
        n = frm - k; src = os.path.join(out_dir, f'badge_{n}.png')
        badge_png(n, src, style=style)
        out.append({'src': src, 't0': times[k], 't1': times[k + 1], 'x': c['x'], 'y': c['y'], 'w': c['w']})
    return out

def red_pulse(times, out_dir, dur=0.5, color=(220, 20, 40)):
    """Red edge vignette that flashes on and fades (gunshot, fight, scream). Returns overlays (5 alpha steps)."""
    from PIL import Image
    import numpy as np
    W, H = 540, 960
    y, x = np.mgrid[0:H, 0:W]; dx = np.minimum(x, W - 1 - x) / W; dy = np.minimum(y, H - 1 - y) / H
    edge = np.clip(1 - np.minimum(dx * 6.5, dy * 9), 0, 1) ** 1.6
    steps = [1.0, 0.8, 0.55, 0.3, 0.12]; out = []
    for k, a in enumerate(steps):
        rgba = np.zeros((H, W, 4), np.uint8); rgba[..., :3] = color; rgba[..., 3] = (edge * 200 * a).astype(np.uint8)
        src = os.path.join(out_dir, f'redpulse_{k}.png'); os.makedirs(out_dir, exist_ok=True)
        Image.fromarray(rgba).save(src)
        for t in times:
            out.append({'src': src, 't0': round(t + k * dur / len(steps), 3), 't1': round(t + (k + 1) * dur / len(steps), 3),
                        'x': 0.5, 'y': 0.5, 'w': 1.0})
    return out

def watermark(handle, end, out_dir):
    """The user's OWN handle, small, half transparent, bottom centre (never the sample channel's)."""
    from PIL import Image, ImageDraw
    if not handle: return []
    f = _font(44, 'Inter-ExtraBold.ttf'); w = int(f.getlength(handle)) + 20
    im = Image.new('RGBA', (w, 64), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((w / 2, 32), handle, font=f, anchor='mm', fill=(255, 255, 255, int(255 * CFG['watermark']['alpha'])),
                            stroke_width=2, stroke_fill=(0, 0, 0, 90))
    src = os.path.join(out_dir, 'watermark.png'); os.makedirs(out_dir, exist_ok=True); im.save(src)
    return [{'src': src, 't0': 0, 't1': end, 'x': 0.5, 'y': CFG['watermark']['y'], 'w': w / 1080}]

def walk(prefix, t0, t1, frm, to, y=0.5, w=1.0, n_poses=2, hz=5.0, bid=None, **kw):
    """A person walking across: the block slides from x=frm to x=to while pose pictures cut/<prefix>1..n swap at hz
    (2-4 walk drawings, all cut out at the same scale), with a small step bob. Returns cutout layers (one per pose,
    alpha-switched so only one shows at a time)."""
    out, period = [], 1.0 / hz
    for p in range(n_poses):
        keys, t, k = [], t0, 0
        while t < t1:
            on = (k % n_poses) == p
            x = frm + (to - frm) * (t - t0) / max(1e-6, t1 - t0)
            x2 = frm + (to - frm) * (min(t1, t + period) - 0.01 - t0) / max(1e-6, t1 - t0)
            a = 1.0 if on else 0.0; yy = y - (0.004 if k % 2 else 0)
            keys.append({'t': round(t, 3), 'x': round(x, 4), 'y': yy, 'alpha': a, 'ease': 'linear'})          # hard swap:
            keys.append({'t': round(min(t1, t + period) - 0.01, 3), 'x': round(x2, 4), 'y': yy, 'alpha': a, 'ease': 'linear'})
            t += period; k += 1
        keys.append({'t': t1, 'x': to, 'y': y, 'alpha': 1.0 if p == 0 else 0.0, 'ease': 'linear'})
        out += block(f'{prefix}{p + 1}', t0, x=frm, y=y, w=w, keys=keys, bid=f'{bid or prefix}_{p}', **kw)
    return out

def turn(img_a, img_b, t, x=0.5, y=0.5, w=1.0, dur=0.24, bid='turn'):
    """Turn-around (S04 0.8 s): pose A shrinks a little into the swap, pose B (other side / front) pops back to size with
    an overshoot. layers.py scales blocks uniformly, so this reads as a quick 'pop turn', not a true paper flip."""
    h = dur / 2
    a = block(img_a, t - 1.0, x=x, y=y, w=w, bid=bid + '_a', t1=t,
              keys=[{'t': t - h, 'w': w, 'ease': 'in'}, {'t': t, 'w': w * 0.88, 'ease': 'in'}])
    b = block(img_b, t, x=x, y=y, w=w * 0.88, bid=bid + '_b', keys=[{'t': t + h, 'w': w, 'ease': 'back'}])
    return a + b

def write_edl(SHOTS, end, path, out_mp4, overlays=(), **kw):
    """animal kit write_edl + screen overlays (badge, red pulse, watermark) and this style's grade / bed defaults."""
    kw.setdefault('grade', CFG['grade']); kw.setdefault('bed_db', -7); kw.setdefault('cam_gain', 1.0)
    kw.setdefault('dissolve', CFG['edit']['dissolve_dur']); kw.setdefault('creep', 0.0)
    edl = base.write_edl(SHOTS, end, path, out_mp4, **kw)
    edl['captions']['style'] = STYLE
    edl['overlays'] = list(overlays)
    json.dump(edl, open(path, 'w'), indent=1)
    return edl
