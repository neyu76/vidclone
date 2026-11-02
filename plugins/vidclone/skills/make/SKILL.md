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

## 3. Shot list (`shots.md`)
One row per beat from the bible's shot grammar, placed on the word timings:
`id | start–end | words | subject + action (what we SEE happen on the key word ±0.15 s) | shot size/angle | camera move | transition in | text/labels | sfx`.
Match the profile: median shot length, transitions/min and mix, camera-move shares, dissolve length, cuts allowed, motifs (open and close
on the same image if the samples loop), text overlays where the samples use them. Every noun/verb that matters gets a visual.

## 4. Visuals (by `style.json.engine`, see `docs/ENGINES.md`)
- **stills-motion**: one image per shot (or per 2–3 shots with different framings via `focus`/`from`/`to`), generated with
  `style.json.image_prompt` + the shot's subject; consistent characters = same description block + reference image every time. Vertical
  canvas, leave room for camera moves (generate ≥ 1.2× the frame).
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
`audio` block. Then
```bash
bin/vidclone assemble edl.json
```
Shot durations must add up so the picture covers the voice + tail (transitions overlap the shots they join).

## 7. QA loop — not done until it passes
```bash
bin/vidclone qa out/final.mp4 --style styles/<name>
```
Read `report.md`, then look at `sheets/compare.jpg` (sample vs new at the same % of time), `sheets/sec_*.jpg`, `sheets/shots_*.jpg`.
Fix failures at the source (shot timing, moves, grade, caption style in `style.json`, music level, script length), reassemble, re-QA.
Eye review too: every key word has its action on screen, no broken/blank frames, captions never covered, text legible, characters
consistent, nothing copied from the samples. A gate that is wrong for this video (e.g. duration of a deliberately longer cut) → say why
in the report instead of forcing it.

## 8. Deliver
Copy `final.mp4` (+ a smaller preview: `ffmpeg -i final.mp4 -vf scale=720:-2 -crf 26 preview.mp4`) to `deliver_dir`, send the preview,
and report: duration, QA x/y with any failing gate explained, what was checked by eye, tools/credits used, anything not done.
