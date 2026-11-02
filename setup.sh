#!/bin/bash
# vidclone toolchain (Ubuntu/Debian, WSL, macOS with Homebrew). Idempotent.
#   bash setup.sh            install system packages + Python venv (~/.vidclone/venv)
#   bash setup.sh --check    report what is installed
#   bash setup.sh --extras   also demucs (stem separation, ~2 GB with torch)
set -e
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="${VIDCLONE_VENV:-$HOME/.vidclone/venv}"
PKGS="numpy scipy opencv-python-headless<5 pillow scikit-learn soundfile librosa pyloudnorm scenedetect faster-whisper"

check() {
  for b in ffmpeg ffprobe tesseract python3; do printf '%-10s %s\n' "$b" "$(command -v $b >/dev/null && echo ok || echo MISSING)"; done
  [ -x "$VENV/bin/python" ] && "$VENV/bin/python" - <<'PY' || echo "venv       MISSING ($VENV)"
import importlib
for m in ["cv2", "librosa", "pyloudnorm", "scenedetect", "faster_whisper", "sklearn", "soundfile", "demucs"]:
    try: importlib.import_module(m); print(f"{m:10s} ok")
    except Exception: print(f"{m:10s} {'optional' if m == 'demucs' else 'MISSING'}")
PY
}
[ "$1" = "--check" ] && { check; exit 0; }

if command -v apt-get >/dev/null; then
  SUDO=$([ "$(id -u)" = 0 ] || echo sudo)
  $SUDO apt-get update -qq
  $SUDO apt-get install -y -qq ffmpeg tesseract-ocr fonts-dejavu-core python3-venv python3-pip >/dev/null
elif command -v brew >/dev/null; then
  brew install ffmpeg tesseract python >/dev/null
else
  echo "Install ffmpeg, tesseract and python3 (with venv) yourself, then rerun." >&2
fi
[ -x "$VENV/bin/python" ] || python3 -m venv "$VENV"
"$VENV/bin/pip" install -q --upgrade pip
"$VENV/bin/pip" install -q $PKGS
[ "$1" = "--extras" ] && "$VENV/bin/pip" install -q demucs
chmod +x "$ROOT/bin/vidclone"
check
echo "CLI: $ROOT/bin/vidclone   (first transcription downloads the Whisper model, ~500 MB)"
