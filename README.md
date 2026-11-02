# vidclone

Learn a video style from sample videos — any niche — and make new videos in that style, checked against the samples.

```
samples ──analyze──▶ analysis.json + sheets ──merge──▶ profile.json + gates.json      (numbers)
                                    └── Claude reads frames + transcript ──▶ style.md + style.json   (bible + production plan)
topic/script ──▶ voice ──▶ words.json ──▶ shot list ──▶ images / clips / footage ──▶ edl.json ──assemble──▶ final.mp4 ──qa──▶ report
```

```bash
bash setup.sh                                               # ffmpeg, tesseract, venv (~/.vidclone/venv)
bin/vidclone analyze sample1.mp4 --style styles/my-style --id S01
bin/vidclone merge styles/my-style                          # profile.json + gates.json
bin/vidclone transcribe voice.mp3 --out words.json --script script.txt
bin/vidclone assemble edl.json                              # format: vidclone/assemble.py docstring
bin/vidclone qa out/final.mp4 --style styles/my-style       # report.md + compare sheets
```

## Claude Code plugin
```
/plugin marketplace add neyu76/vidclone        # or a local path to this folder
/plugin install vidclone@vidclone
/vidclone:setup                                 # once per machine
/vidclone:learn <video(s)> [files]  as my-style
/vidclone:make my-style <topic | script | Notion link>
/vidclone:qa <video> my-style
```

What is measured: edit (shots, cut/dissolve/flash/fade/whip, camera push/pull/pan/tilt/static, move rate), look (saturation, brightness,
contrast, detail, warmth, palette, faces), speech (wpm, pauses, hook, closer), audio (LUFS, true peak, stereo, music bed level, key,
tempo, voice pitch, SFX density), text (caption position/size/colours/words per caption, other on-screen text). See `CLAUDE.md`.
Engines for making videos: `docs/ENGINES.md`. Style bible template: `docs/STYLE_TEMPLATE.md`.

Samples, their frames and audio stay on the machine that analysed them (`styles/*/samples/*/work` is git-ignored); new videos are
original content in the learned style.
