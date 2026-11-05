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
Measure wpm = words / speech span; outside the gate → regenerate with another speed, or cap long pauses first (cut the middle
of gaps over the samples' longest pause) and then time-stretch (`ffmpeg -af atempo=X`, 0.8–1.35) and transcribe again — TTS
takes read slower than the samples even with a "fast" tag. Words must equal the script (fix ASR spellings in `words.json`
against `script.txt`). Changing the pace after shots exist: stretch the voice and scale EVERY timing (shots, words, captions,
SFX) by the same factor in one pass; never re-plan the scenes.

## 2b. New style or "not like the samples yet" → imitate 15–20 s first
Before full episodes in a style that has not been accepted yet, rebuild the first 15–20 s of one sample beat for beat
(own content, same devices, same timing), put it next to the sample (`qa` compare + frames at the same times) and fix
what differs. Both accepted styles so far only converged after this step (`docs/LESSONS.md`).

## 3a. Style recipe and motion
Niche rules live in the style folder, not here. If `styles/<name>/recipe.md` exists it is this style's production recipe
(assets, motion system, numbers, devices, voice) — follow it, use its `kit.py` helpers and `examples/` reference build.
Whatever the niche, match the **motion**, not only the edit. The gates `picture_changes_per_min`, `local_motion_share`
and `local_motion_p95` (measured by `analyze`, checked by `qa`) tell what kind of video it is:
- Few changes, little local motion → stills / footage with camera moves; the shot list and the camera carry it.
- Many changes / high local motion → the action is inside the pictures. Plan it before any image is made:
  a **pose script** (a new pose or framing every ~0.6–1.5 s, each pose its own picture chained from the character's base for
  identity; 2-frame loops for repeated actions), then **keyframed cut-out blocks**: each character / prop cut out and placed
  over one clean plate per scene, the block keyframed as a whole (walk in with `hop`, land with a squash, snap in with
  `ease: back`, lean about a `pivot`, slide in from the side it is cut off on). Moving parts (jaws, paws) are `parts` lifted
  off the block. Side characters and props are blocks of their own. Faces / eyes / expressions on the words.
  Puppet warp only as a last resort, never as the main motion.
- Keep the camera calm while pictures change — a big move on every swap hides the swaps.
- Study the samples at 10 fps (not 1 fps sheets) for every device they use, and add it to the recipe.
Toolbox (`vidclone/layers.py`, documented in its docstring): cut-out blocks (`keys` with ease / hop / alpha, `pose`,
`parts`, `shadow`, `fill` silhouette gauge, `glow`), cartoon `eyes` (single profile eye, brows, lids, moods), `png` props,
`icon`s, `text` with changing `texts`, `bubble`, `meter`, `tint`, `lens`, `warp`. Write layer times in script seconds and
convert with `layers.shift_times(layers, shot_start)`. Read positions off gridded crops (picture fractions), never guess;
cover cut-out defects with a foreground prop.

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
- **Animated layers** (when the samples animate inside shots — see 3a): give shots `layers` (`vidclone/layers.py`): cut-out
  blocks over clean plates, characters' eyes (positions from gridded crops or `gemini.find_points`), props generated on pure green
  (or white when the prop is green) and cut with `python -m vidclone.cutout [--white]`, icons, text; key expressions and pops on the words.
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
consistent, nothing copied from the samples, the main subject never covered by props or graphics, faces and key text out of the
caption band, the same graphics package as the samples (not a new card style per episode), and the light / space checks of the
`qa` skill (a picture can pass every number and still be flat). A gate that is wrong for this video (e.g. duration of a deliberately longer cut) → say why
in the report instead of forcing it.

## 8. Deliver
Copy `final.mp4` (+ a smaller preview: `ffmpeg -i final.mp4 -vf scale=720:-2 -crf 26 preview.mp4`) to `deliver_dir`, send the preview,
and report: duration, QA x/y with any failing gate explained, what was checked by eye, tools/credits used, anything not done.
