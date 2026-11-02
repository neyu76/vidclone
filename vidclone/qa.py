"""QA a new video against a style's gates: analyze it the same way, compare, write report.md/json + compare sheet."""
import os, glob
from . import profile, sheets
from .common import load, save

def run(video, style_dir, out=None):
    name = os.path.splitext(os.path.basename(video))[0]
    out = out or f'{style_dir}/qa/{name}'
    r = profile.analyze(video, out, with_sheets=True)
    gates = load(f'{style_dir}/gates.json')
    rows = []
    for g in gates:
        if not g.get('on', True): continue
        v = profile._get(r, g['path'])
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            rows.append({**g, 'value': v, 'ok': None}); continue
        ok = bool((g['lo'] is None or v >= g['lo']) and (g['hi'] is None or v <= g['hi']))
        rows.append({**g, 'value': round(float(v), 4), 'ok': ok})
    passed = sum(1 for x in rows if x['ok']); failed = [x for x in rows if x['ok'] is False]
    samples = sorted(glob.glob(f'{style_dir}/samples/*/work'))
    if samples: sheets.compare(samples[0], f'{out}/work', f'{out}/sheets/compare.jpg')
    rep = {'video': os.path.abspath(video), 'passed': passed, 'checked': sum(1 for x in rows if x['ok'] is not None),
           'failed': [x['key'] for x in failed], 'rows': rows}
    save(rep, f'{out}/qa.json')
    fmt = lambda x: '—' if x is None else f'{x:g}' if isinstance(x, (int, float)) else str(x)
    md = [f'# QA {name} vs {os.path.basename(style_dir.rstrip("/"))}', '',
          f'**{passed}/{rep["checked"]} pass**' + (f' — fail: {", ".join(rep["failed"])}' if failed else ''), '',
          '| | Metric | Value | Target | Range |', '|---|---|---|---|---|']
    for x in rows:
        mark = '✅' if x['ok'] else '❌' if x['ok'] is False else '·'
        md.append(f"| {mark} | {x['label']} | {fmt(x['value'])} | {fmt(x['target'])} | {fmt(x['lo'])} … {fmt(x['hi'])} |")
    md += ['', 'Sheets: `sheets/compare.jpg` (sample | new), `sheets/sec_*.jpg`, `sheets/shots_*.jpg` — review them by eye too.']
    open(f'{out}/report.md', 'w', encoding='utf-8').write('\n'.join(md) + '\n')
    print('\n'.join(md))
    return rep
