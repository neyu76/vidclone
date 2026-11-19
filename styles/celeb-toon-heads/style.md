# Style bible — celeb-toon-heads

US celebrities and US movies as "10 Weird Things You Didn't Know About X" shorts. Real-photo bodies and sets, with the
person's **whole head and neck** turned into a flat 2D cartoon meme drawing. Adapted from `animal-toon-eyes`: animals → people,
cartoon eyes on a real face → a fully drawn cartoon head (caricature), myth-busting script → numbered countdown of facts.

Samples (local only, analysed 2026-11-19): S01 pop singer, ex-boy-band 61.7 s · S02 rapper 67.0 s · S03 the real house behind
a horror film franchise 62.7 s · S04 pop diva 50.9 s (female narrator). All four come from one channel (the handle is burned in,
bottom centre). Tags: [measured] analysis.json/profile.json · [seen] contact sheets and 10 fps strips · [inferred].

## 1. Format and niche
- Vertical 1080×1920, 30 fps [measured]. 51–67 s, median 62 s [measured].
- English, US-casual. Topic = one famous person (singer, rapper, actor) or one film / the true story behind it (haunted house,
  real case, set accident) [seen]. Audience: teens / young adults who know the name. Tone: gossip, "can you believe this",
  deadpan — never mean, never a takedown [inferred].
- **Our niche** (user request 2026-11-19): US celebrities and US movies — actors, singers, rappers, athletes-turned-stars,
  film productions, the true stories behind films, famous on-set incidents.

## 2. Narrative template
| Beat | % of duration | Purpose | Typical line (paraphrased) |
|---|---|---|---|
| Title hook | 0–4 % (title line ends ≈ 2–3 s) [measured] | the fixed formula, said as one line | "10 weird things you didn't know about <name>." |
| Fact 1 | 4–15 % | "First off," + the most relatable odd fact, often from childhood or the start of their career | "First off, as a kid they nearly skipped the audition that made them famous because …" |
| Facts 2–N | 15–90 % | 6–9 more facts, each 1–2 sentences, each opened by a turn word | "Next, …" / "Even weirder, …" / "Even crazier, …" / "Before becoming famous, …" |
| Last fact / closer | last 1–2 sentences, 5–22 words (median 15.5) [measured] | "Lastly," + an ironic or full-circle payoff | "Lastly, a dating app banned them for using fake photos of themself — except the photos were real." |

- The hook gate reads 7.3–8.8 s because Whisper glues the title to fact 1 (no full stop between them) [measured]; the spoken
  title itself takes ~2.2 s.
- Pace 199–241 wpm (median 224) [measured], first word at 0.0 s, longest pause ≤ 0.4 s [measured]; sentences 17–24 words [measured].
- 0 questions, "you" only in the title [measured]. Third person, past tense, the star's name repeated in almost every fact instead of "he / she" [seen].
- Turn words: "First off," → "Next," ×2–4 → "Even weirder," / "Even crazier," ×1–3 → "Lastly," [measured in transcripts].
- Closer: 3 of 4 end on the last fact with no outro; S04 ends "Follow for more weird facts." [measured]. Default: no CTA.
- Facts mix harmless quirks (sleep, food, phobias, habits) with 1–2 darker ones (arrest, shooting, haunting) [seen].
  **Our rule**: only facts that are on public record (interviews, court records, major outlets) and phrased with their source
  ("they said in an interview", "reportedly", "pleaded no contest"); no health, sexuality or crime claims without a source;
  nothing about the person's children.

## 3. Visual medium and art direction
- **Real photo world + drawn heads** [seen]: bodies, clothes, hands, props and backgrounds are photoreal (AI photos); only
  the head and neck down to the collar are a flat 2D cartoon. That contrast is the joke and the brand.
