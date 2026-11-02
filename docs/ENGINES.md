# Production engines

vidclone learns any style, but each video still has to be *made* by something. Pick the engine whose output medium matches the samples;
mix engines per shot when the samples do (e.g. footage + AI stills + text cards). All of them end in `bin/vidclone assemble edl.json`
except `3d-toon`, which renders its own frames.

| Engine | Fits samples that are… | Visual source | Strengths | Limits |
|---|---|---|---|---|
| **stills-motion** (default) | illustrated/AI-art story, history, facts, finance/explainer, documentary "Ken Burns", kids stories, quotes | one generated image per shot + camera move in the EDL | any art style, cheap, deterministic, consistent | no character animation (only camera, parallax by layering two images, overlays) |
| **ai-video** | cinematic AI shorts, product/b-roll heavy, "satisfying" loops, motion-heavy scenes | ElevenLabs `creative_generate_video` / vidIQ `generate_video`/`generate_broll`, start frame from stills-motion | real motion, physics, lighting | cost per clip, 3–10 s clips, character drift, text inside clips unreliable |
| **footage** | talking head, podcast clips, gameplay, vlog, tutorials/screen recordings, reaction | the user's own files (`in`/`dur`), vidIQ `generate_clips` for long → short | authentic, fast | needs the footage; punch-in zooms + captions do most of the styling |
| **text/graphics** | quote cards, lists/rankings, data/chart explainers, kinetic typography | images drawn with PIL/matplotlib (charts, cards, number counters) → stills in the EDL; vidIQ `motion_graphics` | exact numbers and type | design work per template |
| **3d-toon** | 3D toon story shorts (round-head characters, x-ray cutaways, constant camera moves) | `rickclips` plugin: three.js scenes, props, characters, CPU render | full 3D action per word | long render (~1–2 h/min), its own toolkit; QA still with `/vidclone:qa` |

Building blocks every engine shares:
- **Camera** (`move`, `amount`, `focus`, or `from`/`to` = (cx, cy, zoom)): push, pull, pan, tilt, drift, handheld, none; easing.
  Hit the profile's camera shares and move-change rate by giving each shot its own move and splitting long shots into 2–3 moves.
- **Transitions** (`trans` on the incoming shot): cut, dissolve (length from profile), fade, flash, whip_left/right/up/down, zoom.
- **Grade** (ffmpeg eq / colortemperature / vignette / unsharp) to land saturation, brightness, contrast, warmth, detail.
- **Captions** from word timings, styled by the profile (+ `style.json` overrides); fonts in `fonts/`.
- **Mix**: voice at −16 LUFS, music bed at the profile's level, ducking, SFX, final LUFS/true peak, mono or stereo.
- **Overlays**: PNG with alpha (logos, labels, stickers, arrows, lower thirds) at times and positions.

Choosing when tools are missing: no video generation → stills-motion with stronger moves and more shots; no TTS → the user records the
voice (still transcribe it for timings); no image generation → stock/user images or text/graphics. Always tell the user which part of the
look the chosen engine cannot reach.
