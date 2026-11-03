# vidclone — notes for Claude

Workflow lives in the plugin skills (`plugins/vidclone/skills/{setup,learn,make,qa}`); this file is the code map and the known limits.

## Code (`vidclone/`, Python 3.10+, venv `~/.vidclone/venv`, run via `bin/vidclone`)
| Module | Does |
|---|---|
| `common.py` | ffprobe, analysis inputs (30 fps H.264 proxy at 360 px short side, 1 fps PNG stills at 720 px, 48 k stereo + 16 k mono wav) |
| `edit.py` | shots, transitions, camera motion (Farneback flow on the 360 px proxy, caption band masked → robust similarity fit: zoom %/s, pan/tilt % width/s, roll) + `camera_grammar` in px/f @720: hold/drift/move shares, move bursts (peak, attack, release, FWHM, size), push-in during holds, hand-held residual, impact kicks, blurred whips (method from mromidev/claude-animated-shorts `motion.md`, MIT) |
| `look.py` | colour/light/detail/palette/faces/letterbox from stills |
| `speech.py` | faster-whisper word timings (`VIDCLONE_WHISPER` = model, default `small`), pace, pauses, hook, closer |
| `audio.py` | loudness (ffmpeg loudnorm), stereo, bed vs voice, key (Krumhansl), tempo, pyin pitch, onsets |
| `text.py` | tesseract OCR; captions = words that match the narration ±2 s; second pass on the caption band with a colour mask |
| `sheets.py` | contact sheets (per second, per shot, sample-vs-new) |
| `profile.py` | analyze one video; merge samples → profile + gates (`GATES` table: path, rule, tolerance) |
| `qa.py` | analyze a video, compare to gates, frame check, report.md/qa.json + compare sheet |
| `frames.py` | every frame at 30 fps: black / unplanned white / frozen holds / pops, planned jumps from the EDL, problems.jpg (idea from mromidev/claude-animated-shorts, MIT) |
| `assemble.py` | EDL → mp4: OpenCV compositor (moves, creep on held shots, impact kicks, transitions, overlays) → ffmpeg (grade, ASS captions, mux) |
| `layers.py` | animated layers on a shot's picture (before the camera move): procedural cartoon eyes (looks, brows, lids, blinks, single profile eye, happy / shock moods, lower lid), PNG props / icons / lens / bounce text with pop, slide, bob, wobble, keyframes (per-key ease, hop, alpha); cut-out blocks with jaw `parts`, contact `shadow`, silhouette `fill`, `glow`; `meter`, `bubble`, `tint`, changing `texts`; `shift_times` |
| `cutout.py` | green-screen prop → trimmed RGBA PNG (soft edge, despill); `--white` for green props shot on white |
| `parts.py` | local motion inside shots = flow minus camera fit: moving-area share, local speed p95 (px/f @720), dominant Hz of the main blob, heat-map sheets — tells "puppet / cut-out animation" apart from stills with camera moves |
| `seedvis.py` | seedvis.com images (Nano Banana 2.1 = model `NARWHAL`, image-to-image with up to 10 references, 9:16, upscale 2k/4k); key `~/.secrets/seedvis_key` |
| `gemini.py` | the user's own Gemini key (`~/.secrets/gemini_key`): Nano Banana image generation (needs billing) and vision `find_points` (eye positions; free tier = 20 requests/day) |
| `captions.py` | ASS from word timings; chunking follows the profile's words-per-caption histogram; pop_from / pop_ms word pop |
| `mixer.py` | numpy mix: voice LUFS, music at `bed_db`, ducking, SFX, mono, final LUFS + true-peak limiter |

## Accuracy (checked on 4 team samples, 2026-11-02)
- Captions: baseline 0.717 / height 0.029 / 75 % one-word — same as the hand-measured Style Bible (71.7 %, 2.7 %, ~70 %).
- Transitions: 0–1 hard cut per sample, dissolves 0.2–0.37 s median (Style Bible: 6–8 frames). Fast whips are sometimes logged as
  dissolves, a fade through a dark frame as a dissolve; flashes are found. Always confirm surprising transitions on the frames
  (`proxy.mp4`, frame numbers in `analysis.json`).
- Camera grammar (2026-11-03): the caption band (`profile.caption_band`, ≈ 57–79 % of the height for one-word 9:16 captions) is left
  out of the camera fit — captions change every word and read as motion. Team S01–S04: move peaks 12–20 px/f, attack ≈ release
  (7–19 f), holds push in 0.15–0.25 %/f, hand-held residual 0.02–0.17 px — in line with the 20-sample toon reference (14 px/f, 10 f/10 f,
  0.14 %/f, 0.08 px). Hold share reads higher (21–35 % vs 10 %): flat backgrounds give no flow. Kicks are informational (not a gate).
- Music character (`percussive_ratio`, `beat_regularity`) is unreliable under continuous narration (voice counts as percussive) — not a gate.
- `bed_under_voice_db` = median level in word gaps minus 75th percentile of speech level; compare it only with the same metric.
- Faces: OpenCV Haar frontal faces (needs `opencv-python-headless<5`; OpenCV 5 dropped CascadeClassifier).
- OCR misses heavily stylised caption fonts → caption share reads low; the band pass recovers most.

## Gotchas
- faster-whisper is fed a numpy array (its PyAV decoder breaks with recent `av`).
- `assemble` decodes video shots with ffmpeg (any codec) at 1.6× cover size so push-ins stay sharp; images are warped from source.
- Transitions overlap the two shots they join: total = Σ dur − Σ transition durations.
- Windows: run in WSL; write bash to a `.sh` file (PowerShell breaks quoting). Long jobs: detach (`Start-Process wsl.exe … -WindowStyle Hidden`).