- **Cartoon head design** [seen, close-ups S01 0.2 s, S03 0.1 s, S04 12 s]:
  - flat warm skin fill with soft cel shading, thin clean black outline (~1.5–2 % of head width), head ~1.1–1.2× real size;
  - eyes: white almond / oval with small black pupils and a heavy black upper lid — a tired, deadpan stare is the default;
    brows short and thick;
  - nose = 2–3 thin lines; mouth = a short line, a small open dark oval, or bared teeth for a grin;
  - hair, beard and stubble drawn as flat shapes in the person's real colour and cut (the signature quiff, dreads, ponytail,
    curls) — the hair carries the likeness; earrings, chains, glasses kept;
  - neck drawn too, joining the real collar / neckline cleanly;
  - expressions change per beat: deadpan, worried, eyes closed asleep (+ "zZz"), smug grin, shock (tiny pupils), crying.
- **Side characters** (parents, doctors, journalists, judges, fans, the other celebrity in a story) get the same cartoon heads [seen].
  Strangers in a crowd sometimes have blank cartoon heads with dot eyes [seen S02].
- Sets: city streets, suburban houses, bedrooms, studios, stages, prison cells, vet clinics, hotel rooms, mansions; daylight or
  night with street lamps [seen]. Palette per scene (no channel colour); warm b* +5, brightness median 109, contrast 60,
  saturation 61, shadow share 0.26 [measured]. Accents come from props (red sports car, purple tracksuit, neon UFO light).
- Film topics (S03): period sets matching the story (1970s farmhouse, family in 70s clothes), dark rooms for the scary beats,
  one real-footage-looking cutaway (war explosion) for a historical claim [seen].

## 4. Shot grammar
- The person is **full body, centred, standing on the ground plane, small to medium in frame** (head at 25–45 % of the height),
  facing camera or in profile [seen]. Close-ups only for the opening frame and reactions.
- One scene per clause: every fact gets 3–6 different scenes (a new place or pose every 1.5–2.5 s) [measured shot median 1.87 s,
  seen]. Example pattern (S01 fact 1, paraphrased): asleep in bed + thought bubble of the audition panel + alarm clock 4:00 →
  mother at the door pointing → sitting up on the bed → walking out.
- The key noun gets a literal prop or set: the chicken under the arm at the vet, the jet ski, the suitcase left on the road,
  the stack of 200 books in the cell, the $10,000 stack handed over, the rings on a hand, the donut tray [seen].
- Recurring devices [seen]:
  - **countdown badge** top-left (white disc, black number) from the end of the title line, 10 → 1 over the video, about one
    step per 5–6 s; "1" holds to the end. It counts down even when fewer than 10 facts are told (S01 has 8). S04: plain white
    "10." with black outline.
  - thought bubble (white cloud, black outline) with a small cartoon picture inside (the audition panel, the alien);
  - speech label: tilted white rectangle with black lowercase handwritten-ish text ("i see potential in you", "welcome home mr …");
  - POV inserts: two real hands holding a phone (texts, a live-stream, a dating app), binoculars mask on black, a plane window;
  - icons: "zZz", muzzle flash spark, music notes from a mic, pink sound-wave at an ear (voices), "?" ;
  - a real hand / arm entering from a frame edge to hand over money or block the face;
  - arched title text over the location for a closing establishing shot (film topics);
  - red edge vignette pulse on the shooting / violence beat;
  - shadow figure / ghost silhouette in a doorway (horror topics), UFO beam (dream / alien claim).
- Closing shot holds 3–5 s on a simple tableau (POV phone, the house at sunset, the star in the studio) [measured tail 0.4–5.6 s].

## 4b. Motion inside the picture
- Picture changes 25–78 / min, median 48 [measured `picture_changes_per_min`]; local motion share 0.33 (0–0.86), p95 8.4 px/f
  [measured] — busier than stills + camera (15–20), calmer than the animal style (69–100 %).
- What moves [seen at 10 fps]: people **walk in / walk across** with a real walk cycle (S01 6 s with the chicken, S02 couples
  walking); cars and trucks drive across the frame (S01 0–2 s); a person **turns around** (back → front, S04 0.8 s) with a
  squeeze; sit down / stand up as pose swaps; the countdown badge swaps; thought bubbles and icons pop.
