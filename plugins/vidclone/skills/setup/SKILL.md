---
name: setup
description: Prepare this machine for vidclone — get the repo, install ffmpeg/tesseract and the Python analysis venv, check which generation connectors (ElevenLabs, vidIQ, Notion…) and engines (rickclips, GPU) exist, and save it all to ~/.vidclone/config.json. Run once per machine, or when another vidclone skill finds no config.
---
# vidclone setup

1. **Where to run.** Linux/macOS: the normal shell. Windows: WSL (`wsl.exe -u root bash <script.sh>`; PowerShell mangles `$`, `&&`, `(` —
   write bash into a scratch `.sh` file and run that). Record the prefix as `run_prefix`.
2. **Code.** If the repo is not on this machine: `gh repo clone <owner>/vidclone` (ask the user for the repo if unknown). Record `repo_dir`.
3. **Toolchain.** `bash setup.sh` (apt/brew packages + venv at `~/.vidclone/venv`), then `bash setup.sh --check`. All lines must say `ok`
   (demucs is optional: `bash setup.sh --extras` only if stem separation is wanted).
4. **Generation tools** — check what this session actually has (ToolSearch / connector status), don't assume:
   | Need | First choice | Fallbacks |
   |---|---|---|
   | Voice (TTS, clone) | ElevenLabs connector `creative_generate_speech` | vidIQ `vidiq_voiceover_generate`; the user records it |
   | Images | ElevenLabs `creative_generate_image` (check models with `creative_get_model_guide`) | vidIQ `generate_broll`/`generate_thumbnail`; user art |
   | Video clips | ElevenLabs `creative_generate_video` | vidIQ `vidiq_generate_video`/`generate_broll`; user footage |
   | Music / SFX | ElevenLabs flow nodes (music, text-to-sound) | vidIQ `vidiq_generate_music`; user library |
   | Transcription | local faster-whisper (in the venv) | ElevenLabs `creative_transcribe_audio` |
   | Script source | Notion connector / pasted text | — |
   | 3D toon engine | `rickclips` plugin + repo (if installed) | stills-motion engine |
   Never ask for or store API keys in chat, config, repo or memory; keys only in `~/.secrets/<name>_key` (chmod 600) if a tool truly needs one.
5. **Hardware.** `nproc`, RAM, `nvidia-smi` (GPU enables local 3D/AI tools, e.g. Hunyuan3D via rickclips `prop-3d`).
6. Write `~/.vidclone/config.json`:
   ```json
   {"repo_dir": "...", "run_prefix": "wsl.exe -u root bash" , "styles_dir": "<repo_dir>/styles", "work_dir": "~/vc_work",
    "deliver_dir": null, "tools": {"voice": "elevenlabs", "image": "elevenlabs", "video": "elevenlabs", "music": "elevenlabs"},
    "voice": {"voice_id": null, "model": null}, "engines": ["stills-motion", "footage", "ai-video"], "gpu": "RTX 3060 12 GB"}
   ```
   Ask once for `deliver_dir` and a default voice when first needed, then remember them here.
7. Report what works and what does not (and the fallback for each gap).
