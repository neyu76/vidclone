# Clone-fidelity lessons (all niches)

Mined from the work sessions on this machine (2026-11-01 → 11-05): animal-toon-eyes (cut-out 2D), RickClips (3D toon
explainers: Pink Prison, Railroads), AbsurdPlay / Sport USA what-if (3D sports), team samples. Each lesson = what the user
rejected or what measurement lied, and the rule that fixed it. Niche-specific rules live in `styles/<name>/recipe.md`.

## A. Before building: study the samples the right way
1. **Same video twice?** Check samples for duplicates (same duration + narration; `merge` now drops them). Sport USA V3 was V1.
2. **Watch at 10 fps, not 1 fps sheets**, and list every recurring device with its time: how people / characters are drawn,
   how props enter, what moves inside a shot, graphics cards, flashes. The user's "it doesn't look like the sample" was
   always a device we had not listed (keyframed blocks, replaced cartoon heads, jaw parts, side characters, TV-style cards).
3. **Imitate the first 15–20 s of one sample first** (same beats, own content), compare side by side, fix, THEN make full
   episodes. Both ATE and RickClips only converged after this step.
4. When the user says "chưa giống / chả đẹp": put sample and clone frames side by side at the same % of time, list the
   differences ranked by impact, and say which ones the numbers missed — before changing anything.

## B. Numbers that lie (and what to look at instead)
5. **Brightness median matched, picture still flat** (RickClips T005): the sample had dark corners, pools of light,
   a vignette, one strong key light (sun through a window), a narrow cold palette with ONE saturated accent. Raising
   exposure to hit the median is the wrong direction. Gates now: `shadow_share`, `luma_spread`, `light_pattern`,
   `vignette`, `hue_spread` (look.light) — re-run `analyze` + `merge` on a style to get them.
6. **Space / lens**: samples shoot wide, camera above or below eye level, 3–4 planes visible (floor, two walls, ceiling),
   subject 1/3–1/2 of the frame height, foreground – subject – background layers, far planes hazier. A flat wall parallel
   to the lens with a subject filling the frame reads as a stage.
7. **Transitions**: short white flashes (2–4 frames, peak 0.5–0.8 white, straddling a cut) were logged as dissolves;
   `edit.short_flash` now requires a near-white jump (share of pixels > 0.7 rising ≥ 0.3). Confirm surprising transition
   counts on the frames.
8. **Caption colour / font / size**: OCR read yellow captions as white; a font chosen by eye was ~40 % too big (ASS size ≠
   pixel height). Use `vidclone capfont` (libass-fitted font, size, margin, outline) and check by burning one caption over
   the sample frame. Caption fonts must be .ttf/.otf — libass silently replaces .woff2 (captions now warn).
8b. `capfont` reads the caption as the white blob near the caption line: on bright frames it grabbed white clothes and a
    thought bubble (width 504 px for a ~220 px word, celeb-toon-heads 2026-11-19). Pick a frame where the caption sits on a
    dark, plain background, and check the measured width against the frame before trusting the font ranking.
9. **Camera**: "moving" can mean constant slow drift (wrong) or hold → fast whip / push (right). Compare hold share,
   push share and whips per minute, not just the share of moving frames.
10. **hook_end_s** reads the first Whisper segment, not the first sentence — a known false fail when the hook is short.

## C. Picture rules that held in every niche
11. **Motion lives inside the pictures** when the samples animate: pose changes every 0.6–1.5 s, cut-out blocks keyframed
    as wholes (enter, land, squash, lean), moving parts (jaws) lifted off — never wobble one point as the main motion.
12. **Don't economise on assets**: every prop, side character, bush, food item the samples show is its own picture /
    block; one picture per pose and per expression.
13. **Characters act with their hands** on props (pour, roll paint, hold food to the mouth); several characters per
    scene with their own expressions when the samples do it.
14. **Detailed, labelled props** where the samples have them (paint can "TRIM RED", taped recipe sheet).
15. **Scene changes**: count scenes in the first 15 s of the sample (Pink Prison: ~8); one scene held for 30 s fails
    even when cuts / min looks fine (reframes are not new scenes).
16. **One graphics package per channel** (fixed card style, colours, font, hard on / off on cuts); never a new look per
    episode.
17. **The subject stays visible**: no prop or graphic covering the main character; faces and key text never in the
    caption band; masks / hats sit where the samples put them (eyes visible).

## D. Voice / length
18. Keep duration and wpm inside the samples' range. To change pace after the fact: time-stretch the voice and shift every
    timing (shots, words, captions) by the same factor in one pass; don't re-plan or re-render scenes.
19. Cap pauses before stretching (ElevenLabs takes read slow even with a fast tag).

## E. Process
20. Keep the engine niche-neutral; put what one channel needs in its style folder (`recipe.md`, `kit.py`, `examples/`).
21. After any detector change, run a regression on every stored sample (old vs new transition mix) and check the new
    hits on the frames before committing.