- Faces: expressions are new drawings, swapped on the word (eyes open → shut, deadpan → grin). Eyes dart in a held shot
  (S03 voices beat). No lip sync [seen].
- Opening: 0.0–0.3 s close-up of the star's cartoon face, then a hard pull-out to the full scene (S01, S03, S04) [seen].

## 5. Camera and edit
- Camera **mostly holds**: static 76–86 % of frames, hold share 0.74 [measured]; push 10 %, pull 4 %, pan 3 % [measured].
  Moves are short snaps: peak 12 px/f @720, attack 3.5 frames, fwhm 7 frames, 1.6 moves / 10 s [measured] — punch-in on a
  reaction word, pull-out to reveal, quick slide to follow a walker. No slow creep (quiet push rate 0.14 %/f, residual 0) [measured].
- Median shot 1.87 s (1.05–2.9) [measured]; 26 transitions/min [measured]; mix ≈ 60 % hard cuts, 30 % dissolves (0.32–0.40 s),
  rare whip, S04 adds short white flashes [measured]. Dissolves mark a new fact; cuts run inside a fact [seen].
- No cut in the last 3 s [measured].

## 6. Typography
- Captions: **one word at a time** (97–100 %) [measured], UPPERCASE [measured], white fill, black outline (~9 px @1920) and a soft
  dark shadow [seen], small: letter height 2.2 % of the frame [measured]; baseline median 0.67 (0.58–0.76) — on the person's body
  around the waist [measured]. Font: heavy wide rounded sans (closest OFL: Rubik Black; capfont IoU 0.44) [measured]. S04 uses a
  bigger cartoon display face (Titan One look, ~4.5 % height) [seen].
- Badge numbers: heavy black sans in a white disc, top-left at (0.085, 0.097), disc ≈ 0.135 of the width [seen].
- Speech / sign text: black lowercase casual handwriting on white tilted labels [seen].
- Channel handle bottom centre, small, ~55 % opacity — ours or none, never theirs.

## 7. Sound
- Voice: adult male, f0 111–113 Hz, casual US storyteller (S01–S03); adult female, f0 203 Hz (S04, a female star) [measured].
  Speech covers ~85 % of the runtime [measured].
- Music: steady minor-key underscore (C, G#, A, G minor), 117–129 bpm, regular beat (trap-ish hats / soft plucks) [measured];
  **louder than the animal style**: bed −6.6 dB (−11 … −0.6) under the voice [measured].
- SFX: sparse hits on visual changes, 9 gap hits/min (S01) [measured]; whooshes on walk-ins, a pop on the badge or bubble,
  a boom or shot on violent beats [seen].
- Loudness −14.2 LUFS (−16 … −8), true peak ≤ −3 dBTP, near-mono (side −16 dB) [measured]. We deliver −14 LUFS / −1 dBTP.

## 8. What makes it work
- A famous name in the first 2 s + a fixed, trusted formula ("10 weird things…") + a visible countdown = people stay to reach 1.
- Real world + drawn heads: instantly funny and readable, and clearly a cartoon — not a photo of the real person.
- Every clause becomes a literal mini-scene with one prop, so 220 wpm of facts never feels like a lecture.
- Quirky facts first, one or two darker ones in the middle, an ironic payoff last.

## 9. Avoid
- Photoreal faces, face swaps, lip-synced mouths — the head must always be an obvious flat drawing (likeness via hair, beard,
  signature accessories, not a realistic face). No sexualised or degrading depictions of real people.
- Unsourced allegations, rumours stated as fact, medical or private-life claims; mocking victims in crime / tragedy facts.
- Real film stills, posters, studio logos, trailer footage, movie music, or a cloned voice of the star — recreate scenes with our
  own generated pictures and say "in the movie …".
- Do not copy the samples' scripts or fact lists (re-research every topic), the channel's handle or watermark, or its music.
- Long holds without a swap (> 2.5 s outside the closing shot), big multi-word captions, captions on the face.
