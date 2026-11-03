---
name: make
description: Make a new video in a learned style — from a topic, a pasted script or a Notion page — through script, voice, word timings, shot list, generated or supplied visuals, EDL assembly (camera moves, transitions, grade, captions, mix) and QA against the style's gates until it passes. Works for any niche the style folder describes. Use when the user invokes /vidclone:make or asks for a video "like the samples".
---
# Make a video in a learned style

Input: style name (folder `styles/<name>` from skill `learn`) + topic, script or Notion link. No style yet → run `learn` first.
Read `~/.vidclone/config.json`, then `styles/<name>/style.md`, `style.json`, `profile.json`, `gates.json`. Keep the task list current.
Work folder: `<work_dir>/<style>/<slug>/` with `script.txt`, `voice/`, `art/`, `clips/`, `audio/`, `words.json`, `shots.md`, `edl.json`, `out/`.

## 1. Script
- Given a script: use it **verbatim**; check it against the bible (hook type and length, beat order, word count for the target duration
  = `wpm` × minutes, closer) and suggest changes — don't rewrite silently.
- Given a topic: write an original script that follows the narrative template (same hook type, beats at the same % of duration, same pace,
  closer pattern, recurring phrases in spirit, never copied lines). True stories: check facts and keep dates/numbers right.
- Numbers spelled the way they should be read. Show the script to the user before spending credits unless they said to go ahead.

## 2. Voice → word timings
Generate with `style.json.voice` (2 takes when the tool allows). Then:
```bash
bin/vidclone transcribe voice/take1.mp3 --out words.json --script script.txt
```
Measure wpm = words / speech span; outside the gate → regenerate with another speed, or time-stretch (`ffmpeg -af atempo=X`, 0.9–1.15)
and transcribe again. Words must equal the script (fix ASR spellings in `words.json` against `script.txt`).

## 3a. Pose script first (for character styles such as animal-toon-eyes)
Measure the samples' **picture changes per minute** (`frames.check` with no planned set: every cut or in-place swap counts):
animal-toon-eyes samples 29–101 / min (median ~51); stills-with-puppet-wiggle only reaches 15–20. So the action is carried by
**pose drawings**, not by wiggle:
- Write, per sentence, the **poses** the character goes through — one new pose or framing every 0.6–1.5 s (stand → sit → paw on chin →
  close-up worried → squashed by a patting hand …). Each pose is its own picture, chained from the character's base for identity.
- **2-frame loops** for repeated actions (eating, chewing, rubbing a forehead, paddling): two pictures swapped at 2–4 Hz.
- **Entrances and exits**: characters rise from behind foreground plants, slide in from the edge, dive in; hands slide in and act
  (pat, feed, poke) — cut-out layer with keys, a foreground layer (ferns, grass, leaf) in front of it.
- **Several characters** in a frame when the narration lists animals; a human stand-in (real body, cartoon head) for "scientists / you".
- Per pose 1–2 small events on the words: eye change, icon pop, thought bubble, prop slide, typed note, squash on impact.
- **Keyframed blocks, not point wiggle** (user correction 2026-11-03, confirmed at 10 fps on S01): every pose picture is cut out
  (BiRefNet, full-frame and aligned) and placed over ONE clean plate per scene ("remove the animal" edit); the block itself is
  keyframed — walk in from the edge with `hop` bounces and shrink to its spot, drop onto its seat with a landing squash, snap in
  with `ease: back`, lean / tilt about a `pivot`, slide in from the side the body is cut off on, rise from the bottom. Props and
  foreground plants (ferns, leaves) are blocks with their own paths, in front of the character. Eyes ride on the block (`parent`).
  Reference build: `REMAKE-S01-panda/gen_edl_v3.py`. Puppet warp only as a last resort; never as the main motion.
- Don't skimp (user correction): draw every prop the sample has as its own block (food held to the mouth, bitten food,
  chewed bits, grass tufts at the feet and in the mouth, bushes in front of people); side characters are separate blocks
  with toon eyes and entrances (rebuild group shots over an empty plate); eating = the jaw lifted off the block (`parts`,
  dark mouth behind) and chewing; profile = ONE eye (`single`); an expression change on almost every beat (brows, lids,
  `low`, `mood: happy|shock`, `pupil`); plates slightly blurred; `shadow` under standing blocks; eyes ~0.58 x eye spacing
  (panda), set `lid` for dark-furred animals. Read positions off gridded crops (picture fractions), never by guess.
  Cover cut-out defects (broken legs, halo) with a foreground prop.
- Devices from the other samples (all in `vidclone/layers.py`): `meter` battery that drains with effort, cutout `fill`
  (silhouette energy gauge), `bubble` thought/speech with words that change (`texts`), `text` + `texts` for calendars and
  counters, `tint` for night → day / flashback (list it LAST to wash the whole frame), keys `alpha` + icon `halo` for ghosts,
  cutout `glow` for the injured / chosen one, icons skull / heart / clock / fire / zap / note on their words, line-ups of
  characters entering one by one with labels. Use `layers.shift_times(layers, dt)` to turn absolute script times into shot times.
