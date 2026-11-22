# Dark Atlas Tales — series kit (US states)

Self-contained production kit for the Dark Atlas horror-legend shorts (9:16, ~72 s, 2D vector art drawn in Python,
Sonic Voice "Milo", Oswald word-by-word captions). It has its **own** render engine (`dark_atlas/tools/engine.py`,
`style.py`, `render_epXX.py`) and its own QA (`qa_full.py`, 11 metrics) — it does not use the vidclone EDL / gates.

Source: `DarkAtlas_US_States_Kit_2026-11-21.zip` on the user's Drive (file id `14jO5Kk1QWOZxeb--xqu9vKMYajXqho9m`).
The full handoff guide (Vietnamese) is `00_DOC_TRUOC.md`; the workflow skill is `skill/dark-atlas-tales-production/`
(also linked as `.claude/skills/dark-atlas-tales-production` at the repo root so Claude Code picks it up here).

## Layout
| Path | What |
|---|---|
| `dark_atlas/` | the project folder (`DA/` in the skill); run every command from here |
| `dark_atlas/EP02_belsnickel`, `EP04_kushtaka`, `EP05_nimerigar` | approved episodes: script, sources, style.json, voice + word transcript, SFX cues |
| `dark_atlas/assets/sfx/` | shared horror SFX library + per-monster SFX (do not regenerate) |
| `dark_atlas/assets/music/` | US-series bed (`us_bed_master_5min.mp3` in git; `.wav` master restored by `fetch_kit.sh`) |
| `dark_atlas/fonts/` | Oswald (captions/titles); Gelasio Bold and Kalam = open stand-ins for Windows Georgia Bold / Segoe Script |
| `skill/` | the skill (rules, QA table, templates, copies of the tools) |
| `video_mau/` | the 3 approved videos (not in git; `fetch_kit.sh`) |

Not in git (see `.gitignore`): WAV masters, episode `sfx.wav` (rebuild with `build_sfx.py`), MP4s, stills / QA sheets.

## Setup (Linux / cloud session)
```bash
python3 -m venv ~/.darkatlas-venv
~/.darkatlas-venv/bin/pip install -r styles/dark-atlas-tales/requirements.txt
styles/dark-atlas-tales/fetch_kit.sh        # optional: WAV masters + reference videos (needs drive.usercontent.google.com)
```
Smoke test (≈ 40 s, writes `EP05_nimerigar/test.jpg`: jumpscare, title card, reveal):
```bash
cd styles/dark-atlas-tales/dark_atlas && ~/.darkatlas-venv/bin/python -I tools/render_ep05.py . "0.9,15,70.8" test.jpg
```

## Changes from the zip (2026-11-22)
- `render_ep02.py` / `render_ep04.py`: Windows-only fonts fall back to `fonts/Gelasio-Bold.ttf` / `fonts/Kalam-Regular.ttf`.
- `mix_episode.py`: uses `<bed>.mp3` when the `<bed>.wav` master is missing.
- Both changes are mirrored in `skill/.../scripts/`.

## Checked here (2026-11-22)
- Stills for EP02 (incl. the 1827 newspaper), EP04 (incl. the ethnologist's notebook) and EP05 render correctly.
- `build_sfx.py` (EP05, 27 cues) and `mix_episode.py` (WAV and MP3 bed) run.
- `qa_full.py` on the approved EP05 v3: 11/11 PASS. Note: it reads `voice_milo_transcript.json` next to the video,
  so the MP4 must sit in its episode folder.

## External services a new episode needs
| Step | Needs |
|---|---|
| Voice (`sonic_tts.py`) | `SONIC_API_KEY` + host `sonicvoice.pro` (header `X-API-Key`) |
| Transcribe (`transcribe.py`) | Whisper `large-v3` (~3 GB) from `huggingface.co` on first run |
| Monster SFX (2–3 per episode, quote first) | Magnific connector (`audio_sfx_generate`), or free libraries — `assets/sfx/README.md` |
