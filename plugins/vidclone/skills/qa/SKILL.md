---
name: qa
description: Check any video against a learned style — measure it the same way as the samples, compare with the style's gates, build sample-vs-new contact sheets and review by eye. Use after making a video, to judge someone's edit against a style, or when the user asks "does this match the samples?".
---
# QA against a style

```bash
bin/vidclone qa <video.mp4> --style styles/<name> [--edl edl.json]     # exit code 0 = all gates + frame check pass
```
→ `styles/<name>/qa/<video>/report.md` (✅/❌ per gate with value, target and range), `qa.json`, `analysis.json`, `sheets/compare.jpg`
(sample | new at the same relative times), `sheets/sec_*.jpg`, `sheets/shots_*.jpg`.

**Frame check** (every frame at 30 fps): black frames, unplanned white frames and holds frozen longer than `style.json`
`frame_check.max_frozen_s` (default 0.4 s) fail; unplanned pops (one-frame jumps) are listed for review. `sheets/problems.jpg` shows each
problem frame between its neighbours. With `--edl`, shot starts, transitions, overlay edges and kicks count as planned; without it,
the measured transitions do (so in-place swaps the analyser missed show up as pops — check them by eye).

**Motion** (every video): `analyze` records `motion` — picture changes / min (cuts + in-place swaps + block moves, counted
with a detector that tolerates camera motion) and local motion (`parts`: flow minus the camera fit → share of the frame moving,
p95 speed, heat maps in `<out>/parts/parts_*.jpg`). They are gated like everything else (`picture_changes_per_min`,
`local_motion_share`, `local_motion_p95`). As a guide: stills with camera moves read 10–20 changes / min, ~25 %, ~1.5 px/f;
pose-swap / cut-out character styles 30–110 / min, 65–100 %, 6–16 px/f. Older sample folders: `bin/vidclone motion
styles/<name>/samples/*` then `merge` to add the gates. Fast block snaps can read as camera moves (camera ease-in gate) — check by eye.

**Verifier round** (after the numbers pass, or when they cannot judge the look): give one fresh agent (Agent tool, no prior context)
`sheets/compare.jpg`, 2–3 `sheets/sec_*.jpg` of the new video, the matching sample sheets and `style.md`. Ask for ≤ 200 words:
a score out of 10 for each area — subject & art style, faces/characters, colour & light, framing & composition, camera & rhythm,
captions & text, story-to-picture match — and a numbered fix list with times. Map each fix to its source (prompt, shot list, EDL,
style.json), fix, reassemble, re-QA, and send the next round to the same verifier (SendMessage) so scores are comparable.
Up to 3 rounds; report the scores per round.

Then look at the sheets and judge what numbers cannot: subject and action match the narration, framing/composition like the samples,
art style and character consistency, text legibility, no blank/broken frames, nothing copied from the samples.
**Matching numbers can still be a flat picture** (`docs/LESSONS.md` B): compare sample vs new on the same frames for camera
height and lens width (planes visible, subject size), foreground / subject / background layers and haze, dark areas and
pools of light, palette width and the one accent colour, surface detail, scenes per 15 s, hands acting on props, the
subject never covered and faces out of the caption band. List differences by impact before fixing.

Reading failures:
- duration / wpm → script length or voice speed; shot length / transitions per min → the shot list; camera shares → `move` mix in the EDL;
- saturation / brightness / contrast / warmth → `grade` (or the image prompt's palette); detail low → images too small for the push-in or blur;
- shadow share / light range / light pattern / vignette / hue spread (`look.light`, styles merged after 2026-11-05) → lighting and
  palette of the pictures / 3D scene (key light, dark corners, one accent colour), not the global grade — brightening to hit a
  median flattens the look;
- caption baseline/height/words → `style.json` `captions` (baseline_rel, height_rel, size_per_cap, words_hist);
- LUFS / true peak / bed level / stereo → the EDL `audio` block.
Metric limits: OCR misses stylised fonts (caption share reads low) and can misread the caption colour (check a frame), fast whips
can read as dissolves, `hook_end_s` reads the first Whisper segment (false fail when the hook is short), faces = frontal human faces only
(cartoon faces count sometimes). When a gate does not apply, turn it off in `gates.json` with a note rather than chasing it.
Report pass count, each failure with the fix you made or why it stays, and what you checked by eye.
