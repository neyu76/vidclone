"""Identify a sample's caption font and size, calibrated for libass (the renderer captions are burned with).

Why: profile.json only knows the caption height, and captions.write guessed the size with a fixed ratio. In a 2026-11-05
project that guess (and an eyeballed font) made captions ~40 % too wide; the real font was found by rendering candidates
over the sample frame. ASS font size is NOT CSS px (libass sizes by the font's line height), so the size is fitted by
rendering through libass itself.

  vidclone capfont <video> --t 0.5 [--text "could the dallas cowboys"] [--fill '#f5f500'] [--fonts DIR ...] [--style DIR]

Picks a frame with one caption line, finds the caption by its fill colour, then for every candidate TTF/OTF
(repo fonts/, ~/.fonts, --fonts dirs): fits the size so the rendered fill width equals the sample's, scores glyph-shape
overlap (IoU) and x-height, then fits MarginV so the baseline lands on the sample's. With --style the winner is written
to style.json "captions" (font, size, margin_v, outline_px, ref_h, fill, bold 0), which captions.write uses as is.
Only fonts installed/readable as TTF/OTF can be tested — libass silently falls back for missing ones, which is detected
and skipped.
"""
import os, re, json, glob, subprocess, tempfile, numpy as np, cv2
from .captions import FONTS

def _frame(video, t, out):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', video, '-frames:v', '1', out], check=True)
    return cv2.imread(out)

def _hex2bgr(h):
    h = h.lstrip('#'); return np.array([int(h[4:6], 16), int(h[2:4], 16), int(h[0:2], 16)], float)

