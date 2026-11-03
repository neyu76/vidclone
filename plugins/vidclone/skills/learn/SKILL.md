---
name: learn
description: Learn a video style from one or more sample videos (any niche — story shorts, explainers, finance, history, gaming, talking-head, product, kids, documentary…) plus optional files (script, SRT, brand kit, music, character sheets). Measures every detail (edit rhythm, transitions, camera moves, colour, captions, narration pace, hook/structure, music, SFX, loudness), reads the frames, and writes a reusable style folder (profile, QA gates, style bible, production plan). Use when the user gives sample videos and wants similar videos made, or invokes /vidclone:learn.
---
# Learn a style from samples

Input: sample video paths/URLs + optional files, and a style name (ask if none; slug like `history-shorts`).
Read `~/.vidclone/config.json` first (missing → skill `setup`). Commands run with `run_prefix` in `repo_dir`; CLI = `bin/vidclone`.
Keep the user's task list current. One sample ≈ 1–2 min of analysis per minute of video on 8+ cores.

## 0. Rights and inputs
- URL samples: download with the `watch` skill / yt-dlp only when the user has the right to use them for analysis. Keep samples on this
  machine; never commit or upload sample videos, frames or their audio. The style folder keeps numbers, text notes and small sheets only.
- The goal is the **style** (form, rhythm, grammar). New videos must have original content: never reuse the sample's script text,
  characters, logos, artwork, music or voice clone of a person without their consent.
- 3–5 samples of the same series give much better ranges than one. Mixed series → separate styles.

## 1. Measure (per sample)
```bash
bin/vidclone analyze <sample.mp4> --style styles/<name> --id S01 [--script given_script.txt]
```
→ `styles/<name>/samples/S01/`: `analysis.json`, `words.json` (word timings), `sheets/sec_*.jpg` (1 still/s), `sheets/shots_*.jpg`
(start/mid/end of each shot), `work/` (proxy, stills, wav — local only, git-ignored).
What it measures (all relative to frame size, so it transfers across resolutions):
- **edit**: shots, transitions (cut / dissolve / flash / fade / whip) with time and length, shots/min, camera move per frame
  (push / pull / pan / tilt / roll / static via optical-flow similarity fit), how often the move changes, zoom/pan speeds, jitter.
- **look**: saturation, brightness, contrast, fine-detail ratio, warmth, clipping, palette (k-means), faces share/size, letterbox, brightness arc.
- **speech**: transcript, wpm, pauses, sentence lengths, hook (first sentence) and closer, questions, 2nd-person use, words per second.
- **audio**: LUFS / true peak / LRA, stereo width, music bed level in gaps vs voice, key, tempo, beat regularity, voice pitch, onset/SFX density.
- **text**: captions (OCR matched to the narration): baseline/height/width/centre, words on screen (histogram), case, fill/edge colours,
  boxed or outlined; other on-screen text (titles, labels, numbers).
- **motion**: picture changes per minute (cuts + in-place swaps + block moves, camera-tolerant) and local motion inside shots
  (share of the frame moving, p95 speed, heat maps in `parts/`) — separates "stills + camera" from animated / cut-out styles.
Check the numbers against the sheets when something looks odd (e.g. a "cut" that is a 4-frame dissolve) and say so in the bible.

## 1b. Watch the motion at 10 fps (1 fps sheets hide it)
For each sample, three 2.4 s stretches (start, middle, late) as 10 fps strips, kept in a scratch folder (never in the repo):
```bash
ffmpeg -ss <t> -t 2.4 -i <sample.mp4> -vf "fps=10,scale=120:-1,tile=12x2" -frames:v 1 strip.jpg
```
plus a few full-size stills of close-ups. Write down what moves and how: camera only, pose swaps, keyframed cut-out blocks
(whole-object moves over a fixed background), part animation (jaws, limbs), entrances / exits, props and side characters as
separate pieces, faces / eyes and expression changes, and every device (gauges, bubbles, counters, icons, labels, tints,
ghosts). This list drives section 4b of the bible and the recipe.

## 2. Merge → gates
```bash
bin/vidclone merge styles/<name>
```
→ `profile.json` (per-metric median/min/max over samples + facts) and `gates.json` (QA ranges: target, lo, hi, on).
Turn a gate off (`"on": false`) when it does not define the style (e.g. face share for a faceless channel); hand-set bounds get `"manual": true`
so a later merge keeps them.

## 3. Read the samples (the part numbers cannot do)
Open every `sheets/shots_*.jpg` and `sec_*.jpg`, the transcript and `analysis.json`. For each sample write a beat table:
`time | narration | what is on screen | subject/action | shot size & angle | camera move | transition | text on screen | sound`.
Then write **`styles/<name>/style.md`** (the style bible), using `docs/STYLE_TEMPLATE.md`:
format & niche · narrative template (hook type with the samples' hook lines paraphrased, beats with % of duration, twist position, closer
pattern, phrases that recur) · visual medium (2D/3D/AI art/footage/screen-recording/talking head…) and art direction (palette hexes,
lighting per act, textures, character design) · shot grammar (shot sizes, what each beat type looks like, how a sentence becomes an
action, motifs, loops) · camera and transitions (with the measured numbers) · typography (captions + other text) · sound (voice
character, pace, music genre/key/level, SFX use) · what makes it work · what to avoid. Mark each rule [measured] / [seen] / [inferred].

## 4. Decide how to produce it → `styles/<name>/style.json`
Pick the engine(s) from `docs/ENGINES.md` that can reach this look with the tools this machine has (config `tools`/`engines`), and write:
```json
{"engine": "stills-motion", "canvas": {"w": 1080, "h": 1920, "fps": 30},
 "voice": {"tool": "elevenlabs", "voice_id": "...", "model": "...", "speed": 1.0, "notes": "young male, energetic"},
 "image_prompt": "<art-direction prompt template with {subject}>", "video_prompt": "...",
 "music_prompt": "...", "sfx_list": ["whoosh", "pop", "..."],
 "grade": {"saturation": 1.0, "contrast": 1.0}, "captions": {"font": "Work Sans", "upper": false, "pop": false},
 "edit": {"default_transition": {"kind": "dissolve", "dur": 0.23}, "moves": {"push": 0.5, "pull": 0.2, "pan": 0.2, "static": 0.1}},
 "limits": ["what this engine cannot match, honestly"]}
```
Caption fonts: if the measured style needs another face, pick an OFL font (Google Fonts) that matches the letterforms on the sheets, put
the .ttf in `fonts/` (with its licence) and name it in `style.json`.
Then write **`styles/<name>/recipe.md`** — how to BUILD this style (template at the end of `docs/STYLE_TEMPLATE.md`): numbers
to hit, asset pipeline, motion system mapped to `vidclone/layers.py` features, faces / expressions, devices → layer types, voice.
Everything niche-specific goes there (and in an optional `kit.py` / `examples/`), never into the generic skills. When the
user corrects a video, add the lesson to the recipe so the next video of this style starts from it.

## 5. Report
Show the user: a short summary of the style (5–8 lines), the key numbers, the engine choice and its limits, and where the bible is.
Offer `/vidclone:make <name> <topic or script>` as the next step.
