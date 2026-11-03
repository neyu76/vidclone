# animal-toon-eyes — production recipe

How this style is MADE with vidclone (the bible `style.md` says what it looks like; this file says how to build it).
Helpers: `styles/animal-toon-eyes/kit.py`. Reference build: `examples/remake_s01_edl.py` (our own script; S01's first 20 s
structure), accepted by the user 2026-11-03.

## Numbers to hit (measured, `motion` gates in gates.json)
- Picture changes / min (cuts + pose swaps + block moves, `frames.motion`): samples 48–82 over whole videos (S01 98 in its
  busy first 20 s); gate 31–110. Stills with camera moves only reach 15–20 — the action must come from pose pictures and
  keyframed blocks. Reference build: 115 / min.
- Local motion inside shots: 69–100 % of the frame moving, p95 5–11 px/f @720 (reference build 95 %, 16).
- Camera calm while pictures change: camera moving on ~48 % of frames. Small travel per shot (`CAM_GAIN` 0.45 in the
  reference); a big push/pull on every swap hides the swaps.

## 1. Pose script (before any image is made)
Per sentence, the poses the character goes through — one new pose or framing every 0.6–1.5 s (stand → sit → paw on chin →
close-up worried → squashed by a patting hand …). Each pose is its own picture, chained from the character's base picture so
identity holds. 2-frame loops for repeated actions (rubbing a forehead, paddling): two pictures swapped at 2–4 Hz.
Several characters when the narration lists animals; a human stand-in (real body, flat cartoon head) for "scientists / you".
Per pose 1–2 events on the words: expression change, icon pop, bubble, prop slide, squash on impact.

## 2. Assets
- Pose pictures: Nano Banana 2.1 (ElevenLabs `gemini-nano-banana-2.1`, 9:16 2K), realistic animal photo, natural eyes visible.
- Every pose cut out with BiRefNet (full-frame, aligned → x = y = 0.5, w = 1 is its original place).
- ONE clean plate per scene ("remove the animal" edit of a base picture), slightly blurred (radius = width / 300).
- Props, food, plants, side characters generated separately: on pure green #00FF00, or on white #FFFFFF when the prop
  itself is green (grass, leaves) → `python -m vidclone.cutout in.png out.png [--white]`.
- Don't skimp: every prop the samples have is its own block — food held to the mouth, bitten food, chewed bits, grass
  tufts at the feet and in the mouth, bushes / ferns in front of people. Group shots are REBUILT from separate blocks over an
  empty plate, every side character with toon eyes and its own entrance; side characters peek in at frame edges later.

## 3. Motion = keyframed blocks (never point wiggle as the main motion)
- Walk in from the edge with `hop` bounces and shrink to the spot; drop onto a seat with a landing squash (`LAND`); snap in
  with `ease: back`; lean / tilt about a `pivot`; slide in from the side the body is cut off on; rise from the bottom.
- Eating = the jaw lifted off the block (`parts`, dark mouth behind) chewing about its hinge + the food block moving to the
  mouth on each bite + chewed bits popping (`kit.bites`).
- Contact `shadow` under standing / sitting blocks; eyes ride on the block (`parent`).
- Cover cut-out defects (broken legs, halos) with a foreground prop (grass tuft, bush).

## 4. Eyes and expressions
- Sample look: big white eyeball, grey rim, black pupil with highlight, thick round black brows (`brow_w` 0.22).
- Size ≈ 0.75 × eye spacing for pandas / bears (after the ×1.3 in `kit.eyes`), smaller for wide-set dog eyes; close-ups bigger.
- Profile / three-quarter view: ONE eye (`single`: "l" when the nose is to the right of the eye).
- An expression change on almost every beat: brows (up / worried / sad / smug / angry), half lid + `low`, `mood: happy`
  (white ^ band, readable on dark fur), `mood: shock` (small pupils), `pupil` 1.25 for pleading eyes.
- Dark-furred animals: set `lid` (panda #a39c92, black dog #5a524c) or half lids read as black slits.
- Read eye / jaw positions off gridded crops in picture fractions (`kit.grid_crop`), never by guess.

## 5. Devices seen in S02–S05 (layers.py)
battery `meter` draining with effort · cutout `fill` (silhouette energy gauge) · `bubble` thought / speech whose words
change (`texts`) · `text` + `texts` for calendars and counters · `tint` for night → day / flashback (list it last) · keys
`alpha` + icon `halo` for a ghost · cutout `glow` for the injured / chosen one · icons skull / heart / clock / fire / zap / note
on their words · line-ups of characters entering one by one over labels · big orange outlined words on objects.
Never copy the channel's round logo (top-right) — our own mark or none.

## 6. Voice and captions
ElevenLabs `eleven_v4`, voice `UgBBYS2sOqTuMpoF3BR0` (Mark) reads ~181 wpm → cap pauses at 0.25 s, then atempo 1.2 (~235 wpm).
Transcribe with `--lang en`, align to the script. Captions: one word, Anton, orange gradient, y 0.72 (style.json).