def _auto_fill(img):
    H = img.shape[0]; band = img[int(H * 0.45):int(H * 0.9)]
    hsv = cv2.cvtColor(band, cv2.COLOR_BGR2HSV).reshape(-1, 3); px = band.reshape(-1, 3)
    sat = px[(hsv[:, 1] > 140) & (hsv[:, 2] > 190)]
    if len(sat) > 400:
        hue = hsv[(hsv[:, 1] > 140) & (hsv[:, 2] > 190), 0]; mode = np.bincount(hue // 6).argmax()
        c = np.median(sat[(hue // 6) == mode], 0)
    else:
        c = np.array([255, 255, 255], float)
    return '#%02x%02x%02x' % (int(c[2]), int(c[1]), int(c[0]))

def _mask(img, fill, tol=70):
    return (np.abs(img.astype(float) - _hex2bgr(fill)).max(2) < tol)

def _line(mask, H):
    """rows of the densest text line in the lower part of the frame -> (y0, y1)."""
    rows = mask.sum(1).astype(float); rows[:int(H * 0.4)] = 0
    if rows.max() < 10: return None
    on = rows > rows.max() * 0.08
    best, cur, s = None, 0, 0
    for y in range(len(on) + 1):
        if y < len(on) and on[y]:
            if cur == 0: s = y
            cur += 1
        elif cur:
            tot = rows[s:y].sum()
            if best is None or tot > best[2]: best = (s, y, tot)
            cur = 0
    return best[0], best[1]

def _measure(mask):
    ys, xs = np.nonzero(mask)
    if len(xs) < 30: return None
    rows = mask.sum(1); d = np.nonzero(rows > rows.max() * 0.35)[0]
    return dict(x0=int(xs.min()), x1=int(xs.max()), w=int(xs.max() - xs.min() + 1), top=int(ys.min()), bot=int(ys.max()),
                core_top=int(d.min()), base=int(d.max()), core=int(d.max() - d.min() + 1))

def _family(path):
    try:
        f = subprocess.run(['fc-scan', '--format', '%{family[0]}', path], capture_output=True, text=True).stdout.strip()
        if f: return f
    except FileNotFoundError: pass
    return os.path.splitext(os.path.basename(path))[0]

def _render(text, family, size, fontsdir, W, H, fill, margin_v, tmp):
    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: C,{family},{size},&H00{fill[5:7]}{fill[3:5]}{fill[1:3]},&H00000000,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,2,20,20,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:05.00,C,,0,0,0,,{text}
"""
    a, o = os.path.join(tmp, 'c.ass'), os.path.join(tmp, 'c.png')
    open(a, 'w', encoding='utf-8').write(ass)
    vf = f"subtitles={a}" + (f":fontsdir={fontsdir}" if fontsdir else '')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'color=c=0x404040:s={W}x{H}:d=1', '-vf', vf, '-ss', '0.5',
                    '-frames:v', '1', o], check=True)
    return _mask(cv2.imread(o), fill, 60)

def _iou(sm, s, cm, c):
    """overlap of the two fill masks after aligning left edge and baseline."""
    h0 = s['base'] - s['top'] + 1; hb = s['bot'] - s['base']
    A = sm[s['top']:s['bot'] + 1, s['x0']:s['x1'] + 1]
    B = cm[c['base'] - h0 + 1:c['base'] + hb + 1, c['x0']:c['x0'] + s['w']]
    hh, ww = min(A.shape[0], B.shape[0]), min(A.shape[1], B.shape[1])
    A, B = A[:hh, :ww], B[:hh, :ww]
    return float((A & B).sum() / max(1, (A | B).sum()))

def _outline(img, mask):
    """outline thickness: rings around the fill that are mostly dark."""
    # the first ring or two are anti-aliased fill→outline pixels: count dark rings from the first dark one, stop at the
    # first light ring after that, and add the transition rings back (they are outline too, just blended)
    m = mask.astype(np.uint8); g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY); prev = m; first = last = None
    for r in range(1, 14):
        d = cv2.dilate(m, np.ones((2 * r + 1, 2 * r + 1), np.uint8)); ring = (d > 0) & (prev == 0); prev = d
        dark = ring.sum() > 0 and (g[ring] < 110).mean() >= 0.5  # compressed outlines blur toward the background
        if dark:
            first = first or r; last = r
        elif first: break
        elif r > 3: break
    return last or 0

def run(video, t=0.5, text=None, fill=None, font_dirs=(), style=None, top=5):
    tmp = tempfile.mkdtemp(prefix='vc_capfont_')
    img = _frame(video, t, os.path.join(tmp, 'f.png')); H, W = img.shape[:2]
    fill = fill or _auto_fill(img)
    full = _mask(img, fill); ln = _line(full, H)
    if not ln: raise SystemExit(f'no caption of colour {fill} found at t={t}; pass --fill or another --t')
    sm = np.zeros_like(full); sm[ln[0]:ln[1]] = full[ln[0]:ln[1]]; s = _measure(sm)
    if text is None:
        crop = (255 - sm[ln[0]:ln[1]].astype(np.uint8) * 255); cv2.imwrite(os.path.join(tmp, 'o.png'), cv2.resize(crop, None, fx=2, fy=2))
        text = subprocess.run(['tesseract', os.path.join(tmp, 'o.png'), '-', '--psm', '7'], capture_output=True, text=True).stdout.strip()
        text = re.sub(r'\s+', ' ', text)
    dirs = [FONTS, os.path.expanduser('~/.fonts')] + list(font_dirs)
    files = sorted({p for d in dirs for p in glob.glob(os.path.join(d, '**', '*.[ot]tf'), recursive=True)})
    # libass silent fallback detector: what a missing family renders like
    ref_missing = _render(text, 'NoSuchFontVcX', 60, None, W, H, fill, 300, tmp)
    res, seen = [], set()
    for p in files:
        fam = _family(p); fd = os.path.dirname(p)
        if fam in seen: continue   # same family installed in several dirs
        seen.add(fam)
        m60 = _render(text, fam, 60, fd, W, H, fill, 300, tmp)
        if np.array_equal(m60, ref_missing): continue
        c60 = _measure(m60)
        if not c60: continue
        size = max(8, round(60 * s['w'] / c60['w']))
        cm = _render(text, fam, size, fd, W, H, fill, 300, tmp); c = _measure(cm)
        if not c: continue
        iou = _iou(sm, s, cm, c); xh = abs(c['core'] / s['core'] - 1)
        res.append(dict(font=fam, file=p, size=size, iou=round(iou, 3), width=c['w'], core=c['core'],
                        score=round((1 - iou) + xh + abs(c['w'] / s['w'] - 1), 3), _base=c['base']))
    if not res: raise SystemExit('no candidate font could be rendered')
    res.sort(key=lambda r: r['score']); best = res[0]
    margin_v = 300 + (best['_base'] - s['base'])
    out = dict(sample=dict(t=t, text=text, fill=fill, width=s['w'], baseline=s['base'], core=s['core'], frame_h=H),
               best=dict(font=best['font'], size=best['size'], margin_v=int(margin_v), outline_px=_outline(img, sm),
                         iou=best['iou'], file=best['file']),
               ranking=[{k: v for k, v in r.items() if not k.startswith('_')} for r in res[:top]])
    if style:
        sp = os.path.join(style, 'style.json'); st = json.load(open(sp)) if os.path.exists(sp) else {}
        cap = st.setdefault('captions', {})
        cap.update(font=best['font'], size=best['size'], margin_v=int(margin_v), outline_px=out['best']['outline_px'],
                   ref_h=H, fill=fill, bold=0)
        json.dump(st, open(sp, 'w'), indent=1, ensure_ascii=False); out['written'] = sp
    return out
