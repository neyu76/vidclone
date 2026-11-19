# celeb-toon-heads — production recipe

How this style is MADE with vidclone (`style.md` says what it looks like). Helpers: `styles/celeb-toon-heads/kit.py`
(imports the animal-toon-eyes kit for blocks, keys, props, `split_long`, `grid_crop`). No accepted reference build yet:
the first job is a 15–20 s imitation of one sample's opening (make skill, step 2b).

## Numbers to hit (gates.json, 4 samples)
- 51–67 s, 200–240 wpm, longest pause ≤ 0.4 s, first word at 0.0 s.
- Shot median ~1.9 s (1.05–2.9), 26 transitions/min, ~60 % cuts / 30 % dissolves 0.37 s, no cut in the last 3 s.
- Camera: hold ~75 % of frames; 1–3 snaps per 10 s (3–4 frame attack, peak ~12 px/f @720). Use `kit.write_edl(cam_gain=1.0,
  creep=0)` with most shots on `kit.HOLD`-like still frames (from == to) and a few `FT(a, b, 'out')` punch-ins / pull-outs.
- Picture changes 25–78 / min (median 48): new scene every 1.5–2.5 s + pose / expression swaps + walkers.
- Captions: 1 word, white, black outline, Rubik Black 100 px @1920, baseline ~0.67 (style.json). Keep the person's face out of
  the caption band: frame people so the caption lands on the torso / legs.

## 1. Script (before anything else)
1. Research 8–10 facts about the star / film from at least two reliable sources each (interviews, court records, major outlets).
   Keep a `sources.md` next to the script with one link per fact. Drop anything unsourced, medical, about their children, or cruel.
2. Write: title line → "First off," → facts with turn words → "Lastly," + ironic payoff. 210–240 words for ~60 s.
3. Mark `fact_starts` (the first word of each fact) — they drive the countdown badge.

## 2. Characters: one cartoon head per person, kept for the whole video
- **Head reference first**: generate ONE head sheet per person (front, 3/4, profile; deadpan, grin, worried, eyes closed,
  shocked) with `style.json.head_prompt`. Likeness comes from hair cut and colour, facial hair, skin tone, signature accessories —
  a caricature, never a photoreal face. Approve the sheet before making scenes.
- **Scene pictures**: generate the real-photo scene with the person (Nano Banana 2.1, 9:16 2K), then the head edit
  ("replace the whole head and neck with the cartoon head from reference image 2 …"), always passing the head sheet as a
  reference so every picture has the same head. One picture per pose and per expression — chain edits from the scene's first
  picture so clothes and set stay identical.
- Side characters (mother, doctor, journalist, judge, fans) get their own head sheet when they appear more than once.
- Check identity on a contact sheet of all heads before building; redo any picture whose head drifts.

## 3. Assets per scene
- Scene picture(s) with the person in place; for walkers, turners and anything that moves: an empty plate
  (`image_edit_prompts.empty_plate`) + the person cut out (BiRefNet, full-frame aligned → x = y = 0.5, w = 1).
- Walk cycles: 2–4 pose pictures of the same person mid-stride (left foot / right foot forward), cut out at the same scale →
  `kit.walk(prefix, t0, t1, frm, to)` slides the block and swaps poses at 5 Hz. For a long or complex walk (carrying something,
  two people walking together) use a 2–3 s image-to-video clip instead and keep the head check.
- Vehicles and big props (sports car, truck, jet ski, plane) as separate blocks that drive / slide across (`keys` with
  `ease: linear`), green-screen props cut with `python -m vidclone.cutout`.
- POV inserts (hands + phone, binoculars, plane window) are full pictures of their own; phone screens drawn by us (PIL) or
  generated — never a real app's logo.
- Film topics: rebuild settings in period style (house, cars, clothes of the era); no stills, posters or logos from the film.

## 4. Motion system (kit.py → layers.py)
- Default shot: still picture, camera static, one swap on the key word (expression / pose / prop pop).
- Entrances: `kit.walk` across or into frame; cars `keys` from off-frame; people rise into frame from behind objects.
- `kit.turn(a, b, t)` for a back → front turn (pop turn; layers scale uniformly, no true paper flip).
- Bubbles: `bubble` layer kind thought for dreams / memories (or a PNG with a small cartoon picture inside); speech labels as
  `text` on a white tilted card PNG with lowercase text.
- Icons on their words: `zzz` (sleep), `spark` (gunshot / flash), `note` (music), `question`, `exclaim`, `heart`, `skull`.
- Violence / shock beat: `kit.red_pulse([t])` + `kicks=[t]` + a boom SFX; keep it brief and non-graphic.
- Countdown: `kit.countdown(fact_starts, END, 'art/ui')` → overlays (white disc, black number, 10 → 1; extra steps go into the
  longest facts). Watermark: `kit.watermark('@your.handle', END, 'art/ui')` or nothing.
- Opening: 0–0.3 s close-up crop of the first scene on the star's face, hard cut (or 4-frame pull) to the full scene; the
  badge appears when the title line ends (~2.2–3.5 s).
- Ending: last fact's payoff picture, then a 3–4 s hold (POV, establishing shot with arched title text, or the star in their
  studio) while the music runs out.

## 5. Voice, music, SFX
- ElevenLabs `eleven_v4`, male narrator `UgBBYS2sOqTuMpoF3BR0` (Mark) by default; for a female star pick a female voice
  (`creative_list_voices`) and store it as `voice.female_voice_id`. Prompt tag: `[casual, amused, fast-paced, like telling a
  friend wild celebrity gossip]`. Cap pauses at 0.3 s, then atempo to reach 215–235 wpm.
- Music from `style.json.music_prompt`, bed −7 dB (samples −6.6, louder than the animal style), no ducking needed.
- SFX from a real library, one per visual cue: whoosh (walk-ins, cars), pop (bubble, badge, prop), camera shutter (paparazzi),
  cash register (money), boom (shock), phone ding (texts). 6–12 per minute.

## 6. QA notes
- `hook_end_s` reads title + fact 1 (no full stop between) — the samples read 7.3–8.8 s, so it is gated as is.
- `face_share` counts Haar faces on cartoon heads (0.15–0.97 in the samples); a low value means people are too small in frame.
- Captions: check that the caption band never covers a face.
