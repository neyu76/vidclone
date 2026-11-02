---
name: qa
description: Check any video against a learned style — measure it the same way as the samples, compare with the style's gates, build sample-vs-new contact sheets and review by eye. Use after making a video, to judge someone's edit against a style, or when the user asks "does this match the samples?".
---
# QA against a style

```bash
bin/vidclone qa <video.mp4> --style styles/<name>      # exit code 0 = all gates pass
```
→ `styles/<name>/qa/<video>/report.md` (✅/❌ per gate with value, target and range), `qa.json`, `analysis.json`, `sheets/compare.jpg`
(sample | new at the same relative times), `sheets/sec_*.jpg`, `sheets/shots_*.jpg`.

Then look at the sheets and judge what numbers cannot: subject and action match the narration, framing/composition like the samples,
art style and character consistency, text legibility, no blank/broken frames, nothing copied from the samples.

Reading failures:
- duration / wpm → script length or voice speed; shot length / transitions per min → the shot list; camera shares → `move` mix in the EDL;
- saturation / brightness / contrast / warmth → `grade` (or the image prompt's palette); detail low → images too small for the push-in or blur;
- caption baseline/height/words → `style.json` `captions` (baseline_rel, height_rel, size_per_cap, words_hist);
- LUFS / true peak / bed level / stereo → the EDL `audio` block.
Metric limits: OCR misses stylised fonts (caption share reads low), fast whips can read as dissolves, faces = frontal human faces only
(cartoon faces count sometimes). When a gate does not apply, turn it off in `gates.json` with a note rather than chasing it.
Report pass count, each failure with the fix you made or why it stays, and what you checked by eye.