- Keep the camera calm while the pictures change (S01: camera moving on ~48 % of frames): big push/pull on every pose swap
  hides the swaps and doubles the frame difference. Small travel per shot, the pose change carries the beat.
QA: picture changes / min inside the samples' range, plus `vidclone.parts` local motion. Count changes with a detector that
ignores camera motion (frame diff > 2× the median of its ±2–9 neighbours, ≥ 4): REMAKE-S01-panda 111 / min vs S01 98 / min,
local motion 79 % active / p95 6.0 px/f (samples 65–100 %, 6–11) — the pose-script reference build.

## 3. Shot list (`shots.md`)
One row per beat from the bible's shot grammar, placed on the word timings:
`id | start–end | words | subject + action (what we SEE happen on the key word) | shot size/angle | camera move | transition in | text/labels | sfx`.
Timing rule: every visual reaction (cut, swap, prop pop-in, kick) lands **0–3 frames (0–0.1 s) before** its word's start in `words.json`,
never after; the SFX for it sits on the same frame. Never show only what the narration already says when a gag can add to it.
Match the profile: median shot length, transitions/min and mix, camera-move shares, dissolve length, cuts allowed, motifs (open and close
on the same image if the samples loop), text overlays where the samples use them. Every noun/verb that matters gets a visual.

## 4. Visuals (by `style.json.engine`, see `docs/ENGINES.md`)
- **stills-motion**: one image per shot (or per 2–3 shots with different framings via `focus`/`from`/`to`), generated with
  `style.json.image_prompt` + the shot's subject; consistent characters = same description block + reference image every time. Vertical
  canvas, leave room for camera moves (generate ≥ 1.2× the frame).
- **Animated layers** (when the bible's samples animate inside shots — check them at 6 fps, not 1 fps): give shots `layers`
  (see `vidclone/layers.py`): procedural eyes over the animal's real eyes (positions via `gemini.find_points` or read off the picture),
  props generated on pure green and cut with `python -m vidclone.cutout`, icons, bounce text; key expressions and pops on the words.
- **ai-video**: one clip per shot from `video_prompt` (+ start image from stills-motion for consistency); trim with `in`/`dur`.
- **footage**: the user's clips; cut on the word timings, punch-in (`push` with amount 0.1–0.25 over ≤ 0.3 s) where the style does.
- **3d-toon**: hand the script, shot list and gates to the `rickclips` plugin (`/rickclips:episode`), then QA here.
- Download every generated file (full-resolution URL) into the work folder; record prompts in `prompts.json` so the video can be rebuilt.

## 5. Sound
Music from `style.json.music_prompt` (length ≥ video + 5 s, instrumental, the profile's key/tempo/feel); SFX from the bible's list on the
shot list's cue times; level/ducking from the profile (`bed_db`, mono/stereo, LUFS, true peak).

## 6. Assemble
Write `edl.json` (format in `vidclone/assemble.py` docstring): shots with `dur`, `move`/`amount`/`focus` or `from`/`to`, `trans`
(kind + dur) from the shot list; `grade` from style.json; `captions: {"words": "words.json", "style": "<styles>/<name>", "offset": <voice_offset>}`;
`audio` block; `creep` from style.json (every `"move": "none"` hold still zooms slowly, so nothing freezes) and `kicks`
(`{"t", "amp", "frames"}`, impact shakes that flip every frame and decay over ~7 f) on the shot list's impact words. Then
```bash
bin/vidclone assemble edl.json
```
Shot durations must add up so the picture covers the voice + tail (transitions overlap the shots they join).

## 7. QA loop — not done until it passes
```bash
bin/vidclone qa out/final.mp4 --style styles/<name> --edl edl.json
```
Read `report.md` (gates + frame check: black / unplanned white / frozen holds fail; unplanned pops are listed for review with
`sheets/problems.jpg`), then look at `sheets/compare.jpg` (sample vs new at the same % of time), `sheets/sec_*.jpg`, `sheets/shots_*.jpg`.
Then run the **verifier round** from the `qa` skill (fresh agent, side-by-side sheets, scores per area + numbered fixes with times);
fix, reassemble, re-QA. Stop after 3 rounds or when scores stop rising, and report the scores.
Fix failures at the source (shot timing, moves, grade, caption style in `style.json`, music level, script length), reassemble, re-QA.
Eye review too: every key word has its action on screen, no broken/blank frames, captions never covered, text legible, characters
consistent, nothing copied from the samples. A gate that is wrong for this video (e.g. duration of a deliberately longer cut) → say why
in the report instead of forcing it.

## 8. Deliver
Copy `final.mp4` (+ a smaller preview: `ffmpeg -i final.mp4 -vf scale=720:-2 -crf 26 preview.mp4`) to `deliver_dir`, send the preview,
and report: duration, QA x/y with any failing gate explained, what was checked by eye, tools/credits used, anything not done.
