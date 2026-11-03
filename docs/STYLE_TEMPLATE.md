# Style bible — <style name>

Samples: S01 … (source, duration, date analysed). Tags: [measured] from analysis.json · [seen] from the sheets · [inferred].

## 1. Format and niche
Platform, aspect, resolution, fps, duration range, audience, topic range, tone (funny / dramatic / calm / hype).

## 2. Narrative template
| Beat | % of duration | Purpose | Typical line (paraphrased, never copied) |
|---|---|---|---|
| Hook | 0–5 % | … | … |
Hook type and length (words, ends by s), turning-point phrases, twist position, closer pattern and length, pace (wpm), pauses,
person (you / he / we), dialogue lines, recurring phrases.

## 3. Visual medium and art direction
Medium (2D/3D/AI art/footage/screen/talking head), drawing style, line/texture, palette (hexes + shares), lighting per act,
character design (proportions, faces, expressions, outfits), sets/props, depth of field, grain.

## 4. Shot grammar
Shot sizes and angles, what each beat type looks like, how a sentence becomes an on-screen action, recurring visual devices
(documents, counters, maps, x-ray, POV, labels), motifs and loops, text-on-screen use.

## 4b. Motion inside the picture
Picture changes / min and local motion [measured, `motion` gates]; what moves (camera only / pose swaps / keyframed cut-out
blocks / puppet parts / real footage) [seen at 10 fps]; entrances and exits, part animation (jaws, limbs), faces / eyes and
how expressions change; every device (gauges, bubbles, counters, icons, labels, ghosts, tints) with the words it lands on.
How to BUILD all of this goes in `recipe.md` (see below).

## 5. Camera and edit
Camera shares (push/pull/pan/tilt/static), move change rate, speeds, shot length median/p10/p90, transitions/min and mix, dissolve length,
cut rules, rhythm against the narration.

## 6. Typography
Captions: font family look, weight, size (height/frame), baseline, colours, outline/box, case, words per caption, animation.
Other text: titles, labels, numbers — font, placement, timing.

## 7. Sound
Voice (gender, age, pitch Hz, energy, accent), music (genre, key, tempo, drums or not, level under voice), SFX types and density,
loudness, stereo/mono, silence use.

## 8. What makes it work
3–6 bullets.

## 9. Avoid
Things that break the style, and the samples' own content (scripts, characters, logos, music) that must not be copied.

---
# Companion files in the style folder
- `recipe.md` — the production recipe: numbers to hit, asset pipeline (which generator, cut-outs, plates, props), the motion
  system and its rules, faces / expressions, devices → layer types, voice settings, lessons from the user's feedback.
- `kit.py` (optional) — helpers for writing this style's EDLs (see `styles/animal-toon-eyes/kit.py`).
- `examples/` (optional) — a reference build the user accepted, our own content only.
